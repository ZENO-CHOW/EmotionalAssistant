<template>
  <div class="register-container">
    <div class="register-card">
      <div class="logo-section">
        <div class="logo">🌱</div>
        <h1>注册账号</h1>
        <p class="subtitle">加入小安，开始情绪管理之旅</p>
      </div>

      <div class="form-section">
        <div class="input-group">
          <input
            v-model="form.username"
            type="text"
            placeholder="用户名"
          />
        </div>

        <div class="input-group">
          <input
            v-model="form.password"
            type="password"
            placeholder="密码"
          />
        </div>

        <div class="input-group">
          <input
            v-model="form.confirmPassword"
            type="password"
            placeholder="确认密码"
          />
        </div>

        <div class="input-group">
          <input
            v-model="form.email"
            type="email"
            placeholder="邮箱（可选）"
          />
        </div>

        <button class="register-btn" @click="handleRegister" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>

        <div class="footer-links">
          <a href="#" @click.prevent="goToLogin">已有账号？登录</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { register } from '@/api/auth.js'

export default {
  name: 'RegisterPage',
  data() {
    return {
      form: {
        username: '',
        password: '',
        confirmPassword: '',
        email: ''
      },
      loading: false
    }
  },
  methods: {
    async handleRegister() {
      // 验证
      if (!this.form.username || !this.form.password) {
        alert('请输入用户名和密码')
        return
      }

      if (this.form.password !== this.form.confirmPassword) {
        alert('两次密码输入不一致')
        return
      }

      this.loading = true

      try {
        const response = await register({
          username: this.form.username,
          password: this.form.password,
          confirmPassword: this.form.confirmPassword,
          ...(this.form.email && { email: this.form.email })
        })

        if (response.code === 200) {
          alert('注册成功！请登录')
          this.$router.push('/login')
        } else {
          alert(response.message || '注册失败')
        }

      } catch (error) {
        console.error('注册失败:', error)
        const errorMessage = error.response?.data?.detail?.message || error.message || '注册失败，请稍后重试'
        alert(errorMessage)
      } finally {
        this.loading = false
      }
    },

    goToLogin() {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg,
    #E8F5E9 0%,
    #C8E6C9 30%,
    #A5D6A7 60%,
    rgba(46, 125, 50, 0.76) 100%
  );
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.register-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 48px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 8px 32px rgba(46, 125, 50, 0.2);
}

.logo-section {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  font-size: 64px;
  margin-bottom: 16px;
}

h1 {
  color: #2E7D32;
  font-size: 32px;
  margin-bottom: 8px;
}

.subtitle {
  color: #666;
  font-size: 14px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-group input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid rgba(46, 125, 50, 0.2);
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s;
  background: rgba(255, 255, 255, 0.8);
}

.input-group input:focus {
  outline: none;
  border-color: #4CAF50;
  background: white;
}

.register-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #4CAF50, #2E7D32);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 8px;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
}

.register-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.footer-links {
  text-align: center;
  margin-top: 16px;
}

.footer-links a {
  color: #4CAF50;
  text-decoration: none;
  font-size: 14px;
}

.footer-links a:hover {
  text-decoration: underline;
}
</style>
