# FastAPI 后端架构文档

## 1. 项目结构

```
EmotionalAssistant/
├── main.py                          # 遗留原型（未使用）
└── backend/
    ├── start_backend.py             # uvicorn 启动入口
    ├── .env / .env.example          # 环境变量配置
    ├── requirements.txt             # Python 依赖
    ├── static/                      # 静态文件（CAPS 情绪图片）
    └── app/
        ├── __init__.py              # 版本号 "1.0.0"
        ├── main.py                  # FastAPI 应用入口 ★
        ├── config.py                # Pydantic Settings 配置管理
        ├── api/                     # 路由层
        │   ├── auth.py              #   用户认证
        │   ├── admin.py             #   管理员后台
        │   ├── chat.py              #   对话（LangGraph）
        │   ├── diary.py             #   情绪日记
        │   ├── dbt.py               #   DBT 技能
        │   └── emotion.py           #   情绪图片识别
        ├── core/                    # 核心模块
        │   ├── auth.py              #   JWT + bcrypt 工具
        │   ├── dependencies.py      #   FastAPI Depends 认证依赖
        │   ├── llm_client.py        #   LLM 客户端
        │   ├── emotion_recognizer.py
        │   ├── crisis_detector.py
        │   ├── skill_recommender.py
        │   ├── evaluator.py
        │   └── vision_client.py
        ├── database/                # 数据层
        │   ├── connection.py        #   SQLAlchemy 引擎 + get_db 生成器
        │   ├── models.py            #   ORM 模型（7 张表）
        │   ├── repositories/        #   仓库层
        │   └── migrations/
        ├── models/                  # Pydantic 请求/响应模型
        │   ├── chat.py
        │   └── diary.py
        ├── agent/                   # LangGraph 多智能体
        │   ├── coordinator.py
        │   ├── state.py
        │   ├── langgraph_builder.py
        │   └── ...
        ├── middleware/
        │   └── exceptions.py        # 全局异常处理器
        ├── dbt/
        │   └── skills.py            # DBT 技能定义
        └── utils/
            └── image_utils.py
```

---

## 2. 应用入口

### 2.1 创建 FastAPI 实例

文件：`backend/app/main.py`

```python
app = FastAPI(
    title="大学生情绪管理系统 API",
    description="基于DBT疗法的情绪管理辅助系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
```

- 自动生成 Swagger UI（`/docs`）和 ReDoc（`/redoc`）
- 版本号从 `app/__init__.py` 获取

### 2.2 启动方式

文件：`backend/start_backend.py`

```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

或直接在 `app/main.py` 末尾：

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000, reload=True)
```

### 2.3 生命周期事件

```python
@app.on_event("startup")
async def startup_event():
    init_db()          # 创建表 + 数据目录
    create_admin_account()  # 自动创建默认管理员

@app.on_event("shutdown")
async def shutdown_event():
    # 清理资源
```

### 2.4 根路径端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 返回应用名称、版本、运行状态 |
| GET | `/health` | 健康检查，返回 `{"status": "healthy"}` |

---

## 3. 路由层

### 3.1 路由注册

所有路由器在 `app/main.py` 末尾集中注册：

```python
from app.api import diary, chat, dbt, emotion, auth, admin

app.include_router(diary.router,   prefix="/api", tags=["情绪日记"])
app.include_router(chat.router,    prefix="/api", tags=["对话"])
app.include_router(dbt.router,     prefix="/api", tags=["DBT技能"])
app.include_router(emotion.router, prefix="/api", tags=["情绪识别"])
app.include_router(auth.router,    prefix="/api", tags=["用户认证"])
app.include_router(admin.router,   prefix="/api", tags=["管理员"])
```

- 每个路由文件内部创建 `router = APIRouter()`
- 统一前缀 `/api`，无嵌套

### 3.2 路由详情

#### auth.py — 用户认证

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/auth/login` | 无 | 用户名/邮箱 + 密码登录 |
| POST | `/api/auth/register` | 无 | 注册新用户 |
| GET | `/api/auth/user` | User | 获取当前用户信息 |
| PUT | `/api/auth/user` | User | 更新个人信息 |
| POST | `/api/auth/change-password` | User | 修改密码 |
| POST | `/api/auth/logout` | User | 退出登录 |

#### chat.py — 对话

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/chat/message` | User | 发送消息（LangGraph 单会话引擎） |
| POST | `/api/chat/message/multi-agent` | User | 发送消息（多智能体协调模式） |
| POST | `/api/chat/message/stream` | User | 流式对话（SSE） |
| GET | `/api/chat/history` | User | 获取当前会话历史 |
| GET | `/api/chat/sessions` | User | 获取所有会话列表 |

#### diary.py — 情绪日记

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/diary` | User | 创建日记 |
| GET | `/api/diary/list` | User | 日记列表（分页） |
| GET | `/api/diary/{id}` | User | 日记详情 |
| PUT | `/api/diary/{id}` | User | 更新日记 |
| DELETE | `/api/diary/{id}` | User | 删除日记 |
| GET | `/api/diary/today` | User | 今日日记 |
| GET | `/api/emotion/statistics` | User | 情绪统计 |
| GET | `/api/emotion/trend` | User | 情绪趋势 |

#### dbt.py — DBT 技能

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | `/api/dbt/skills` | User | 所有 DBT 技能列表 |
| GET | `/api/dbt/skills/{name}` | User | 技能详情 |
| GET | `/api/dbt/categories` | User | 技能分类列表 |

#### emotion.py — 情绪图片识别

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | `/api/emotion/images` | User | 获取 CAPS 情绪图片库 |
| POST | `/api/emotion/analyze` | User | 上传图片分析情绪 |
| GET | `/api/emotion/images/statistics` | User | 图片使用统计 |

#### admin.py — 管理员后台

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/admin/login` | 无 | 管理员登录 |
| POST | `/api/admin/logout` | Admin | 管理员退出 |
| GET | `/api/admin/info` | Admin | 管理员信息 |
| GET | `/api/admin/statistics/overview` | Admin | 系统概览统计 |
| GET | `/api/admin/statistics/emotions` | Admin | 情绪数据统计 |
| GET | `/api/admin/statistics/user-activity` | Admin | 用户活跃度统计 |
| GET | `/api/admin/users` | Admin | 用户列表 |
| GET | `/api/admin/users/{id}` | Admin | 用户详情 |
| PUT | `/api/admin/users/{id}/status` | Admin | 修改用户状态 |
| DELETE | `/api/admin/users/{id}` | SuperAdmin | 删除用户 |
| GET | `/api/admin/crisis/recent` | Admin | 近期危机事件 |

### 3.3 静态文件挂载

```python
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
```

用于提供 CAPS 情绪图片库的静态资源访问。

---

## 4. 中间件

### 4.1 CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

当前允许所有来源，生产部署时应改为具体前端域名。

### 4.2 全局异常处理

文件：`backend/app/middleware/exceptions.py`

通过 `register_exception_handlers(app)` 注册 4 层异常处理器：

| 异常类型 | HTTP 状态码 | 响应格式 |
|----------|------------|---------|
| `BusinessException` | 可变（code 字段） | `{code, message, details}` |
| `RequestValidationError` | 422 | `{code: 422, message, details: [{field, message, type}]}` |
| `SQLAlchemyError` | 500 | `{code: 500, message: "数据库操作失败"}` |
| `Exception`（兜底） | 500 | `{code: 500, message: "服务器内部错误"}` |

自定义异常类继承体系：

```
BusinessException (基类, code + message + details)
├── DatabaseException   (code=500)
├── ValidationException (code=400)
├── NotFoundException   (code=404)
└── ConflictException   (code=409)
```

所有异常响应统一为 `{code: int, message: str, details: any}` 的 JSON 结构。

---

## 5. 依赖注入

### 5.1 数据库会话

文件：`backend/app/database/connection.py`

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

使用方式：

```python
@router.get("/some-path")
async def handler(db: Session = Depends(get_db)):
    ...
```

- SQLAlchemy + SQLite，`check_same_thread=False` 允许多线程访问
- 连接池大小由 `MAX_DB_CONNECTIONS` 配置（默认 10）
- `init_db()` 在启动时自动创建所有表

### 5.2 认证依赖链

文件：`backend/app/core/dependencies.py`

```
                    HTTPBearer + Header("Authorization")
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
    get_current_user_id    get_current_user      (管理员专用)
    返回 int user_id       查库 + 验状态           │
                          返回 User ORM 对象  ┌────┴────┐
                                             ▼         ▼
                                   get_current_admin_id  get_current_admin
                                   返回 int admin_id     查库 + 验状态
                                                        返回 Admin ORM 对象
                                                              │
                                                        require_super_admin
                                                        验 role == "super_admin"
```

**用户认证两个层级：**

| 依赖函数 | 返回类型 | 校验内容 |
|----------|---------|---------|
| `get_current_user_id` | `int` | 仅验证 JWT 有效性，不查库 |
| `get_current_user` | `User` (ORM) | JWT + 查库 + 验状态为 active |

**管理员认证三个层级：**

| 依赖函数 | 返回类型 | 校验内容 |
|----------|---------|---------|
| `get_current_admin_id` | `int` | 仅验证 JWT，优先读 Admin-Authorization 头 |
| `get_current_admin` | `Admin` (ORM) | JWT + 查库 + 验状态 |
| `require_super_admin` | `Admin` (ORM) | 继承上者 + 验 role == "super_admin" |

使用示例：

```python
# 只需用户 ID
@router.get("/data")
async def get_data(user_id: int = Depends(get_current_user_id)):
    ...

# 需要完整用户对象
@router.put("/profile")
async def update_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    ...

# 超级管理员
@router.delete("/users/{id}")
async def delete_user(
    user_id: int,
    current_admin = Depends(require_super_admin),
):
    ...
```

---

## 6. 认证模块

文件：`backend/app/core/auth.py`

使用 `AuthTools` 类（模块级单例 `auth_tools`）：

| 方法 | 用途 |
|------|------|
| `hash_password(pw)` | bcrypt 哈希密码 |
| `verify_password(plain, hashed)` | bcrypt 验证明文 vs 哈希 |
| `create_user_token(user_id, username)` | 生成用户 JWT，payload 含 `{sub, username, type:"user"}` |
| `create_admin_token(admin_id, username, role)` | 生成管理员 JWT，payload 含 `{sub, username, role, type:"admin"}` |
| `extract_user_id_from_token(token)` | 解码并验 `type=="user"`，返回 user_id |
| `extract_admin_id_from_token(token)` | 解码并验 `type=="admin"`，返回 admin_id |

JWT 配置：
- 算法：HS256
- 过期时间：`ACCESS_TOKEN_EXPIRE_MINUTES`（默认 1440 分钟 = 24 小时）
- 密钥：`SECRET_KEY`（.env 中配置，生产环境务必修改）

---

## 7. 配置管理

文件：`backend/app/config.py`

使用 `pydantic_settings.BaseSettings`，通过 `@lru_cache()` 实现单例：

```python
settings = get_settings()  # 模块级单例，各处直接 import
```

关键配置项：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `DATABASE_URL` | `sqlite:///./data/emotions.db` | 数据库连接 |
| `SECRET_KEY` | `"your-secret-key-here-..."` | JWT 签名密钥 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token 过期时间（分钟） |
| `LLM_MODEL` | `ZhipuAI/GLM-4.7-Flash` | 大模型 |
| `LLM_BASE_URL` | `https://api-inference.modelscope.cn/v1` | LLM API 地址 |
| `VISION_MODEL` | `Qwen/Qwen3-VL-30B-A3B-Instruct` | 视觉模型 |
| `CRISIS_INTENSITY_THRESHOLD` | `9` | 危机检测强度阈值 |
| `LOG_LEVEL` | `INFO` | 日志级别 |

配置从 `backend/.env` 文件加载，`case_sensitive=True`。

---

## 8. 统一响应格式

所有 API 返回统一的 JSON 结构：

```json
{
    "code": 200,
    "message": "操作成功",
    "data": { ... }
}
```

- `code`：业务状态码（200 成功，400 参数错误，401 未认证，403 无权限，404 不存在，409 冲突，422 验证失败，500 服务端错误）
- `message`：人类可读的描述
- `data`：实际业务数据（可为 dict、list、null）

---

## 9. 对话系统架构

两条对话路径并行存在：

### 9.1 LangGraph 单会话引擎

`POST /api/chat/message`

6 节点状态图，使用 `MemorySaver` 检查点按 session_id 持久化：

```
用户消息 → 情绪识别 → 强度评估 → 身体感受 → 危机检测 → 技能推荐 → 指导输出
```

### 9.2 多智能体协调模式

`POST /api/chat/message/multi-agent`

```
Coordinator 协调器
  ├── RecognitionAgent    识别智能体
  ├── RecommendationAgent 推荐智能体
  └── InterventionAgent   干预智能体
```

### 9.3 流式输出

`POST /api/chat/message/stream`

使用 `astream` 异步生成器，SSE（Server-Sent Events）格式推流。

### 9.4 RequiresInputSchema

对话响应中包含 `RequiresInputSchema` 字段，指导前端渲染对应的交互组件：

- `intensity_slider` — 情绪强度滑块
- `skill_confirmation` — 技能确认
- `step_completion` — 步骤完成
- `emotion_images` — 情绪图片选择
- `body_selector` — 身体感受选区
- `image_upload` — 图片上传
- `general` / `text` — 普通文本输入

---

## 10. 数据模型

### 10.1 ORM 模型（SQLAlchemy）

7 张表：`User`, `ChatSession`, `ChatMessage`, `EmotionDiary`, `SkillUsageRecord`, `CrisisEvent`, `EmotionImage`, `Admin`

### 10.2 Pydantic 模型

用于请求验证和响应序列化，定义在各 `models/` 和 `api/` 文件中，使用 `Field` 添加校验规则（`min_length`, `max_length` 等）和 `field_validator` 做自定义校验。

---

## 11. 项目依赖关键词

- **Web 框架**：FastAPI, uvicorn
- **数据库**：SQLAlchemy, SQLite
- **认证**：python-jose (JWT), bcrypt
- **配置**：pydantic-settings
- **AI/对话**：LangGraph, openai (兼容 SDK)
- **日志**：Python logging 模块（文件 + 控制台）
