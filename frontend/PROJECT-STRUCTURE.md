# 前端项目完整架构

## 📁 目录结构

```
frontend/
├── src/
│   ├── api/                    # API接口封装
│   │   ├── index.js           # axios配置
│   │   ├── user.js            # 用户相关接口
│   │   ├── chat.js            # 对话相关接口
│   │   ├── diary.js           # 日记相关接口
│   │   ├── emotion.js         # 情绪识别接口
│   │   ├── admin.js           # 管理员接口
│   │   └── interfaces.md      # **接口文档（重要）**
│   │
│   ├── assets/                # 静态资源
│   │   ├── styles/           # 样式文件
│   │   │   ├── global.css    # 全局样式
│   │   │   ├── variables.css # CSS变量
│   │   │   └── animations.css # 动画效果
│   │   ├── images/           # 图片资源
│   │   │   ├── iaps/         # IAPS图片库
│   │   │   ├── gaped/        # GAPED图片库
│   │   │   └── icons/        # 图标
│   │   └── data/             # 静态数据
│   │       ├── emotions.json  # 情绪类型配置
│   │       └── dbt-skills.json # DBT技能配置
│   │
│   ├── components/            # 可复用组件
│   │   ├── common/           # 公共组件
│   │   │   ├── NavBar.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   ├── Modal.vue
│   │   │   ├── Button.vue
│   │   │   └── Slider.vue
│   │   │
│   │   ├── chat/             # 对话相关组件
│   │   │   ├── ChatBox.vue
│   │   │   ├── MessageItem.vue
│   │   │   ├── MessageInput.vue
│   │   │   ├── DBTGuidance.vue      # DBT技能引导
│   │   │   ├── CrisisModal.vue      # 危机干预弹窗
│   │   │   └── HotlineCard.vue
│   │   │
│   │   ├── emotion/          # 情绪相关组件
│   │   │   ├── EmotionImageSelector.vue  # IAPS/GAPED图片选择器
│   │   │   ├── EmotionIntensitySlider.vue # 情绪强度滑块
│   │   │   ├── EmotionResult.vue    # 情绪识别结果展示
│   │   │   └── ImageGallery.vue     # 图片画廊
│   │   │
│   │   ├── diary/            # 日记相关组件
│   │   │   ├── DiaryForm.vue
│   │   │   ├── DiaryList.vue
│   │   │   ├── DiaryCard.vue
│   │   │   └── DiaryDetail.vue
│   │   │
│   │   ├── profile/          # 个人信息组件
│   │   │   ├── ProfileHeader.vue
│   │   │   ├── ChatHistory.vue
│   │   │   ├── SkillRecord.vue
│   │   │   └── BadgeDisplay.vue
│   │   │
│   │   └── admin/            # 管理员组件
│   │       ├── UserManagement.vue
│   │       ├── CrisisMonitor.vue      # 危机事件监控
│   │       ├── ChatLogViewer.vue      # 对话记录查看
│   │       ├── DataStatistics.vue     # 数据统计
│   │       └── SystemConfig.vue       # 系统配置
│   │
│   ├── pages/                # 页面组件
│   │   ├── user/            # 用户端页面
│   │   │   ├── LoginPage.vue
│   │   │   ├── RegisterPage.vue
│   │   │   ├── HomePage.vue           # 主页（含3个tab）
│   │   │   ├── ChatTab.vue           # 对话窗口tab
│   │   │   ├── DiaryTab.vue          # 情绪日记tab
│   │   │   └── ProfileTab.vue        # 个人信息tab
│   │   │
│   │   └── admin/           # 管理员端页面
│   │       ├── AdminLogin.vue
│   │       ├── AdminDashboard.vue     # 管理员仪表盘
│   │       ├── UserManagementPage.vue
│   │       ├── CrisisManagementPage.vue
│   │       └── SystemSettingsPage.vue
│   │
│   ├── router/              # 路由配置
│   │   └── index.js
│   │
│   ├── store/               # Vuex状态管理（如需要）
│   │   ├── index.js
│   │   ├── modules/
│   │   │   ├── user.js
│   │   │   ├── chat.js
│   │   │   └── admin.js
│   │
│   ├── utils/               # 工具函数
│   │   ├── auth.js          # 认证工具
│   │   ├── storage.js       # 本地存储
│   │   ├── validators.js    # 表单验证
│   │   ├── emotion-analyzer.js # 情绪分析辅助
│   │   └── constants.js     # 常量定义
│   │
│   ├── App.vue
│   └── main.js
│
├── public/                  # 公共资源
│   └── index.html
│
├── .env.development         # 开发环境变量
├── .env.production          # 生产环境变量
├── vite.config.js
├── package.json
└── PROJECT-STRUCTURE.md     # 本文档
```

## 🎯 核心功能模块

### 用户端（User Portal）
1. **登录注册模块**
   - 用户登录/注册
   - 找回密码
   - 自动登录

2. **对话窗口模块**
   - 实时对话
   - 情绪图片选择（IAPS/GAPED）
   - 情绪强度评估
   - DBT技能AI引导
   - 危机干预（全屏弹窗）

3. **情绪日记模块**
   - 日记记录（情绪+强度+技能使用）
   - 历史日记查看
   - 情绪趋势可视化

4. **个人信息模块**
   - 对话历史
   - 技能训练记录
   - 成就徽章
   - 个人设置

### 管理员端（Admin Portal）
1. **用户管理**
   - 用户列表
   - 用户详情
   - 账号管理

2. **危机监控**
   - 实时危机事件列表
   - 危机等级标记
   - 人工介入接口

3. **数据统计**
   - 用户活跃度
   - 情绪分布统计
   - DBT技能使用统计
   - 危机事件统计

4. **系统配置**
   - DBT技能库管理
   - 情绪图片库管理
   - 热线信息管理
   - 敏感词配置

## 🔌 数据流设计

### 用户端数据流
```
用户操作 → Vue组件 → API调用 → 后端处理 → 返回数据 → 更新UI
```

### 管理员端数据流
```
管理员操作 → 管理组件 → Admin API → 后端处理 → WebSocket推送更新
```

## 🎨 设计规范

### 用户端
- 森林绿主题（温暖、治愈）
- 液态玻璃效果
- 圆角卡片设计
- 流畅动画过渡

### 管理员端
- 专业深色主题
- 数据可视化图表
- 表格列表为主
- 响应式布局

## 📝 开发优先级

### Phase 1: 基础框架（第1周）
- [x] Vue项目搭建
- [ ] 路由配置
- [ ] API接口封装
- [ ] 公共组件库

### Phase 2: 用户端核心功能（第2-3周）
- [ ] 登录注册
- [ ] 对话窗口
- [ ] 情绪图片选择系统
- [ ] DBT技能引导

### Phase 3: 用户端辅助功能（第4周）
- [ ] 情绪日记
- [ ] 个人信息
- [ ] 危机干预

### Phase 4: 管理员端（第5周）
- [ ] 管理员登录
- [ ] 用户管理
- [ ] 危机监控
- [ ] 数据统计

## 🔐 权限设计

### 路由守卫
```javascript
用户端路由: 需要登录token
管理员路由: 需要admin token
```

### 接口权限
- 用户接口: Authorization: Bearer {userToken}
- 管理员接口: Authorization: Bearer {adminToken}
