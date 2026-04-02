<template>
  <div class="admin-login-page">
    <div class="login-container">
      <!-- Logo和标题 -->
      <div class="login-header">
        <div class="logo">🔐</div>
        <h1 class="title">管理员登录</h1>
        <p class="subtitle">大学生情绪管理系统 - 后台管理</p>
      </div>

      <!-- 登录表单 -->
      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">管理员账号</label>
          <input
            v-model="form.username"
            type="text"
            class="form-input"
            placeholder="请输入管理员账号"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">登录密码</label>
          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            class="form-input"
            placeholder="请输入密码"
            required
          />
          <button
            type="button"
            class="password-toggle"
            @click="showPassword = !showPassword"
          >
            {{ showPassword ? '👁️' : '👁️‍🗨️' }}
          </button>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input v-model="form.remember" type="checkbox" />
            <span>记住我（7天）</span>
          </label>
        </div>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <!-- 登录按钮 -->
        <button type="submit" class="login-btn" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
      </form>

      <!-- 底部提示 -->
      <div class="login-footer">
        <p>⚠️ 管理员权限账号，请妥善保管密码</p>
        <a href="#" @click.prevent="handleForgotPassword" class="forgot-link">
          忘记密码？联系系统管理员
        </a>
      </div>
    </div>

    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
  </div>
</template>

<script>
import { adminLogin } from '@/api/admin.js'

export default {
  name: 'AdminLoginPage',
  data() {
    return {
      form: {
        username: '',
        password: '',
        remember: false
      },
      showPassword: false,
      isLoading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.errorMessage = ''
      this.isLoading = true

      try {
        // 调用真实的后端 API
        const response = await adminLogin({
          username: this.form.username,
          password: this.form.password,
          remember: this.form.remember
        })

        // 保存管理员 token 和信息
        localStorage.setItem('admin_token', response.data.token)
        localStorage.setItem('admin_info', JSON.stringify(response.data.adminInfo))

        // 跳转到管理员主页
        this.$router.push('/admin/dashboard')

      } catch (error) {
        console.error('管理员登录失败:', error)
        this.errorMessage = error.message || '登录失败，请检查账号密码'
      } finally {
        this.isLoading = false
      }
    },

    handleForgotPassword() {
      alert('请联系系统管理员重置密码')
    }
  },
  mounted() {
    // 检查是否已登录
    const adminToken = localStorage.getItem('admin_token')
    if (adminToken) {
      this.$router.push('/admin/dashboard')
    }
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

/* ========== 背景装饰 ========== */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  animation: float 20s infinite ease-in-out;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 200px;
  height: 200px;
  bottom: -50px;
  right: -50px;
  animation-delay: 5s;
}

.circle-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  left: 80%;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20px, -20px) scale(1.05);
  }
  50% {
    transform: translate(-10px, 30px) scale(0.95);
  }
  75% {
    transform: translate(30px, 10px) scale(1.02);
  }
}

/* ========== 登录容器 ========== */
.login-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 48px 40px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 1;
  animation: slideUp 0.6s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== 头部 ========== */
.login-header {
  text-align: center;
  margin-bottom: 36px;
}

.logo {
  font-size: 64px;
  margin-bottom: 16px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
}

/* ========== 表单 ========== */
.login-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.3s ease;
  background: #f8fafc;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 38px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
  transition: transform 0.2s ease;
}

.password-toggle:hover {
  transform: scale(1.1);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #475569;
  cursor: pointer;
  user-select: none;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* ========== 错误提示 ========== */
.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  color: #dc2626;
  font-size: 14px;
  animation: shake 0.4s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

/* ========== 登录按钮 ========== */
.login-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(59, 130, 246, 0.5);
}

.login-btn:active:not(:disabled) {
  transform: translateY(0);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: linear-gradient(135deg, #94a3b8, #64748b);
  box-shadow: none;
}

/* ========== 底部 ========== */
.login-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.login-footer p {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 8px;
}

.forgot-link {
  font-size: 13px;
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: #2563eb;
  text-decoration: underline;
}

/* ========== 响应式 ========== */
@media (max-width: 640px) {
  .login-container {
    padding: 32px 24px;
  }

  .logo {
    font-size: 48px;
  }

  .title {
    font-size: 24px;
  }
}
</style>
