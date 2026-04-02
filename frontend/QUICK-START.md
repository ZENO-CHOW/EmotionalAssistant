# 🚀 快速启动指南

## ✅ 已完成的工作

### 1. Vue项目基础搭建
- ✅ Vue 3 + Vite 配置完成
- ✅ Axios HTTP客户端已安装
- ✅ 端口已改为 8080 (避免冲突)
- ✅ 代理配置完成 (前端8080 → 后端3000)

### 2. 完整的规划文档
- ✅ `PROJECT-STRUCTURE.md` - 项目完整架构
- ✅ `src/api/interfaces.md` - **API接口文档（重要！）**
- ✅ `EMOTION-IMAGE-SYSTEM.md` - 情绪图片系统设计

---

## 📂 当前项目结构

```
frontend/
├── src/
│   ├── api/
│   │   ├── index.js           ✅ axios基础配置
│   │   └── interfaces.md      ✅ 接口文档（重要！）
│   ├── assets/
│   │   └── styles/
│   │       └── global.css     ✅ 全局样式
│   ├── components/            待开发
│   ├── pages/                 待开发
│   ├── utils/                 待开发
│   ├── App.vue                ✅ 临时欢迎页
│   └── main.js                ✅ 入口文件
├── PROJECT-STRUCTURE.md       ✅ 架构文档
├── EMOTION-IMAGE-SYSTEM.md    ✅ 情绪系统设计
└── QUICK-START.md             ✅ 本文档
```

---

## 🎯 核心功能模块

### 用户端（4个主要页面）
1. **登录注册页** - 用户入口
2. **对话窗口** - 核心功能
   - 情绪图片选择（IAPS/GAPED）
   - 情绪强度滑块
   - AI对话式DBT技能引导
   - 危机干预全屏弹窗
3. **情绪日记** - 记录与回顾
4. **个人信息** - 历史数据与成就

### 管理员端（4个主要功能）
1. **用户管理** - 用户列表与详情
2. **危机监控** - 实时危机事件，人工介入
3. **数据统计** - 可视化仪表盘
4. **系统配置** - 技能库、图片库、热线管理

---

## 🔌 API接口概览

详细文档见 `src/api/interfaces.md`，核心接口：

### 用户端
| 功能 | 接口 | 优先级 |
|------|------|--------|
| 登录注册 | POST /auth/login<br>POST /auth/register | P0 |
| 情绪图片 | GET /emotion/images<br>POST /emotion/analyze | P0 |
| 对话 | POST /chat/message<br>POST /chat/dbt-guidance | P0 |
| 危机干预 | GET /crisis/resources<br>POST /crisis/log | P0 |
| 日记 | POST /diary/create<br>GET /diary/list | P1 |
| 个人信息 | GET /user/profile<br>GET /user/skill-records | P1 |

### 管理员端
| 功能 | 接口 | 优先级 |
|------|------|--------|
| 用户管理 | GET /admin/users | P2 |
| 危机监控 | GET /admin/crisis-events<br>POST /admin/crisis-events/:id/handle | P2 |
| 数据统计 | GET /admin/statistics | P2 |
| 对话日志 | GET /admin/chat-logs/:userId | P3 |

**优先级**:
- P0: 核心功能，必须优先
- P1: 重要功能
- P2: 管理功能
- P3: 辅助功能

---

## 🎨 情绪图片选择系统

### 核心流程
```
用户进入
  ↓
展示情绪图片（IAPS/GAPED，8张宫格）
  ↓
用户选择1-3张最符合感受的图片
  ↓
拖动滑块标记情绪强度（1-10）
  ↓
提交后端分析（VAD值映射）
  ↓
返回情绪类型 + 置信度
  ↓
AI根据结果个性化对话
```

### 为什么用图片？
- **隐性评估**: 降低用户防御心理
- **更准确**: 比直接问"你焦虑吗"更真实
- **科学依据**: IAPS/GAPED是国际标准情感图片库

详细设计见 `EMOTION-IMAGE-SYSTEM.md`

---

## 🚦 开发优先级

### Phase 1: 基础框架（1周）
- [ ] 安装路由（Vue Router）
- [ ] 创建页面骨架
- [ ] 封装API模块
- [ ] 开发公共组件（按钮、输入框、加载动画等）

### Phase 2: 用户端核心（2-3周）
- [ ] 登录注册
- [ ] 对话窗口
- [ ] 情绪图片选择器
- [ ] 情绪强度滑块
- [ ] DBT技能引导
- [ ] 危机干预弹窗

### Phase 3: 用户端辅助（1周）
- [ ] 情绪日记
- [ ] 个人信息

### Phase 4: 管理员端（1周）
- [ ] 管理员登录
- [ ] 用户管理
- [ ] 危机监控
- [ ] 数据统计

---

## 💻 开发命令

### 启动开发服务器
```bash
cd frontend
npm run dev
```
访问: http://localhost:8080

### 构建生产版本
```bash
npm run build
```

### 预览生产版本
```bash
npm run preview
```

---

## 📝 开发注意事项

### 1. 接口调用
所有接口调用都通过 `src/api/` 封装，不要直接用axios
```javascript
// ❌ 错误
axios.post('/api/chat', data)

// ✅ 正确
import api from '@/api/chat'
api.sendMessage(data)
```

### 2. 扩展性设计
避免硬编码，使用配置文件
```javascript
// ❌ 错误
const emotions = ['焦虑', '开心', '平静']

// ✅ 正确
import { EMOTION_TYPES } from '@/utils/constants'
```

### 3. 组件复用
相似功能抽取为组件
```javascript
// 情绪卡片在多处使用，应该是独立组件
<EmotionCard type="anxiety" intensity="7" />
```

### 4. 错误处理
统一错误处理机制
```javascript
try {
  await api.sendMessage(message)
} catch (error) {
  showErrorToast(error.message)
}
```

---

## 🔐 环境变量

创建 `.env.development` 和 `.env.production`

```bash
# .env.development
VITE_API_BASE_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000/ws

# .env.production
VITE_API_BASE_URL=https://your-domain.com/api
VITE_WS_URL=wss://your-domain.com/ws
```

使用:
```javascript
const baseURL = import.meta.env.VITE_API_BASE_URL
```

---

## 📚 学习资源

### Vue 3 官方文档
- https://cn.vuejs.org/

### Vite 文档
- https://cn.vitejs.dev/

### 情绪识别相关论文
- IAPS: International Affective Picture System
- GAPED: Geneva Affective Picture Database

---

## 🤝 协作流程

### 前后端对接
1. 查看 `src/api/interfaces.md` 确认接口定义
2. 后端实现接口
3. 前端调用并测试
4. 发现问题及时沟通调整

### Git分支策略（建议）
```
main         - 生产环境
develop      - 开发环境
feature/xxx  - 功能分支
bugfix/xxx   - 修复分支
```

---

## ❓ 常见问题

### Q1: 接口还没有，怎么开发？
A: 使用Mock数据
```javascript
// 临时Mock
const mockResponse = {
  success: true,
  data: { ... }
}
```

### Q2: 图片资源从哪里来？
A: IAPS/GAPED需要申请授权，开发阶段可以用占位图

### Q3: 如何调试API？
A:
1. 使用浏览器开发者工具的Network面板
2. 使用Postman测试接口
3. 查看后端日志

---

## 📞 联系与支持

遇到问题请查看:
1. 本文档 `QUICK-START.md`
2. 项目架构 `PROJECT-STRUCTURE.md`
3. 接口文档 `src/api/interfaces.md`
4. 情绪系统设计 `EMOTION-IMAGE-SYSTEM.md`

---

## 🎉 下一步

现在你需要确认:
1. ✅ 项目架构是否符合预期？
2. ✅ API接口设计是否完整？
3. ✅ 情绪图片系统是否符合需求？
4. 🚀 从哪个模块开始开发？

**建议**: 从对话窗口开始，因为这是核心功能！
