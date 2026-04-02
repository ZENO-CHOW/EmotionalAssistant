<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-section">
        <div class="logo">🌱</div>
        <h1>小安</h1>
        <p class="subtitle">大学生情绪管理助手</p>
      </div>

      <div class="form-section">
        <div class="mode-toggle">
          <button
            :class="['toggle-btn', { active: isLoginMode }]"
            @click="toggleMode(true)"
          >登录</button>
          <button
            :class="['toggle-btn', { active: !isLoginMode }]"
            @click="toggleMode(false)"
          >注册</button>
        </div>

        <div v-if="isLoginMode" class="form-content">
          <div class="input-group">
            <input
              v-model="loginForm.username"
              type="text"
              placeholder="用户名"
              @keyup.enter="handleLogin"
            />
          </div>

          <div class="input-group">
            <input
              v-model="loginForm.password"
              type="password"
              placeholder="密码"
              @keyup.enter="handleLogin"
            />
          </div>

          <button class="submit-btn" @click="handleLogin" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>

        <div v-else class="form-content">
          <div class="input-group">
            <input
              v-model="registerForm.username"
              type="text"
              placeholder="用户名"
            />
          </div>

          <div class="input-group">
            <input
              v-model="registerForm.password"
              type="password"
              placeholder="密码"
            />
          </div>

          <div class="input-group">
            <input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="确认密码"
            />
          </div>

          <div class="input-group">
            <input
              v-model="registerForm.email"
              type="email"
              placeholder="邮箱（可选）"
            />
          </div>

          <button class="submit-btn" @click="handleRegister" :disabled="loading">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { login, register } from '@/api/auth.js'

export default {
  name: 'LoginPage',
  data() {
    return {
      isLoginMode: true,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        confirmPassword: '',
        email: ''
      },
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      if (!this.loginForm.username || !this.loginForm.password) {
        alert('请输入用户名和密码')
        return
      }

      this.loading = true

      try {
        const response = await login({
          username: this.loginForm.username,
          password: this.loginForm.password
        })

        if (response.code === 200) {
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('userInfo', JSON.stringify(response.data.userInfo))

          this.$router.push('/home')
        } else {
          alert(response.message || '登录失败')
        }

      } catch (error) {
        console.error('登录失败:', error)
        const errorMessage = error.response?.data?.detail?.message || error.message || '登录失败，请检查用户名和密码'
        alert(errorMessage)
      } finally {
        this.loading = false
      }
    },

    async handleRegister() {
      if (!this.registerForm.username || !this.registerForm.password) {
        alert('请输入用户名和密码')
        return
      }

      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        alert('两次密码输入不一致')
        return
      }

      this.loading = true

      try {
        const response = await register({
          username: this.registerForm.username,
          password: this.registerForm.password,
          confirmPassword: this.registerForm.confirmPassword,
          ...(this.registerForm.email && { email: this.registerForm.email })
        })

        if (response.code === 200) {
          alert('注册成功！请登录')
          this.isLoginMode = true
          this.registerForm = {
            username: '',
            password: '',
            confirmPassword: '',
            email: ''
          }
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

    toggleMode(mode) {
      this.isLoginMode = mode
    }
  }
}
</script>

<style scoped>
.login-container {
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

.login-card {
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

.mode-toggle {
  display: flex;
  background: rgba(76, 175, 80, 0.1);
  border-radius: 12px;
  padding: 4px;
  margin-bottom: 8px;
}

.toggle-btn {
  flex: 1;
  padding: 10px;
  background: transparent;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle-btn.active {
  background: white;
  color: #2E7D32;
  box-shadow: 0 2px 8px rgba(46, 125, 50, 0.1);
}

.form-content {
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

.submit-btn {
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
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
}

.submit-btn:disabled {
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
