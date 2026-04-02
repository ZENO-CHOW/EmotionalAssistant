# API接口文档

> **重要说明**: 本文档列出所有前后端对接点，前端开发时需要在对应位置预留接口调用

## 📍 接口基础配置

### Base URL
- 开发环境: `http://localhost:3000/api`
- 生产环境: `待定`

### 请求头
```javascript
{
  'Content-Type': 'application/json',
  'Authorization': 'Bearer {token}'  // 登录后需要
}
```

---

## 1️⃣ 用户认证模块

### 1.1 用户注册
```
POST /auth/register
```

**请求参数**:
```json
{
  "username": "string",      // 用户名
  "password": "string",      // 密码
  "email": "string",         // 邮箱（可选）
  "studentId": "string"      // 学号（可选）
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "userId": "string",
    "token": "string",
    "username": "string"
  }
}
```

**前端调用位置**: `RegisterPage.vue`

---

### 1.2 用户登录
```
POST /auth/login
```

**请求参数**:
```json
{
  "username": "string",
  "password": "string"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "userId": "string",
    "token": "string",
    "username": "string",
    "role": "user"  // user | admin
  }
}
```

**前端调用位置**: `LoginPage.vue`, `AdminLogin.vue`

---

### 1.3 退出登录
```
POST /auth/logout
```

**前端调用位置**: `NavBar.vue`

---

## 2️⃣ 情绪识别模块

### 2.1 获取情绪图片集
```
GET /emotion/images
```

**查询参数**:
```
?library=iaps  // iaps | gaped
&category=all  // all | anxiety | sadness | anger | joy
&count=20      // 返回图片数量
```

**响应**:
```json
{
  "success": true,
  "data": [
    {
      "imageId": "string",
      "url": "string",
      "library": "iaps",
      "valence": 3.5,    // 效价值（1-9）
      "arousal": 6.2,    // 唤醒度（1-9）
      "dominance": 4.1   // 支配度（1-9）
    }
  ]
}
```

**前端调用位置**: `EmotionImageSelector.vue`

---

### 2.2 提交情绪图片选择结果
```
POST /emotion/analyze
```

**请求参数**:
```json
{
  "userId": "string",
  "selectedImages": [
    {
      "imageId": "string",
      "selectionTime": 1500  // 选择时长（ms）
    }
  ],
  "intensity": 7,  // 情绪强度（1-10）
  "context": "对话中" | "日记记录"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "emotionType": "anxiety",  // 识别出的情绪类型
    "confidence": 0.85,        // 置信度
    "valence": 3.2,           // 综合效价
    "arousal": 6.5,           // 综合唤醒度
    "intensity": 7,           // 用户填写的强度
    "isCrisis": false         // 是否危机状态
  }
}
```

**前端调用位置**: `EmotionImageSelector.vue`, `DiaryForm.vue`

---

## 3️⃣ 对话模块

### 3.1 发送消息（支持流式返回）
```
POST /chat/message
```

**请求参数**:
```json
{
  "userId": "string",
  "message": "string",           // 用户消息
  "emotionData": {               // 可选，情绪识别结果
    "emotionType": "anxiety",
    "intensity": 7,
    "valence": 3.2,
    "arousal": 6.5
  },
  "sessionId": "string"          // 会话ID
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "messageId": "string",
    "reply": "string",           // AI回复
    "isCrisis": false,          // 是否触发危机
    "crisisLevel": null,        // 危机等级: low | medium | high
    "suggestedSkills": [        // 推荐的DBT技能
      {
        "skillId": "tipp",
        "skillName": "TIPP技能",
        "reason": "适合当前高强度焦虑"
      }
    ],
    "nextStep": "skill_guidance" | "continue_chat" | "crisis_intervention"
  }
}
```

**前端调用位置**: `ChatBox.vue`, `MessageInput.vue`

---

### 3.2 获取DBT技能引导内容
```
POST /chat/dbt-guidance
```

**请求参数**:
```json
{
  "userId": "string",
  "skillId": "string",      // 技能ID: tipp, stop, mindfulness等
  "emotionState": {
    "type": "anxiety",
    "intensity": 7
  }
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "skillId": "tipp",
    "guidanceSteps": [       // 引导步骤（由AI生成）
      {
        "stepId": 1,
        "instruction": "首先，让我们尝试冷水刺激...",
        "interactionType": "text" | "confirmation" | "input",
        "expectedResponse": "string"
      }
    ],
    "estimatedDuration": "5-10分钟"
  }
}
```

**前端调用位置**: `DBTGuidance.vue`

---

### 3.3 提交技能使用反馈
```
POST /chat/skill-feedback
```

**请求参数**:
```json
{
  "userId": "string",
  "skillId": "string",
  "usageDuration": 600,      // 使用时长（秒）
  "effectRating": 7,         // 效果评分（1-10）
  "intensityBefore": 8,      // 使用前强度
  "intensityAfter": 5,       // 使用后强度
  "feedback": "string"       // 文字反馈（可选）
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "recordId": "string",
    "nextSuggestion": "继续练习" | "尝试其他技能" | "寻求专业帮助"
  }
}
```

**前端调用位置**: `DBTGuidance.vue`

---

### 3.4 获取对话历史
```
GET /chat/history
```

**查询参数**:
```
?userId=string
&limit=50
&offset=0
&startDate=2024-01-01
&endDate=2024-01-31
```

**响应**:
```json
{
  "success": true,
  "data": {
    "total": 100,
    "conversations": [
      {
        "sessionId": "string",
        "startTime": "2024-01-25T10:30:00Z",
        "endTime": "2024-01-25T10:45:00Z",
        "messageCount": 12,
        "mainEmotion": "anxiety",
        "skillsUsed": ["tipp", "mindfulness"],
        "summary": "用户因考试焦虑寻求帮助，使用TIPP技能后情绪有所缓解"
      }
    ]
  }
}
```

**前端调用位置**: `ChatHistory.vue`

---

### 3.5 清除对话历史
```
POST /chat/clear
```

**请求参数**:
```json
{
  "userId": "string",
  "sessionId": "string"  // 可选，指定会话ID则只清除该会话
}
```

**前端调用位置**: `ChatBox.vue`

---

## 4️⃣ 危机干预模块

### 4.1 获取危机干预资源
```
GET /crisis/resources
```

**响应**:
```json
{
  "success": true,
  "data": {
    "hotlines": [
      {
        "name": "教育部华中师范大学心理援助热线",
        "phone": "4009-678-920",
        "available": "24小时",
        "description": "免费、专业"
      }
    ],
    "campusResources": [
      {
        "name": "学校心理咨询中心",
        "contact": "xxx-xxxx",
        "location": "学生活动中心3楼"
      }
    ]
  }
}
```

**前端调用位置**: `CrisisModal.vue`, `HotlineCard.vue`

---

### 4.2 记录危机事件
```
POST /crisis/log
```

**请求参数**:
```json
{
  "userId": "string",
  "crisisLevel": "low" | "medium" | "high",
  "triggerType": "keyword" | "emotion_intensity" | "behavior_pattern",
  "contextMessage": "string",
  "emotionData": {
    "type": "string",
    "intensity": 9
  }
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "crisisId": "string",
    "needHumanIntervention": true,  // 是否需要人工介入
    "notifiedAdmins": ["adminId1"]
  }
}
```

**前端调用位置**: `ChatBox.vue`（自动触发）

---

## 5️⃣ 情绪日记模块

### 5.1 创建日记
```
POST /diary/create
```

**请求参数**:
```json
{
  "userId": "string",
  "date": "2024-01-25",
  "overallFeeling": "string",    // 今日整体感受
  "emotionData": {
    "type": "anxiety",
    "intensity": 7,
    "selectedImages": ["imageId1", "imageId2"]
  },
  "skillsUsed": [
    {
      "skillId": "tipp",
      "duration": 600,
      "effect": 7
    }
  ],
  "notes": "string"              // 额外备注（可选）
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "diaryId": "string",
    "createdAt": "2024-01-25T20:00:00Z"
  }
}
```

**前端调用位置**: `DiaryForm.vue`

---

### 5.2 获取日记列表
```
GET /diary/list
```

**查询参数**:
```
?userId=string
&startDate=2024-01-01
&endDate=2024-01-31
&emotionType=anxiety  // 可选，筛选情绪类型
```

**响应**:
```json
{
  "success": true,
  "data": {
    "total": 30,
    "diaries": [
      {
        "diaryId": "string",
        "date": "2024-01-25",
        "emotionType": "anxiety",
        "intensity": 7,
        "skillsUsed": ["tipp"],
        "preview": "今天因为考试很焦虑..."
      }
    ]
  }
}
```

**前端调用位置**: `DiaryList.vue`

---

### 5.3 获取日记详情
```
GET /diary/:diaryId
```

**响应**:
```json
{
  "success": true,
  "data": {
    "diaryId": "string",
    "date": "2024-01-25",
    "overallFeeling": "string",
    "emotionData": { ... },
    "skillsUsed": [ ... ],
    "notes": "string",
    "emotionTrend": {
      "weekAverage": 6.2,
      "comparison": "比上周降低了1.5分"
    }
  }
}
```

**前端调用位置**: `DiaryDetail.vue`

---

## 6️⃣ 个人信息模块

### 6.1 获取用户信息
```
GET /user/profile
```

**响应**:
```json
{
  "success": true,
  "data": {
    "userId": "string",
    "username": "string",
    "email": "string",
    "joinDate": "2024-01-01",
    "stats": {
      "totalChats": 50,
      "totalDiaries": 30,
      "skillsMastered": 5,
      "consecutiveDays": 15
    },
    "badges": [
      {
        "badgeId": "first_chat",
        "name": "初次对话",
        "icon": "url",
        "earnedAt": "2024-01-01"
      }
    ]
  }
}
```

**前端调用位置**: `ProfileHeader.vue`, `ProfileTab.vue`

---

### 6.2 获取技能训练记录
```
GET /user/skill-records
```

**查询参数**:
```
?userId=string
&skillId=tipp  // 可选
&limit=20
```

**响应**:
```json
{
  "success": true,
  "data": {
    "records": [
      {
        "recordId": "string",
        "skillId": "tipp",
        "skillName": "TIPP技能",
        "usedAt": "2024-01-25T10:30:00Z",
        "duration": 600,
        "effectRating": 7,
        "context": "考试焦虑"
      }
    ],
    "skillStats": {
      "mostUsed": "mindfulness",
      "mostEffective": "tipp",
      "totalPracticeTime": 3600  // 秒
    }
  }
}
```

**前端调用位置**: `SkillRecord.vue`

---

## 7️⃣ 管理员模块

### 7.1 获取用户列表
```
GET /admin/users
```

**查询参数**:
```
?page=1
&limit=20
&search=username  // 可选
&status=active | inactive
```

**响应**:
```json
{
  "success": true,
  "data": {
    "total": 500,
    "users": [
      {
        "userId": "string",
        "username": "string",
        "email": "string",
        "joinDate": "2024-01-01",
        "lastActive": "2024-01-25T10:30:00Z",
        "totalChats": 50,
        "crisisCount": 2,
        "status": "active"
      }
    ]
  }
}
```

**前端调用位置**: `UserManagement.vue`

---

### 7.2 获取危机事件列表
```
GET /admin/crisis-events
```

**查询参数**:
```
?status=pending | handled
&level=low | medium | high
&startDate=2024-01-01
&limit=50
```

**响应**:
```json
{
  "success": true,
  "data": {
    "events": [
      {
        "crisisId": "string",
        "userId": "string",
        "username": "string",
        "level": "high",
        "triggerType": "keyword",
        "occurredAt": "2024-01-25T10:30:00Z",
        "status": "pending",
        "contextMessage": "我真的不想活了...",
        "emotionIntensity": 10
      }
    ]
  }
}
```

**前端调用位置**: `CrisisMonitor.vue`

---

### 7.3 处理危机事件
```
POST /admin/crisis-events/:crisisId/handle
```

**请求参数**:
```json
{
  "adminId": "string",
  "action": "contacted" | "escalated" | "resolved",
  "notes": "已联系学生，情况稳定"
}
```

**前端调用位置**: `CrisisMonitor.vue`

---

### 7.4 获取系统统计数据
```
GET /admin/statistics
```

**查询参数**:
```
?startDate=2024-01-01
&endDate=2024-01-31
&metric=users | emotions | skills | crisis
```

**响应**:
```json
{
  "success": true,
  "data": {
    "userStats": {
      "totalUsers": 500,
      "activeUsers": 350,
      "newUsers": 50
    },
    "emotionDistribution": {
      "anxiety": 35,
      "sadness": 25,
      "anger": 15,
      "joy": 15,
      "other": 10
    },
    "skillUsage": {
      "tipp": 150,
      "mindfulness": 200,
      "stop": 80
    },
    "crisisEvents": {
      "total": 10,
      "handled": 8,
      "pending": 2
    }
  }
}
```

**前端调用位置**: `DataStatistics.vue`, `AdminDashboard.vue`

---

### 7.5 查看用户对话记录（管理员权限）
```
GET /admin/chat-logs/:userId
```

**查询参数**:
```
?sessionId=string  // 可选
&limit=50
```

**响应**:
```json
{
  "success": true,
  "data": {
    "userId": "string",
    "username": "string",
    "sessions": [
      {
        "sessionId": "string",
        "startTime": "2024-01-25T10:30:00Z",
        "messages": [
          {
            "role": "user",
            "content": "我很焦虑",
            "timestamp": "2024-01-25T10:30:00Z"
          },
          {
            "role": "assistant",
            "content": "我能理解...",
            "timestamp": "2024-01-25T10:30:15Z"
          }
        ]
      }
    ]
  }
}
```

**前端调用位置**: `ChatLogViewer.vue`

---

## 8️⃣ WebSocket实时通信

### 8.1 连接配置
```
ws://localhost:3000/ws
```

### 8.2 事件类型

#### 管理员端实时推送
```javascript
// 新危机事件通知
{
  "event": "crisis_alert",
  "data": {
    "crisisId": "string",
    "userId": "string",
    "level": "high",
    "message": "检测到高危关键词"
  }
}

// 系统统计实时更新
{
  "event": "stats_update",
  "data": {
    "activeUsers": 25,
    "pendingCrisis": 3
  }
}
```

**前端监听位置**: `AdminDashboard.vue`, `CrisisMonitor.vue`

---

## 📝 接口调用清单

### 前端组件 → API映射表

| 组件 | 调用的API | 优先级 |
|------|-----------|--------|
| `LoginPage.vue` | POST /auth/login | P0 |
| `RegisterPage.vue` | POST /auth/register | P0 |
| `ChatBox.vue` | POST /chat/message<br>POST /chat/clear<br>POST /crisis/log | P0 |
| `EmotionImageSelector.vue` | GET /emotion/images<br>POST /emotion/analyze | P0 |
| `DBTGuidance.vue` | POST /chat/dbt-guidance<br>POST /chat/skill-feedback | P0 |
| `CrisisModal.vue` | GET /crisis/resources | P0 |
| `DiaryForm.vue` | POST /diary/create<br>POST /emotion/analyze | P1 |
| `DiaryList.vue` | GET /diary/list | P1 |
| `DiaryDetail.vue` | GET /diary/:diaryId | P1 |
| `ProfileHeader.vue` | GET /user/profile | P1 |
| `ChatHistory.vue` | GET /chat/history | P2 |
| `SkillRecord.vue` | GET /user/skill-records | P2 |
| `UserManagement.vue` | GET /admin/users | P2 |
| `CrisisMonitor.vue` | GET /admin/crisis-events<br>POST /admin/crisis-events/:id/handle<br>WebSocket监听 | P2 |
| `DataStatistics.vue` | GET /admin/statistics | P2 |
| `ChatLogViewer.vue` | GET /admin/chat-logs/:userId | P3 |

**优先级说明**:
- P0: 核心功能，必须优先实现
- P1: 重要功能，第二阶段
- P2: 管理功能，第三阶段
- P3: 辅助功能，后期优化

---

## 🔧 开发注意事项

1. **错误处理**: 所有API调用都需要统一的错误处理
2. **Loading状态**: 请求期间显示loading动画
3. **Token刷新**: Token过期时自动刷新或跳转登录
4. **请求重试**: 网络错误时支持重试机制
5. **数据缓存**: 合理使用缓存减少请求
6. **接口Mock**: 后端未完成时使用Mock数据
