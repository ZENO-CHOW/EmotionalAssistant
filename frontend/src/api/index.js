import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api', // Vite会代理到 http://localhost:3000/api
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加token等
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// API方法
export default {
  // 发送聊天消息
  sendMessage(message, userId = 'default') {
    return api.post('/chat', { message, userId })
  },

  // 清除聊天历史
  clearHistory(userId = 'default') {
    return api.post('/clear', { userId })
  },

  // 健康检查
  healthCheck() {
    return api.get('/health')
  }
}
