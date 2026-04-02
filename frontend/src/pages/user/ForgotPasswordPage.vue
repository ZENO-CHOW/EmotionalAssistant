<template>
  <div class="forgot-password-page">
    <div class="forgot-container">
      <!-- Logo -->
      <div class="logo-section">
        <div class="logo-icon">🔐</div>
        <h1 class="page-title">找回密码</h1>
        <p class="page-subtitle">通过邮箱重置你的密码</p>
      </div>

      <!-- 步骤指示器 -->
      <div class="steps-indicator">
        <div class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
          <div class="step-number">1</div>
          <div class="step-label">输入邮箱</div>
        </div>
        <div class="step-line" :class="{ active: currentStep > 1 }"></div>
        <div class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
          <div class="step-number">2</div>
          <div class="step-label">验证码</div>
        </div>
        <div class="step-line" :class="{ active: currentStep > 2 }"></div>
        <div class="step" :class="{ active: currentStep >= 3 }">
          <div class="step-number">3</div>
          <div class="step-label">重置密码</div>
        </div>
      </div>

      <!-- 步骤1：输入邮箱 -->
      <form v-if="currentStep === 1" class="form-section" @submit.prevent="handleSendCode">
        <div class="form-group">
          <label class="form-label">邮箱地址</label>
          <input
            v-model="form.email"
            type="email"
            class="form-input"
            placeholder="请输入注册时使用的邮箱"
            required
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? '发送中...' : '发送验证码' }}
        </button>

        <div class="form-footer">
          <router-link to="/login" class="back-link">← 返回登录</router-link>
        </div>
      </form>

      <!-- 步骤2：输入验证码 -->
      <form v-if="currentStep === 2" class="form-section" @submit.prevent="handleVerifyCode">
        <div class="info-message">
          验证码已发送到 <strong>{{ form.email }}</strong>
        </div>

        <div class="form-group">
          <label class="form-label">验证码</label>
          <div class="code-input-group">
            <input
              v-model="form.code"
              type="text"
              class="form-input"
              placeholder="请输入6位验证码"
              maxlength="6"
              required
            />
            <button
              type="button"
              class="resend-btn"
              :disabled="countdown > 0"
              @click="handleResendCode"
            >
              {{ countdown > 0 ? `${countdown}秒后重发` : '重新发送' }}
            </button>
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? '验证中...' : '下一步' }}
        </button>

        <div class="form-footer">
          <button type="button" class="back-link" @click="currentStep = 1">
            ← 返回上一步
          </button>
        </div>
      </form>

      <!-- 步骤3：重置密码 -->
      <form v-if="currentStep === 3" class="form-section" @submit.prevent="handleResetPassword">
        <div class="form-group">
          <label class="form-label">新密码</label>
          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            class="form-input"
            placeholder="请输入新密码（至少6位）"
            minlength="6"
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
          <label class="form-label">确认密码</label>
          <input
            v-model="form.confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            class="form-input"
            placeholder="请再次输入新密码"
            minlength="6"
            required
          />
          <button
            type="button"
            class="password-toggle"
            @click="showConfirmPassword = !showConfirmPassword"
          >
            {{ showConfirmPassword ? '👁️' : '👁️‍🗨️' }}
          </button>
        </div>

        <div v-if="passwordError" class="error-message">
          {{ passwordError }}
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? '重置中...' : '完成重置' }}
        </button>
      </form>

      <!-- 成功提示 -->
      <div v-if="currentStep === 4" class="success-section">
        <div class="success-icon">✅</div>
        <h2 class="success-title">密码重置成功！</h2>
        <p class="success-text">你的密码已成功重置，现在可以使用新密码登录了</p>
        <button class="submit-btn" @click="goToLogin">
          前往登录
        </button>
      </div>

      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-toast">
        {{ errorMessage }}
      </div>
    </div>

    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ForgotPasswordPage',
  data() {
    return {
      currentStep: 1,
      form: {
        email: '',
        code: '',
        password: '',
        confirmPassword: ''
      },
      showPassword: false,
      showConfirmPassword: false,
      isLoading: false,
      countdown: 0,
      errorMessage: '',
      passwordError: ''
    }
  },
  methods: {
    async handleSendCode() {
      this.isLoading = true
      this.errorMessage = ''

      try {
        // 🔧 开发模式：模拟发送验证码
        await new Promise(resolve => setTimeout(resolve, 1000))

        console.log('发送验证码到:', this.form.email)

        // 进入下一步
        this.currentStep = 2
        this.startCountdown()

      } catch (error) {
        this.errorMessage = '发送验证码失败，请稍后重试'
      } finally {
        this.isLoading = false
      }
    },

    async handleVerifyCode() {
      if (this.form.code.length !== 6) {
        this.errorMessage = '请输入6位验证码'
        return
      }

      this.isLoading = true
      this.errorMessage = ''

      try {
        // 🔧 开发模式：模拟验证
        await new Promise(resolve => setTimeout(resolve, 800))

        console.log('验证码:', this.form.code)

        // 进入下一步
        this.currentStep = 3

      } catch (error) {
        this.errorMessage = '验证码错误，请重新输入'
      } finally {
        this.isLoading = false
      }
    },

    async handleResetPassword() {
      this.passwordError = ''
      this.errorMessage = ''

      // 验证密码
      if (this.form.password.length < 6) {
        this.passwordError = '密码至少需要6位'
        return
      }

      if (this.form.password !== this.form.confirmPassword) {
        this.passwordError = '两次输入的密码不一致'
        return
      }

      this.isLoading = true

      try {
        // 🔧 开发模式：模拟重置密码
        await new Promise(resolve => setTimeout(resolve, 1000))

        console.log('重置密码成功')

        // 显示成功页面
        this.currentStep = 4

      } catch (error) {
        this.errorMessage = '密码重置失败，请稍后重试'
      } finally {
        this.isLoading = false
      }
    },

    async handleResendCode() {
      if (this.countdown > 0) return
      await this.handleSendCode()
    },

    startCountdown() {
      this.countdown = 60
      const timer = setInterval(() => {
        this.countdown--
        if (this.countdown <= 0) {
          clearInterval(timer)
        }
      }, 1000)
    },

    goToLogin() {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.forgot-password-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 50%, #A5D6A7 100%);
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
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite ease-in-out;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  right: -100px;
}

.circle-2 {
  width: 200px;
  height: 200px;
  bottom: -50px;
  left: -50px;
  animation-delay: 5s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(20px, -20px) scale(1.05);
  }
}

/* ========== 容器 ========== */
.forgot-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 48px 40px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(46, 125, 50, 0.2);
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

/* ========== Logo区域 ========== */
.logo-section {
  text-align: center;
  margin-bottom: 36px;
}

.logo-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #2E7D32;
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 14px;
  color: #66BB6A;
}

/* ========== 步骤指示器 ========== */
.steps-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 32px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #E0E0E0;
  color: #9E9E9E;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.step.completed .step-number {
  background: #4CAF50;
  color: white;
}

.step-label {
  font-size: 12px;
  color: #9E9E9E;
  font-weight: 500;
}

.step.active .step-label {
  color: #2E7D32;
  font-weight: 600;
}

.step-line {
  width: 60px;
  height: 2px;
  background: #E0E0E0;
  margin: 0 8px;
  transition: all 0.3s ease;
}

.step-line.active {
  background: #4CAF50;
}

/* ========== 表单 ========== */
.form-section {
  margin-bottom: 24px;
}

.info-message {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 20px;
  font-size: 14px;
  color: #2E7D32;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #E0E0E0;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 4px rgba(76, 175, 80, 0.1);
}

.code-input-group {
  display: flex;
  gap: 12px;
}

.code-input-group .form-input {
  flex: 1;
}

.resend-btn {
  padding: 14px 20px;
  background: rgba(76, 175, 80, 0.1);
  border: 2px solid rgba(76, 175, 80, 0.3);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #4CAF50;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.resend-btn:hover:not(:disabled) {
  background: rgba(76, 175, 80, 0.2);
}

.resend-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(76, 175, 80, 0.4);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(76, 175, 80, 0.5);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #9E9E9E;
  box-shadow: none;
}

.form-footer {
  text-align: center;
  margin-top: 16px;
}

.back-link {
  font-size: 14px;
  color: #4CAF50;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s ease;
}

.back-link:hover {
  color: #2E7D32;
}

/* ========== 成功页面 ========== */
.success-section {
  text-align: center;
  padding: 40px 20px;
}

.success-icon {
  font-size: 80px;
  margin-bottom: 24px;
  animation: bounce 0.8s ease;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.success-title {
  font-size: 24px;
  font-weight: 700;
  color: #2E7D32;
  margin-bottom: 12px;
}

.success-text {
  font-size: 15px;
  color: #66BB6A;
  margin-bottom: 32px;
  line-height: 1.6;
}

/* ========== 错误提示 ========== */
.error-message {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  color: #d32f2f;
  font-size: 14px;
}

.error-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #f44336;
  color: white;
  padding: 16px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(244, 67, 54, 0.4);
  z-index: 9999;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* ========== 响应式 ========== */
@media (max-width: 640px) {
  .forgot-container {
    padding: 32px 24px;
  }

  .steps-indicator {
    transform: scale(0.9);
  }

  .code-input-group {
    flex-direction: column;
  }
}
</style>
