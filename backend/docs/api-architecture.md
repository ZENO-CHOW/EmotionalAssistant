# API 架构文档（API Architecture）

> 基于 `backend/app/main.py` 与 `backend/app/api/` 源码梳理，更新时间：2026-07-14。交互式契约可通过运行服务后的 `/docs` 查看。

## 1. 通用约定

- **Base URL**：`http://<host>:8000`（使用 `start_backend.py` 启动时）。除根路径、健康检查和静态资源外，业务 API 均以 `/api` 开头。
- **内容类型**：请求和响应默认 `application/json`。`POST /api/chat/message/stream` 的实现产生 SSE 格式文本事件。
- **认证**：受保护的普通用户接口传 `Authorization: Bearer <user-jwt>`；管理员接口优先传 `Admin-Authorization: Bearer <admin-jwt>`，也接受 `Authorization`。
- **分页**：常用 `page` 从 1 开始，`page_size` 默认 20；各接口最大值不完全一致，应遵循下表。
- **错误**：多数业务错误为 `{"detail":{"code":<HTTP状态>,"message":"..."}}`，少数图片/DBT 接口会返回字符串 `detail`。客户端需按 HTTP 状态码为准，并兼容两种 detail 形态。

## 2. 服务、认证与资源

| 方法 | 路径 | 认证 | 说明 |
| --- | --- | --- | --- |
| GET | `/` | 否 | 服务名称、版本与运行状态。 |
| GET | `/health` | 否 | 健康检查，返回 `{"status":"healthy"}`。 |
| GET | `/docs`、`/redoc` | 否 | FastAPI 自动文档。 |
| GET | `/static/{path}` | 否 | CAPS 图片静态资源。 |
| POST | `/api/auth/register` | 否 | 注册；`username`、`password`、`confirmPassword` 必填，另有 email/phone/school。 |
| POST | `/api/auth/login` | 否 | 用户名或邮箱 + 密码登录；返回 `data.token` 与 `data.userInfo`。 |
| GET | `/api/auth/user` | 用户 | 读取当前用户资料。 |
| PUT | `/api/auth/user` | 用户 | 更新昵称、邮箱、手机号、学校、头像。 |
| POST | `/api/auth/change-password` | 用户 | `currentPassword`、`newPassword`。 |
| POST | `/api/auth/logout` | 用户 | 无状态 JWT 的客户端退出确认；服务端未维护黑名单。 |

用户与管理员 token 不能混用：解析函数分别读取用户/管理员 JWT claim。

## 3. 日记、统计与图片 API

| 方法 | 路径 | 认证 | 请求 / 查询参数 | 说明 |
| --- | --- | --- | --- | --- |
| POST | `/api/diary` | 用户 | `CreateDiaryRequest` | 新建日记；每天每用户一篇。 |
| GET | `/api/diary/list` | 用户 | `page`、`page_size≤100`、`start_date`、`end_date`、`emotion_type` | 日记列表。 |
| GET | `/api/diary/{diary_id}` | 用户 | 路径 ID | 日记详情。 |
| PUT | `/api/diary/{diary_id}` | 用户 | `UpdateDiaryRequest` | 局部更新。 |
| DELETE | `/api/diary/{diary_id}` | 用户 | 路径 ID | 删除日记。 |
| GET | `/api/diary/today` | 用户 | — | 当日记录，不存在时返回 `null`。 |
| GET | `/api/emotion/statistics` | 用户 | `time_range=week|month|quarter|year` | 个体情绪统计、连续天数与趋势。 |
| GET | `/api/emotion/trend` | 用户 | `days=1..365` | 个体每日趋势。 |
| GET | `/api/emotion/images` | 否 | `category`、`limit=1..50`、`random_select` | CAPS 图片列表与 VAD 数据。 |
| POST | `/api/emotion/analyze` | 否 | `{selectedImages, intensity}` | 以图片平均 VAD 映射情绪。 |
| GET | `/api/emotion/images/statistics` | 否 | — | CAPS 图片库分类统计。 |

### 日记请求主体

```json
{
  "emotion_type": "anxiety",
  "emotion_label": "焦虑",
  "emoji": "😰",
  "intensity": 7,
  "content": "临近考试时很紧张",
  "triggers": ["考试"],
  "body_parts": {"head": true, "chest": true},
  "selected_images": ["_3002"],
  "diary_date": "2026-07-14"
}
```

`emotion` / `emotionLabel` 是对前端 camelCase 的兼容别名；服务端响应也提供兼容字段。情绪类型可用 `joy`、`calm`、`sadness`、`anxiety`、`anger`、`fear`，强度范围为 0–10。

### 图片分析请求主体

```json
{
  "selectedImages": [{"imageId": "_3002"}, {"imageId": "_3011"}],
  "intensity": 7
}
```

响应包含 `emotion`（`emotionType`、`emotionLabel`、`emoji`、`confidence`）和平均 `vad`。该接口没有用户鉴权，不会写日记或会话。

## 4. DBT 技能 API

| 方法 | 路径 | 认证 | 查询/路径参数 | 说明 |
| --- | --- | --- | --- | --- |
| GET | `/api/dbt/skills` | 否 | `category?` | 返回全部或某分类的内置 DBT 技能。 |
| GET | `/api/dbt/skills/{skill_name}` | 否 | 技能名称 | 返回技能详细内容和步骤；不存在返回 404。 |
| GET | `/api/dbt/categories` | 否 | — | 四类技能及数量：痛苦耐受、正念、情绪调节、人际效能。 |

技能库来自进程内 `app/dbt/skills.py`，因此这些接口是内容查询接口，不需要数据库。

## 5. 对话 API 与 UI 状态协议

| 方法 | 路径 | 认证 | 说明 |
| --- | --- | --- | --- |
| POST | `/api/chat/message` | 用户 | 默认对话端点，使用 LangGraph。 |
| POST | `/api/chat/message/multi-agent` | 用户 | 兼容的顺序式多 Agent 端点，不建议新客户端使用。 |
| POST | `/api/chat/message/stream` | 用户 | 返回 SSE 形式的图节点消息；当前实现不保存完整消息历史。 |
| GET | `/api/chat/history` | 用户 | `session_id?`、`limit=1..100`；不传 session 时取最新会话。 |
| GET | `/api/chat/sessions` | 用户 | `page`、`page_size=1..100`；返回当前用户会话列表。 |

### 默认消息请求与响应

```json
{
  "message": "我明天要答辩，感觉很慌",
  "session_id": "可选 UUID；缺省则创建会话",
  "message_type": "text",
  "metadata": null
}
```

```json
{
  "reply": "……",
  "session_id": "UUID",
  "message_id": 123,
  "requires_input": {
    "type": "skill_confirmation",
    "prompt": "你是否愿意尝试这个技能练习？",
    "options": ["愿意", "再想想"],
    "skill_name": "正念呼吸"
  }
}
```

`message` 长度为 1–500。`message_type` 取值和结构化 metadata 如下；客户端应根据上一条响应的 `requires_input.type` 发送对应类型。

| `message_type` | 使用场景 | metadata 示例 |
| --- | --- | --- |
| `text` | 自由输入 | 可省略。 |
| `image_selection` | 选择情绪图片 | `{"emotion_type":"anxiety","image_urls":["/static/..."]}`。 |
| `intensity_rating` | 当前/练习后强度 | `{"value":7}` 或 `{"intensity":7}`。 |
| `body_selection` | 身体感受 | `{"selected_parts":["chest","abdomen"]}`。 |
| `skill_confirmation` | 同意/拒绝练习 | `{"choice":"愿意"}`。 |
| `step_completion` | 完成当前步骤 | metadata 可省略。 |

`requires_input.type` 的可选值包括 `emotion_images`、`intensity_slider`、`body_selector`、`skill_confirmation`、`step_completion` 与 `general`。其中 `emotion_images` 还可能来自“连续五条文本后”的独立评估引导分支；客户端完成选择后应带回 `image_selection` 数据。

## 6. 管理后台 API

| 方法 | 路径 | 权限 | 查询 / 主体 | 说明 |
| --- | --- | --- | --- | --- |
| POST | `/api/admin/login` | 否 | `username`、`password`、`remember?` | 管理员登录，返回管理员 token。 |
| POST | `/api/admin/logout` | 管理员 | — | 退出确认。 |
| GET | `/api/admin/info` | 管理员 | — | 当前管理员资料。 |
| GET | `/api/admin/statistics/overview` | 管理员 | — | 用户、管理员、日记、活跃用户与待处理危机概览。 |
| GET | `/api/admin/statistics/emotions` | 管理员 | `period=week|month|year` | 全局日记情绪分布。 |
| GET | `/api/admin/statistics/user-activity` | 管理员 | `period=week|month` | 每日活跃用户统计。 |
| GET | `/api/admin/users` | 管理员 | `keyword?`、`status?`、`page`、`page_size` | 用户检索及风险等级概览。 |
| GET | `/api/admin/users/{user_id}` | 管理员 | 路径 ID | 用户详情。 |
| PUT | `/api/admin/users/{user_id}/status` | 管理员 | `{"status":"active|inactive|suspended","reason":"可选"}` | 更改账户状态。 |
| DELETE | `/api/admin/users/{user_id}` | 超级管理员 | 路径 ID | 删除用户及关联数据，不可逆。 |
| GET | `/api/admin/crisis/recent` | 管理员 | `limit=10`、`status?` | 最近危机事件列表。 |

## 7. 客户端集成建议

1. 登录后只存储短生命周期 token，并为用户端和后台端分别维护认证头；遇到 401 清理本地会话，403 展示禁用/权限提示。
2. 对话页将 `session_id` 保存在当前会话上下文；不要把它当作跨用户可访问资源。服务端当前读取会话时未在所有端点显式校验 session 所属用户，客户端不应依赖这一缺口。
3. 对话 UI 以 `requires_input` 驱动控件，而不是从回复文案推断阶段；组件提交后继续使用同一个 `session_id`。
4. 统一错误处理时先读取 HTTP 状态，再安全解析 `detail.message` 或字符串 `detail`；不要假设响应外层永远有 `code`。
5. 上线前使用真实环境的 `/docs` 导出 OpenAPI 契约，并将本文件作为架构说明而不是自动生成的精确 schema 替代品。

## 8. 关联源码

- 路由装配：[main.py](/Users/zeno/program/EmotionalAssistant/backend/app/main.py)
- 对话契约：[chat.py](/Users/zeno/program/EmotionalAssistant/backend/app/models/chat.py)
- 对话路由：[chat.py](/Users/zeno/program/EmotionalAssistant/backend/app/api/chat.py)
- 认证依赖：[dependencies.py](/Users/zeno/program/EmotionalAssistant/backend/app/core/dependencies.py)
