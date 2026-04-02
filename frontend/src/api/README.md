# API 使用指南

## 目录结构

```
src/api/
├── README.md           # 本文件
├── request.js          # Axios封装（HTTP请求客户端）
├── auth.js             # 用户认证相关API
├── emotion.js          # 情绪识别和日记相关API
├── admin.js            # 管理员相关API
└── index.js            # 旧版API（待迁移）
```

## 快速开始

### 1. 导入API方法

```javascript
// 导入单个API方法
import { login, register } from '@/api/auth'
import { createDiary, getDiaryList } from '@/api/emotion'
import { getUserList, exportUserData } from '@/api/admin'

// 或导入整个模块
import authAPI from '@/api/auth'
import emotionAPI from '@/api/emotion'
import adminAPI from '@/api/admin'
```

### 2. 使用示例

#### 用户登录
```javascript
import { login } from '@/api/auth'

async function handleLogin() {
  try {
    const response = await login({
      username: 'user@example.com',
      password: 'password123'
    })

    // 保存token
    localStorage.setItem('token', response.data.token)
    localStorage.setItem('user_info', JSON.stringify(response.data.user))

    console.log('登录成功:', response.data.user)
  } catch (error) {
    console.error('登录失败:', error)
    alert('登录失败，请检查用户名和密码')
  }
}
```

#### 创建情绪日记
```javascript
import { createDiary } from '@/api/emotion'

async function saveDiary() {
  try {
    const response = await createDiary({
      emotion: 'joy',
      emotionLabel: '开心',
      emoji: '😊',
      intensity: 8,
      content: '今天心情很好，考试通过了！',
      triggers: ['学业'],
      bodyParts: {
        head: false,
        chest: true,
        stomach: false,
        limbs: false
      }
    })

    console.log('日记创建成功:', response.data)
  } catch (error) {
    console.error('创建失败:', error)
  }
}
```

#### 管理员获取用户列表
```javascript
import { getUserList } from '@/api/admin'

async function loadUsers() {
  try {
    const response = await getUserList({
      page: 1,
      pageSize: 20,
      keyword: '',
      status: 'active',
      sortBy: 'register_desc'
    })

    console.log('用户列表:', response.data.list)
    console.log('总数:', response.data.total)
  } catch (error) {
    console.error('加载失败:', error)
  }
}
```

## Request.js 配置说明

### 基础配置

```javascript
// src/api/request.js
import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})
```

### 请求拦截器

自动添加认证Token到请求头：

```javascript
request.interceptors.request.use(
  config => {
    // 用户Token
    const userToken = localStorage.getItem('token')
    if (userToken) {
      config.headers['Authorization'] = `Bearer ${userToken}`
    }

    // 管理员Token
    const adminToken = localStorage.getItem('admin_token')
    if (adminToken) {
      config.headers['Admin-Authorization'] = `Bearer ${adminToken}`
    }

    return config
  },
  error => Promise.reject(error)
)
```

### 响应拦截器

自动处理响应和错误：

```javascript
request.interceptors.response.use(
  response => response.data,
  error => {
    // 401: 未授权，清除token并跳转登录
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('admin_token')
      window.location.href = '/login'
    }

    // 403: 权限不足
    if (error.response?.status === 403) {
      console.error('没有权限访问该资源')
    }

    return Promise.reject(error)
  }
)
```

## 环境变量配置

在项目根目录创建环境变量文件：

### `.env.development` (开发环境)
```
VITE_API_BASE_URL=http://localhost:3000
```

### `.env.production` (生产环境)
```
VITE_API_BASE_URL=https://api.yourdomain.com
```

## 开发模式 Mock

在后端API未完成时，前端使用Mock数据进行开发：

```javascript
async function someAPICall() {
  // 检测开发模式
  const isDevelopment = import.meta.env.DEV

  if (isDevelopment) {
    // 使用Mock数据
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      data: {
        // Mock数据
      }
    }
  }

  // 生产模式：调用真实API
  return request({
    url: '/api/some-endpoint',
    method: 'get'
  })
}
```

## 错误处理最佳实践

### 1. 使用 try-catch
```javascript
async function fetchData() {
  try {
    const response = await someAPI()
    // 处理成功
  } catch (error) {
    // 处理错误
    console.error('API Error:', error)

    // 显示用户友好的错误消息
    if (error.response) {
      // 服务器返回错误
      alert(error.response.data.message || '操作失败')
    } else if (error.request) {
      // 请求发出但没有收到响应
      alert('网络错误，请检查连接')
    } else {
      // 其他错误
      alert('发生未知错误')
    }
  }
}
```

### 2. 统一错误处理
```javascript
// utils/errorHandler.js
export function handleAPIError(error) {
  if (error.response) {
    const { status, data } = error.response

    switch (status) {
      case 400:
        return data.message || '请求参数错误'
      case 401:
        return '请先登录'
      case 403:
        return '没有权限执行此操作'
      case 404:
        return '请求的资源不存在'
      case 500:
        return '服务器错误，请稍后重试'
      default:
        return '操作失败，请重试'
    }
  } else if (error.request) {
    return '网络连接失败'
  } else {
    return error.message || '未知错误'
  }
}

// 使用
import { handleAPIError } from '@/utils/errorHandler'

try {
  await someAPI()
} catch (error) {
  const errorMessage = handleAPIError(error)
  alert(errorMessage)
}
```

## 文件下载处理

### 导出CSV/Excel
```javascript
import { exportUserData } from '@/api/admin'

async function handleExport() {
  try {
    const response = await exportUserData({
      format: 'csv',
      startDate: '2026-01-01',
      endDate: '2026-01-31'
    })

    // 创建下载链接
    const blob = new Blob([response.data], { type: 'text/csv' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `用户数据_${Date.now()}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    alert('导出成功！')
  } catch (error) {
    console.error('导出失败:', error)
    alert('导出失败，请重试')
  }
}
```

## API调用优化

### 1. 防抖（Debounce）
适用于搜索框等频繁触发的场景：

```javascript
let searchTimer = null

function handleSearch(keyword) {
  // 清除上一次的定时器
  clearTimeout(searchTimer)

  // 延迟500ms执行搜索
  searchTimer = setTimeout(async () => {
    try {
      const response = await getUserList({ keyword })
      // 更新列表
    } catch (error) {
      console.error(error)
    }
  }, 500)
}
```

### 2. 并发请求
当需要同时获取多个数据时：

```javascript
async function loadAllData() {
  try {
    const [users, statistics, crisis] = await Promise.all([
      getUserList({ page: 1 }),
      getStatisticsOverview(),
      getCrisisList({ status: 'pending' })
    ])

    // 同时处理所有数据
    console.log('用户:', users.data)
    console.log('统计:', statistics.data)
    console.log('危机:', crisis.data)
  } catch (error) {
    console.error('加载失败:', error)
  }
}
```

### 3. 请求取消
对于可能被中断的长时间请求：

```javascript
import axios from 'axios'

let cancelToken = null

async function searchUsers(keyword) {
  // 取消上一次请求
  if (cancelToken) {
    cancelToken.cancel('新的搜索请求')
  }

  // 创建新的取消令牌
  cancelToken = axios.CancelToken.source()

  try {
    const response = await getUserList(
      { keyword },
      { cancelToken: cancelToken.token }
    )
    return response
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('请求已取消:', error.message)
    } else {
      console.error('搜索失败:', error)
    }
  }
}
```

## 常见问题

### Q1: 如何调试API请求？

在浏览器开发者工具的Network标签中查看请求和响应。也可以在request.js中添加日志：

```javascript
request.interceptors.request.use(config => {
  console.log('API Request:', config.method.toUpperCase(), config.url, config.data)
  return config
})

request.interceptors.response.use(response => {
  console.log('API Response:', response.config.url, response.data)
  return response.data
})
```

### Q2: Token过期怎么办？

响应拦截器会自动处理401错误，清除token并跳转登录页。也可以实现自动刷新token：

```javascript
request.interceptors.response.use(
  response => response.data,
  async error => {
    if (error.response?.status === 401) {
      // 尝试刷新token
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await refreshToken({ refreshToken })
          localStorage.setItem('token', response.data.token)

          // 重试原请求
          error.config.headers['Authorization'] = `Bearer ${response.data.token}`
          return request(error.config)
        } catch (refreshError) {
          // 刷新失败，跳转登录
          localStorage.clear()
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)
```

### Q3: 如何处理大文件上传？

使用FormData和进度监听：

```javascript
async function uploadFile(file) {
  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await request({
      url: '/api/upload',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        console.log(`上传进度: ${percentCompleted}%`)
      }
    })
    return response
  } catch (error) {
    console.error('上传失败:', error)
  }
}
```

## 与后端对接

### 开发阶段
1. 前端使用Mock数据独立开发
2. 后端按照API文档开发接口
3. 定期沟通确保接口一致性

### 联调阶段
1. 关闭前端Mock，切换到真实API
2. 使用Postman/Insomnia测试后端接口
3. 逐个接口验证，处理差异

### 上线前
1. 确认所有环境变量配置正确
2. 测试所有核心功能流程
3. 检查错误处理是否完善

## 参考资料

- [完整API文档](../../API_REFERENCE.md)
- [Axios官方文档](https://axios-http.com/)
- [Vue 3文档](https://vuejs.org/)

## 更新日志

- **2026-01-26**: 初始版本，包含所有API使用说明
