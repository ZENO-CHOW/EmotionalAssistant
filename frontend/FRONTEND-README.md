# 前端项目说明

## 📁 项目结构

```
frontend/
├── src/
│   ├── api/              # API接口封装
│   │   └── index.js      # axios配置和API方法
│   ├── assets/           # 静态资源
│   │   └── styles/       # 样式文件
│   │       └── global.css # 全局样式
│   ├── components/       # 可复用组件（等待开发）
│   ├── pages/           # 页面组件（等待开发）
│   ├── utils/           # 工具函数（等待开发）
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── vite.config.js       # Vite配置
└── package.json         # 依赖配置
```

## 🚀 快速开始

### 启动开发服务器
```bash
npm run dev
```
访问: http://localhost:5173

### 构建生产版本
```bash
npm run build
```

### 预览生产版本
```bash
npm run preview
```

## 📦 已安装依赖

- **Vue 3** - 前端框架
- **Vite** - 构建工具
- **Axios** - HTTP客户端

## ⚙️ 配置说明

### Vite代理配置
已配置 `/api` 代理到后端服务器 `http://localhost:3000`

### API使用方法
```javascript
import api from '@/api'

// 发送消息
const response = await api.sendMessage('我很焦虑')

// 清除历史
await api.clearHistory()
```

## 🎨 设计系统

### 主题色
- 主色: `#2E7D32` (森林绿)
- 浅色: `#4CAF50`
- 更浅: `#81C784`
- 背景: `#E8F5E9`

### 设计效果
- 液态玻璃风格
- 森林绿渐变背景
- 圆角卡片设计

## 📝 下一步

1. 等待用户上传流程图
2. 根据流程图规划组件
3. 开发各个功能模块
