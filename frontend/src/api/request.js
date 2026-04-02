import axios from 'axios'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 添加用户token
    const userToken = localStorage.getItem('token')
    if (userToken) {
      config.headers['Authorization'] = `Bearer ${userToken}`
    }

    // 添加管理员token
    const adminToken = localStorage.getItem('admin_token')
    if (adminToken) {
      config.headers['Admin-Authorization'] = `Bearer ${adminToken}`
    }

    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const res = response.data

    // 如果返回的状态码不是200，说明有错误
    if (response.status !== 200) {
      console.error('响应错误:', res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }

    return res
  },
  error => {
    console.error('响应错误:', error)

    // 处理401未授权
    if (error.response && error.response.status === 401) {
      // 判断当前路径是否是管理员路径
      const isAdminPath = window.location.pathname.startsWith('/admin')

      if (isAdminPath) {
        // 清除管理员token
        localStorage.removeItem('admin_token')
        localStorage.removeItem('admin_info')
        // 跳转到管理员登录页
        window.location.href = '/admin/login'
      } else {
        // 清除用户token
        localStorage.removeItem('token')
        // 跳转到用户登录页
        window.location.href = '/login'
      }
    }

    // 处理403禁止访问
    if (error.response && error.response.status === 403) {
      console.error('没有权限访问该资源')
    }

    return Promise.reject(error)
  }
)

export default request
