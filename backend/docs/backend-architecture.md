# 后端架构文档（Backend Architecture）

> 基于 `backend/` 源码梳理，更新时间：2026-07-14。本文描述当前实现，而非目标蓝图。

## 1. 定位与运行边界

后端是一个面向大学生情绪管理场景的 Python 服务：提供账户与后台管理、情绪日记和统计、CAPS 情绪图片、DBT 技能库，以及以 LLM/规则驱动的对话干预。HTTP 服务由 FastAPI 承载，默认从 `backend/start_backend.py` 以 Uvicorn 在 `8000` 端口启动；FastAPI 模块自身的直接启动入口使用 `3000` 端口，部署时应统一使用前者。

```mermaid
flowchart TB
    Client[Web / 移动端] --> API[FastAPI app.main]
    API --> Auth[JWT 认证与权限依赖]
    API --> Domain[API 路由层]
    Domain --> Repo[Repository 数据访问层]
    Domain --> Agent[对话 / Agent 层]
    Repo --> DB[(SQLite，默认)]
    Agent --> LLM[OpenAI 兼容 LLM]
    Agent --> Vision[视觉模型服务]
    API --> Static[/static CAPS 图片]
```

## 2. 模块分层

| 层级 | 目录/入口 | 职责 |
| --- | --- | --- |
| 进程与应用 | `start_backend.py`、`app/main.py` | 启动、日志、CORS、异常处理、路由和静态资源注册、建表与默认管理员初始化。 |
| 接口层 | `app/api/` | 认证、日记、对话、图片情绪、DBT、管理后台的 HTTP 契约与参数校验。 |
| 应用/领域能力 | `app/core/`、`app/dbt/` | JWT/密码、LLM 与视觉客户端、危机检测、情绪识别、技能推荐、评估、DBT 技能字典。 |
| Agent 编排 | `app/agent/` | LangGraph 状态机（默认路径）及保留的三 Agent 顺序协调器。详细见《Agent 架构文档》。 |
| 数据访问 | `app/database/repositories/` | 按聚合封装用户、会话、日记、技能使用、危机事件、管理员的 CRUD 与统计查询。 |
| 持久化模型 | `app/database/models.py` | SQLAlchemy ORM 表、索引、外键与序列化字段。 |
| 表现/资源 | `static/`、`utils/` | CAPS 情绪图片静态资源及图片 data URL 工具。 |

依赖方向总体为 `API → core/repository/agent → database model`。`core` 中的危机检测和技能推荐可按需引用 Repository 读取历史数据；这使推荐个性化与危机重复判定可以复用数据层。

## 3. 应用装配与横切能力

- `Settings` 从 `backend/.env` 读取配置，覆盖数据库、JWT、LLM、视觉模型、危机阈值、缓存和日志参数；默认数据库 URL 为 `sqlite:///./data/emotions.db`。
- 启动事件调用 `init_db()` 创建表，并创建默认超级管理员。日志同时写入控制台及 `./logs/app.log`。
- 全局异常处理器由 `app/middleware/exceptions.py` 注册；路由内部大多将异常映射为含 `{code, message}` 的 `HTTPException`。
- CORS 当前允许所有来源、方法和头；静态文件挂载在 `/static`。
- 用户接口以 `Authorization: Bearer <JWT>` 鉴权；管理员可用 `Admin-Authorization: Bearer <JWT>`，也兼容通用 `Authorization`。管理员删除用户需要 `super_admin`。

## 4. 数据架构

| 聚合/表 | 关键关系与用途 |
| --- | --- |
| `users` | 普通用户、资料和账户状态。 |
| `admins` | 管理员账号、角色（含 `super_admin`）和状态。 |
| `emotion_diaries` | 用户每日一篇情绪日记；`(user_id, diary_date)` 唯一，包含情绪、强度、触发因素、身体部位、图片选择。 |
| `chat_sessions` | 一个用户的会话元信息、首末强度、危机标记、评估数据和可选 Agent 状态。 |
| `chat_messages` | 会话内消息、消息类型和附加数据。 |
| `skill_usage_records` | DBT 技能练习前后强度、效果及上下文；为历史低效技能过滤和重复高强度判定提供数据。 |
| `crisis_events` | 危机触发原因、关键词、风险等级与处理状态，供后台查看。 |
| `emotion_images` | CAPS 图片的分类、VAD（效价/唤醒度/支配度）与静态文件路径。 |

SQLite 适合开发与单进程部署；生产环境应通过 `DATABASE_URL` 切换到支持并发与备份策略的数据库。数据库迁移脚本位于 `app/database/migrations/`，但运行时目前使用 `Base.metadata.create_all()`，并非版本化迁移框架。

## 5. 核心业务流

### 5.1 日记与图片情绪

用户创建/更新日记时，路由层将前端兼容字段（`emotion`、`emotionLabel`）归一化为内部字段，并将列表/对象存成 JSON 文本。统计接口从日记聚合分布、均值、连续记录天数和趋势。

图片情绪路径是独立于 Agent 的可解释规则：前端取得 CAPS 图片，提交 `selectedImages` 与强度；服务端求所选图片的平均 VAD 后映射成焦虑、愤怒、悲伤、快乐、平静或中性。

### 5.2 对话与干预

默认 `POST /api/chat/message` 先写入用户消息、恢复最近 20 条历史，再从进程内 LangGraph checkpoint 恢复或初始化状态。状态图完成情绪识别、危机检测、技能练习、效果评估和总结；最终回复与会话的初始情绪信息会写库。五条文本消息后还有一条独立的情绪评估引导分支，向客户端请求图片选择。

详见《Agent 架构文档》。

## 6. 外部依赖与降级

| 依赖 | 配置 | 使用位置 | 降级行为 |
| --- | --- | --- | --- |
| OpenAI 兼容 LLM | `LLM_*` | 文本情绪识别、推荐话术、步骤引导、危机确认、总结 | 未配 key 时客户端不可用；部分节点使用模板或规则，部分通用生成返回默认共情文案。 |
| 视觉模型 | `VISION_*` | Agent 图片识别节点 | 图片选择本身仍可通过 metadata 直接提供情绪。 |
| 数据库 | `DATABASE_URL` | 全部持久化与统计 | 默认 SQLite。 |
| CAPS 静态文件 | `static/images/caps` | 图片列表与选择 | 依赖 `emotion_images` 中的路径和已导入元数据。 |

## 7. 当前实现观察与演进优先级

以下是源码层面的重要约束，应在继续扩展前纳入计划：

1. `MemorySaver` 是进程内内存状态，重启或多实例时无法保持默认 LangGraph 会话状态；数据库中的 `agent_state` 仅被兼容的 multi-agent 端点使用。应改用共享/持久化 checkpointer，或统一持久化策略。
2. 服务同时存在 LangGraph 默认路径和旧式协调器路径，两套状态字段、危机工具和引导逻辑并存。应明确唯一生产编排路径，并为另一条路径设为弃用或完成收敛。
3. API 层使用 `async def`，而 SQLAlchemy 与部分 LLM 调用为同步操作；高并发下会阻塞事件循环。可将同步 I/O 移入线程池或换用异步数据库/客户端。
4. 危机节点调用检测器但没有在默认图中创建 `crisis_events` 记录；后台的危机列表依赖该表，因此应把记录写入纳入确认后的危机事务。
5. `ChatRepository.save_message()` 传入了 ORM 模型未声明的 `metadata` 字段，而模型字段名是 `extra_data`；历史元数据的写读路径需要一次集成测试和字段统一。
6. 生产安全需要收紧 CORS、移除硬编码默认管理员/默认密钥、配置真实密钥和密钥轮换，并审查危机热线内容的运营有效性。

## 8. 关联源码

- 应用入口：[main.py](/Users/zeno/program/EmotionalAssistant/backend/app/main.py)
- 配置：[config.py](/Users/zeno/program/EmotionalAssistant/backend/app/config.py)
- 数据模型：[models.py](/Users/zeno/program/EmotionalAssistant/backend/app/database/models.py)
- 路由集合：[api](/Users/zeno/program/EmotionalAssistant/backend/app/api)
- Agent 图：[langgraph_builder.py](/Users/zeno/program/EmotionalAssistant/backend/app/agent/langgraph_builder.py)
