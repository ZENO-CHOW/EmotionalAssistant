# 大学生情绪管理系统 - API接口文档

## 目录

- [1. 用户认证 API](#1-用户认证-api)
- [2. 情绪识别和日记 API](#2-情绪识别和日记-api)
- [3. 管理员 API](#3-管理员-api)
- [4. 数据模型](#4-数据模型)
- [5. 错误码说明](#5-错误码说明)

---

## 基础信息

- **Base URL**: `http://localhost:3000/api`
- **认证方式**: Bearer Token (JWT)
- **请求格式**: JSON
- **响应格式**: JSON

### 通用响应格式

#### 成功响应
```json
{
  "code": 200,
  "message": "success",
  "data": { /* 响应数据 */ }
}
```

#### 错误响应
```json
{
  "code": 400,
  "message": "错误描述",
  "error": "详细错误信息"
}
```

---

## 1. 用户认证 API

### 1.1 用户登录

**接口**: `POST /api/auth/login`

**请求参数**:
```json
{
  "username": "string",  // 用户名或邮箱
  "password": "string"   // 密码
}
```

**响应数据**:
```json
{
  "token": "string",           // JWT访问令牌
  "refreshToken": "string",    // 刷新令牌
  "user": {
    "id": "string",
    "username": "string",
    "email": "string",
    "avatar": "string",
    "createdAt": "datetime"
  }
}
```

### 1.2 用户注册

**接口**: `POST /api/auth/register`

**请求参数**:
```json
{
  "username": "string",        // 用户名（必填）
  "email": "string",           // 邮箱（必填）
  "password": "string",        // 密码（必填，至少6位）
  "confirmPassword": "string", // 确认密码（必填）
  "phone": "string",           // 手机号（可选）
  "school": "string"           // 学校（可选）
}
```

**响应数据**:
```json
{
  "userId": "string",
  "message": "注册成功，请验证邮箱"
}
```

### 1.3 用户登出

**接口**: `POST /api/auth/logout`

**Headers**: `Authorization: Bearer {token}`

**响应数据**:
```json
{
  "message": "登出成功"
}
```

### 1.4 获取当前用户信息

**接口**: `GET /api/auth/user`

**Headers**: `Authorization: Bearer {token}`

**响应数据**:
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "phone": "string",
  "school": "string",
  "avatar": "string",
  "createdAt": "datetime",
  "lastLoginAt": "datetime"
}
```

### 1.5 更新用户信息

**接口**: `PUT /api/auth/user`

**Headers**: `Authorization: Bearer {token}`

**请求参数**:
```json
{
  "username": "string",   // 可选
  "email": "string",      // 可选
  "phone": "string",      // 可选
  "school": "string",     // 可选
  "avatar": "string"      // 可选
}
```

### 1.6 修改密码

**接口**: `POST /api/auth/change-password`

**Headers**: `Authorization: Bearer {token}`

**请求参数**:
```json
{
  "currentPassword": "string",  // 当前密码
  "newPassword": "string"       // 新密码
}
```

### 1.7 发送重置密码验证码

**接口**: `POST /api/auth/reset-password/send-code`

**请求参数**:
```json
{
  "email": "string"  // 邮箱地址
}
```

**响应数据**:
```json
{
  "message": "验证码已发送到邮箱",
  "expiresIn": 600  // 有效期（秒）
}
```

### 1.8 验证重置密码验证码

**接口**: `POST /api/auth/reset-password/verify-code`

**请求参数**:
```json
{
  "email": "string",  // 邮箱地址
  "code": "string"    // 6位验证码
}
```

**响应数据**:
```json
{
  "resetToken": "string",  // 重置令牌（有效期15分钟）
  "message": "验证成功"
}
```

### 1.9 重置密码

**接口**: `POST /api/auth/reset-password`

**请求参数**:
```json
{
  "resetToken": "string",    // 从验证码验证接口获取
  "newPassword": "string"    // 新密码
}
```

---

## 2. 情绪识别和日记 API

### 2.1 获取情绪图片列表

**接口**: `GET /api/emotion/images`

**Query参数**:
- `category` (可选): positive / negative / neutral
- `limit` (可选): 返回数量，默认12

**响应数据**:
```json
[
  {
    "id": "string",
    "url": "string",
    "category": "positive|negative|neutral",
    "valence": "number",   // 情绪效价 0-10
    "arousal": "number"    // 唤醒度 0-10
  }
]
```

### 2.2 分析情绪

**接口**: `POST /api/emotion/analyze`

**Headers**: `Authorization: Bearer {token}`

**请求参数**:
```json
{
  "selectedImages": [
    {
      "imageId": "string",
      "selectionTime": "number"  // 选择时间（毫秒）
    }
  ],
  "intensity": "number"  // 情绪强度 0-10
}
```

**响应数据**:
```json
{
  "emotionType": "joy|calm|sadness|anxiety|anger|fear",
  "emotionLabel": "string",       // 中文标签
  "confidence": "number",         // 置信度 0-1
  "intensity": "number",          // 强度 0-10
  "isCrisis": "boolean",          // 是否危机
  "recommendedSkills": ["string"], // 推荐的DBT技能
  "analysis": {
    "valenceScore": "number",
    "arousalScore": "number",
    "dominanceScore": "number"
  }
}
```

### 2.3 创建情绪日记

**接口**: `POST /api/diary`

**Headers**: `Authorization: Bearer {token}`

**请求参数**:
```json
{
  "emotion": "joy|calm|sadness|anxiety|anger|fear",
  "emotionLabel": "string",
  "emoji": "string",
  "intensity": "number",        // 0-10
  "content": "string",          // 日记内容
  "triggers": ["string"],       // 触发因素（可选）
  "bodyParts": {                // 身体部位感受（可选）
    "head": "boolean",
    "chest": "boolean",
    "stomach": "boolean",
    "limbs": "boolean"
  },
  "selectedImages": ["string"]  // 图片ID列表（可选）
}
```

**响应数据**:
```json
{
  "id": "string",
  "userId": "string",
  "emotion": "string",
  "intensity": "number",
  "content": "string",
  "createdAt": "datetime"
}
```

### 2.4 更新情绪日记

**接口**: `PUT /api/diary/:diaryId`

**Headers**: `Authorization: Bearer {token}`

**请求参数**: 同创建日记（所有字段可选）

### 2.5 删除情绪日记

**接口**: `DELETE /api/diary/:diaryId`

**Headers**: `Authorization: Bearer {token}`

### 2.6 获取日记列表

**接口**: `GET /api/diary/list`

**Headers**: `Authorization: Bearer {token}`

**Query参数**:
- `page` (可选): 页码，默认1
- `pageSize` (可选): 每页数量，默认20
- `startDate` (可选): 开始日期 YYYY-MM-DD
- `endDate` (可选): 结束日期 YYYY-MM-DD
- `emotion` (可选): 情绪类型筛选

**响应数据**:
```json
{
  "list": [
    {
      "id": "string",
      "emotion": "string",
      "emotionLabel": "string",
      "emoji": "string",
      "intensity": "number",
      "content": "string",
      "triggers": ["string"],
      "createdAt": "datetime"
    }
  ],
  "total": "number",
  "page": "number",
  "pageSize": "number"
}
```

### 2.7 获取日记详情

**接口**: `GET /api/diary/:diaryId`

**Headers**: `Authorization: Bearer {token}`

### 2.8 获取今日日记

**接口**: `GET /api/diary/today`

**Headers**: `Authorization: Bearer {token}`

### 2.9 获取情绪历史

**接口**: `GET /api/emotion/history`

**Headers**: `Authorization: Bearer {token}`

**Query参数**:
- `page`, `pageSize`: 分页参数
- `startDate`, `endDate`: 时间范围

### 2.10 获取情绪统计

**接口**: `GET /api/emotion/statistics`

**Headers**: `Authorization: Bearer {token}`

**Query参数**:
- `timeRange`: week | month | quarter | year

**响应数据**:
```json
{
  "totalRecords": "number",
  "emotionDistribution": {
    "joy": "number",
    "calm": "number",
    "sadness": "number",
    "anxiety": "number",
    "anger": "number",
    "fear": "number"
  },
  "averageIntensity": "number",
  "continuousDays": "number"
}
```

### 2.11 获取情绪趋势

**接口**: `GET /api/emotion/trend`

**Headers**: `Authorization: Bearer {token}`

**Query参数**:
- `days` (可选): 最近天数，默认30

**响应数据**:
```json
[
  {
    "date": "YYYY-MM-DD",
    "averageIntensity": "number",
    "recordCount": "number"
  }
]
```

### 2.12 导出日记数据

**接口**: `GET /api/diary/export`

**Headers**: `Authorization: Bearer {token}`

**Query参数**:
- `format`: csv | json | pdf
- `startDate`, `endDate`: 时间范围

**响应**: 文件下载（blob）

### 2.13 DBT技能相关接口

#### 获取DBT技能列表
**接口**: `GET /api/dbt/skills`

#### 获取学习进度
**接口**: `GET /api/dbt/progress`

**Headers**: `Authorization: Bearer {token}`

#### 更新学习进度
**接口**: `POST /api/dbt/progress`

**Headers**: `Authorization: Bearer {token}`

**请求参数**:
```json
{
  "skillId": "string",
  "progress": "number"  // 0-100
}
```

### 2.14 聊天对话接口

#### 发送消息
**接口**: `POST /api/chat/message`

**Headers**: `Authorization: Bearer {token}`

**请求参数**:
```json
{
  "message": "string",
  "sessionId": "string"  // 可选
}
```

**响应数据**:
```json
{
  "reply": "string",
  "sessionId": "string"
}
```

#### 获取聊天历史
**接口**: `GET /api/chat/history`

**Headers**: `Authorization: Bearer {token}`

**Query参数**:
- `sessionId` (可选)
- `limit` (可选): 返回数量

---

## 3. 管理员 API

### 3.1 管理员登录

**接口**: `POST /api/admin/login`

**请求参数**:
```json
{
  "username": "string",
  "password": "string",
  "remember": "boolean"  // 可选，是否记住登录7天
}
```

**响应数据**:
```json
{
  "token": "string",
  "adminInfo": {
    "id": "string",
    "name": "string",
    "email": "string",
    "role": "超级管理员|管理员"
  }
}
```

### 3.2 管理员退出

**接口**: `POST /api/admin/logout`

**Headers**: `Admin-Authorization: Bearer {token}`

### 3.3 获取统计概览

**接口**: `GET /api/admin/statistics/overview`

**Headers**: `Admin-Authorization: Bearer {token}`

**响应数据**:
```json
{
  "totalUsers": "number",
  "todayNewUsers": "number",
  "totalEmotionRecords": "number",
  "activeCrisis": "number",
  "activeUsers7Days": "number",
  "emotionTrend": [
    {
      "date": "YYYY-MM-DD",
      "count": "number"
    }
  ]
}
```

### 3.4 获取用户列表

**接口**: `GET /api/admin/users`

**Headers**: `Admin-Authorization: Bearer {token}`

**Query参数**:
- `page`: 页码
- `pageSize`: 每页数量
- `keyword`: 搜索关键词（用户ID/姓名/邮箱）
- `status`: active | inactive | risk
- `sortBy`: register_desc | register_asc | activity_desc | risk_desc

**响应数据**:
```json
{
  "list": [
    {
      "id": "number",
      "name": "string",
      "email": "string",
      "registerTime": "datetime",
      "lastActive": "string",
      "emotionCount": "number",
      "riskLevel": "high|medium|low",
      "status": "active|inactive"
    }
  ],
  "total": "number",
  "totalPages": "number"
}
```

### 3.5 获取用户详情

**接口**: `GET /api/admin/users/:userId`

**Headers**: `Admin-Authorization: Bearer {token}`

**响应数据**:
```json
{
  "id": "string",
  "name": "string",
  "email": "string",
  "phone": "string",
  "school": "string",
  "registerTime": "datetime",
  "lastActive": "datetime",
  "emotionCount": "number",
  "riskLevel": "high|medium|low",
  "status": "active|inactive",
  "statistics": {
    "totalDiaries": "number",
    "averageIntensity": "number",
    "mostCommonEmotion": "string"
  }
}
```

### 3.6 获取用户情绪历史详情

**接口**: `GET /api/admin/users/:userId/emotion-history`

**Headers**: `Admin-Authorization: Bearer {token}`

**Query参数**:
- `startDate`, `endDate`: 时间范围
- `emotion`: 情绪类型筛选

**响应数据**:
```json
{
  "userInfo": {
    "id": "string",
    "name": "string",
    "email": "string",
    "riskLevel": "string"
  },
  "records": [
    {
      "id": "string",
      "date": "datetime",
      "emotion": "string",
      "emotionLabel": "string",
      "emoji": "string",
      "intensity": "number",
      "content": "string",
      "triggers": ["string"],
      "riskLevel": "high|medium|low"
    }
  ],
  "statistics": {
    "total": "number",
    "positive": "number",
    "neutral": "number",
    "negative": "number",
    "averageIntensity": "number"
  }
}
```

### 3.7 更新用户状态

**接口**: `PUT /api/admin/users/:userId/status`

**Headers**: `Admin-Authorization: Bearer {token}`

**请求参数**:
```json
{
  "status": "active|inactive|suspended",
  "reason": "string"  // 可选
}
```

### 3.8 获取危机预警列表

**接口**: `GET /api/admin/crisis`

**Headers**: `Admin-Authorization: Bearer {token}`

**Query参数**:
- `page`, `pageSize`: 分页
- `level`: critical | high | medium
- `status`: pending | handling | resolved

**响应数据**:
```json
{
  "list": [
    {
      "id": "string",
      "userId": "string",
      "userName": "string",
      "level": "critical|high|medium",
      "triggerReason": "string",
      "emotionIntensity": "number",
      "status": "pending|handling|resolved",
      "createdAt": "datetime",
      "lastUpdatedAt": "datetime"
    }
  ],
  "total": "number"
}
```

### 3.9 处理危机事件

**接口**: `POST /api/admin/crisis/:crisisId/handle`

**Headers**: `Admin-Authorization: Bearer {token}`

**请求参数**:
```json
{
  "action": "string",           // 处理措施
  "result": "resolved|following|escalated|referred",
  "notes": "string",            // 备注（可选）
  "followUpPlan": "string"      // 跟进计划（可选）
}
```

### 3.10 更新系统设置

**接口**: `PUT /api/admin/settings`

**Headers**: `Admin-Authorization: Bearer {token}`

**请求参数**:
```json
{
  "crisis": {
    "intensityThreshold": "number",  // 强度阈值
    "triggerCount": "number",        // 触发次数
    "timeWindow": "number",          // 时间窗口（小时）
    "keywords": ["string"]           // 关键词列表
  },
  "notification": {
    "emailEnabled": "boolean",
    "smsEnabled": "boolean"
  },
  "dataRetention": {
    "emotionRecords": "number",      // 保留天数
    "chatHistory": "number"
  }
}
```

### 3.11 导出用户数据

**接口**: `GET /api/admin/export/users`

**Headers**: `Admin-Authorization: Bearer {token}`

**Query参数**:
- `format`: csv | excel | json
- `timeRange`: all | today | week | month | quarter | year | custom
- `startDate`, `endDate`: 自定义时间范围
- `statusFilter`: 状态筛选
- `riskFilter`: 风险等级筛选
- `minRecords`: 最小记录数
- `fields`: 导出字段（数组）
- `includeEmotionHistory`: 包含情绪历史
- `includeStatistics`: 包含统计数据
- `anonymize`: 匿名化数据

**响应**: 文件下载（blob）

### 3.12 生成用户报告

**接口**: `GET /api/admin/users/:userId/generate-report`

**Headers**: `Admin-Authorization: Bearer {token}`

**Query参数**:
- `format`: pdf | docx
- `startDate`, `endDate`: 时间范围

**响应**: PDF/DOCX文件下载

### 3.13 发送系统通知

**接口**: `POST /api/admin/notifications/send`

**Headers**: `Admin-Authorization: Bearer {token}`

**请求参数**:
```json
{
  "userIds": ["string"],  // 空数组表示全部用户
  "title": "string",
  "content": "string",
  "type": "info|warning|urgent"
}
```

---

## 4. 数据模型

### User (用户)
```typescript
{
  id: string
  username: string
  email: string
  phone?: string
  school?: string
  avatar?: string
  passwordHash: string
  status: 'active' | 'inactive' | 'suspended'
  createdAt: datetime
  lastLoginAt: datetime
  emailVerified: boolean
}
```

### EmotionDiary (情绪日记)
```typescript
{
  id: string
  userId: string
  emotion: 'joy' | 'calm' | 'sadness' | 'anxiety' | 'anger' | 'fear'
  emotionLabel: string
  emoji: string
  intensity: number  // 0-10
  content: string
  triggers?: string[]
  bodyParts?: {
    head: boolean
    chest: boolean
    stomach: boolean
    limbs: boolean
  }
  selectedImages?: string[]
  createdAt: datetime
  updatedAt: datetime
}
```

### CrisisEvent (危机事件)
```typescript
{
  id: string
  userId: string
  level: 'critical' | 'high' | 'medium'
  triggerReason: string
  emotionIntensity: number
  relatedDiaryId?: string
  status: 'pending' | 'handling' | 'resolved' | 'closed'
  handledBy?: string  // 管理员ID
  handledAt?: datetime
  action?: string
  result?: 'resolved' | 'following' | 'escalated' | 'referred'
  notes?: string
  followUpPlan?: string
  createdAt: datetime
  updatedAt: datetime
}
```

### Admin (管理员)
```typescript
{
  id: string
  username: string
  email: string
  passwordHash: string
  role: '超级管理员' | '管理员'
  permissions: string[]
  createdAt: datetime
  lastLoginAt: datetime
}
```

---

## 5. 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（未登录或token过期） |
| 403 | 禁止访问（权限不足） |
| 404 | 资源不存在 |
| 409 | 资源冲突（如用户名已存在） |
| 422 | 数据验证失败 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

---

## 6. 开发注意事项

### 6.1 认证Token

- 用户Token通过 `Authorization: Bearer {token}` header传递
- 管理员Token通过 `Admin-Authorization: Bearer {token}` header传递
- Token有效期：24小时（可通过refreshToken刷新）

### 6.2 分页

所有列表接口支持分页，默认参数：
- `page`: 1
- `pageSize`: 20
- 最大pageSize: 100

### 6.3 时间格式

- 请求：YYYY-MM-DD 或 ISO 8601
- 响应：ISO 8601 (例: 2026-01-26T10:30:00Z)

### 6.4 文件上传

使用 `multipart/form-data` 格式
- 最大文件大小：10MB
- 支持格式：jpg, png, pdf, docx

### 6.5 开发模式Mock

前端在开发模式下使用Mock数据，`import.meta.env.DEV` 为 true 时启用。
后端开发完成后，前端只需删除Mock逻辑即可无缝对接。

---

## 更新日志

- **2026-01-26**: 初始版本，包含所有核心API接口定义
