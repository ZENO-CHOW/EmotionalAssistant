# 🌱 小安 - 大学生情绪管理助手

基于 DeepSeek API 的 DBT 情绪急救系统 MVP

## 快速开始

### 1. 配置环境变量

复制环境变量模板并配置：

```bash
cd backend
cp .env.example .env
编辑 `.env` 文件，填入必要的配置：
```

**主要配置项**：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | SQLite 数据库地址 | `sqlite:///./data/emotions.db` |
| `LLM_API_KEY` | DeepSeek API 密钥 | - |
| `LLM_BASE_URL` | DeepSeek API 地址 | `https://api.deepseek.com` |
| `LLM_MODEL` | DeepSeek 模型名称 | `deepseek-chat` |
| `VISION_API_KEY` | 视觉模型 API 密钥 | - |
| `VISION_BASE_URL` | 视觉模型 API 地址 | `https://api.siliconflow.cn/v1` |
| `VISION_MODEL` | 视觉模型名称 | `Qwen/Qwen3-VL-30B-A3B-Instruct` |

### 2. 安装依赖

**前端依赖**:
```bash
cd frontend && npm install
```

**后端依赖**:
```bash
cd backend && pip install -r requirements.txt
```

### 3. 启动服务

**启动后端服务器**:
```bash
cd backend && python start_backend.py
```
后端将在 http://localhost:8000 启动

**启动前端开发服务器** (新终端):
```bash
cd frontend && npm run dev
```
前端将在 http://localhost:8080 启动

### 4. 打开网页

在浏览器中访问：
- 用户端：http://localhost:8080
- 管理员端：http://localhost:8080/admin

**管理员账号**：
账户:admin
密码:admin123

## 项目结构

```
.
├── frontend/              # Vue.js 前端项目
│   ├── src/              # 前端源码
│   ├── index.html        # 入口 HTML
│   ├── package.json      # 前端依赖
│   └── vite.config.js    # Vite 配置
├── backend/               # Python FastAPI 后端
│   ├── app/              # 后端应用源码
│   ├── .env              # 环境变量配置
│   ├── requirements.txt  # Python 依赖
│   └── start_backend.py  # 后端启动脚本
└── README.md             # 说明文档
```

## 技术栈

- **前端**: Vue.js 3 + Vite
- **后端**: Python + FastAPI
- **数据库**: SQLite
- **AI**: DeepSeek API
- **设计**: 液态玻璃 + 森林绿主题

## 功能特性

### 已完成
- ✅ 实时对话（接入 DeepSeek）
- ✅ 情绪快捷选择（焦虑/悲伤/愤怒/空虚）
- ✅ 对话历史记录（内存存储）
- ✅ 日记展示（静态示例）
- ✅ 个人中心（静态示例）
- ✅ 数据库持久化
- ✅ 用户登录系统
- ✅ 真实日记记录
- ✅ 情绪数据统计

### 待开发
- ⏳ 危机识别与转介

## API 接口

### POST /api/chat
发送消息给小安

**请求**:
```json
{
  "message": "我很焦虑",
  "userId": "default"  // 可选
}
```

**响应**:
```json
{
  "message": "听起来你现在很难受...",
  "success": true
}
```

### POST /api/clear
清除对话历史

**请求**:
```json
{
  "userId": "default"
}
```

### GET /api/health
健康检查

## 开发说明

### 开发模式（自动重启）

```bash
npm run dev
```

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DEEPSEEK_API_KEY | DeepSeek API密钥 | - |
| DEEPSEEK_API_URL | API地址 | https://api.deepseek.com/v1/chat/completions |
| DEEPSEEK_MODEL | 模型名称 | deepseek-chat |

## 小安的人设

- **身份**: 专门帮助大学生应对情绪困扰的AI助手
- **风格**: 口语化、温暖、像朋友
- **方法**: 基于DBT（辩证行为疗法）
- **原则**: 共情优先、给选择权、承认局限

## 注意事项

⚠️ **不要用于真实的心理危机**：
- 无法替代专业心理咨询
- 遇到危机请拨打专业热线

## License

MIT
