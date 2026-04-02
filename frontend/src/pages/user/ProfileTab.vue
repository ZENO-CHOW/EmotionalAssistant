<template>
  <div class="profile-tab">
    <!-- 个人信息头部 -->
    <div class="profile-header">
      <div class="avatar-container">
        <div class="avatar-ring"></div>
        <div class="avatar">🌱</div>
      </div>
      <div class="profile-info">
        <!-- 显示昵称 -->
        <div v-if="!editingUsername" class="nickname-display">
          <span class="nickname">{{ displayUsername }}</span>
          <button class="edit-nickname-btn" @click="startEditUsername" title="编辑昵称">
            ✏️
          </button>
        </div>

        <!-- 编辑昵称 -->
        <div v-else class="nickname-edit">
          <input
            ref="usernameInput"
            v-model="tempUsername"
            type="text"
            class="nickname-input"
            placeholder="输入你的昵称"
            maxlength="10"
            @keyup.enter="saveUsername"
            @keyup.esc="cancelEditUsername"
          />
          <button class="save-btn" @click="saveUsername">✓</button>
          <button class="cancel-btn" @click="cancelEditUsername">✕</button>
        </div>

        <div class="user-stats">
          <span class="stat-value">🔥 已坚持 {{ joinDays }} 天</span>
          <span class="stat-value">📝 记录 {{ stats.diaries }} 次</span>
        </div>
      </div>
    </div>

    <!-- DBT技能学习进度 -->
    <div class="data-card">
      <div class="section-title">🎯 DBT技能学习进度</div>

      <div
        v-for="skill in skills"
        :key="skill.name"
        class="skill-item"
      >
        <div class="skill-header">
          <span class="skill-label">{{ skill.icon }} {{ skill.name }}</span>
          <span class="skill-percentage">{{ skill.progress }}%</span>
        </div>
        <div class="progress-track">
          <div class="progress-bar" :style="{ width: skill.progress + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- 快捷入口 -->
    <div class="data-card">
      <div class="section-title">🔗 快捷入口</div>
      <div class="quick-links">
        <button class="quick-link-btn" @click="goToEmotionHistory">
          <span class="link-icon">📊</span>
          <div class="link-info">
            <div class="link-title">情绪历史分析</div>
            <div class="link-desc">查看详细的情绪记录和趋势分析</div>
          </div>
          <span class="link-arrow">→</span>
        </button>
      </div>
    </div>

    <!-- 修改密码 -->
    <div class="data-card">
      <div class="section-title">🔐 修改密码</div>

      <div v-if="!showPasswordForm" class="password-prompt">
        <p class="prompt-text">为了保护你的账户安全，建议定期更换密码</p>
        <button class="change-password-btn" @click="showPasswordForm = true">
          修改密码
        </button>
      </div>

      <div v-else class="password-form">
        <!-- 当前密码 -->
        <div class="form-group">
          <label class="form-label">当前密码</label>
          <div class="password-input-wrapper">
            <input
              v-model="passwordForm.currentPassword"
              :type="showCurrentPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请输入当前密码"
            />
            <button
              type="button"
              class="toggle-password"
              @click="showCurrentPassword = !showCurrentPassword"
            >
              {{ showCurrentPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
        </div>

        <!-- 新密码 -->
        <div class="form-group">
          <label class="form-label">新密码</label>
          <div class="password-input-wrapper">
            <input
              v-model="passwordForm.newPassword"
              :type="showNewPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请输入新密码（至少6位）"
            />
            <button
              type="button"
              class="toggle-password"
              @click="showNewPassword = !showNewPassword"
            >
              {{ showNewPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
          <!-- 密码强度指示器 -->
          <div v-if="passwordForm.newPassword" class="password-strength">
            <div class="strength-bar">
              <div
                class="strength-fill"
                :class="passwordStrengthClass"
                :style="{ width: passwordStrengthWidth }"
              ></div>
            </div>
            <span class="strength-text" :class="passwordStrengthClass">
              {{ passwordStrengthText }}
            </span>
          </div>
        </div>

        <!-- 确认新密码 -->
        <div class="form-group">
          <label class="form-label">确认新密码</label>
          <div class="password-input-wrapper">
            <input
              v-model="passwordForm.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请再次输入新密码"
            />
            <button
              type="button"
              class="toggle-password"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              {{ showConfirmPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
          <!-- 密码匹配提示 -->
          <div v-if="passwordForm.confirmPassword" class="password-match-hint">
            <span v-if="passwordsMatch" class="match-success">✓ 密码匹配</span>
            <span v-else class="match-error">✗ 密码不匹配</span>
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-if="passwordError" class="error-message">
          {{ passwordError }}
        </div>

        <!-- 成功提示 -->
        <div v-if="passwordSuccess" class="success-message">
          {{ passwordSuccess }}
        </div>

        <!-- 按钮组 -->
        <div class="form-actions">
          <button
            class="submit-btn"
            @click="handleChangePassword"
            :disabled="passwordLoading || !canSubmitPassword"
          >
            {{ passwordLoading ? '修改中...' : '确认修改' }}
          </button>
          <button class="cancel-btn-form" @click="cancelPasswordChange">
            取消
          </button>
        </div>
      </div>
    </div>

    <!-- 小安的话 -->
    <div class="data-card message-card">
      <div class="section-title">💚 小安的话</div>
      <p class="message-text">{{ personalMessage }}</p>
    </div>

    <!-- 退出登录 -->
    <div class="data-card logout-card">
      <div class="section-title">🚪 退出登录</div>
      <p class="logout-hint">退出后需要重新登录才能继续使用</p>
      <button class="logout-btn" @click="handleLogout">
        退出登录
      </button>
    </div>
  </div>
</template>

<script>
import { getDBTSkills } from '@/api/emotion'
import { getUserInfo, updateUserInfo, changePassword, logout } from '@/api/auth'

export default {
  name: 'ProfileTab',
  data() {
    return {
      nickname: '',
      editingUsername: false,
      tempUsername: '',
      diaries: [],
      skills: [],
      skillsLoading: true,
      // 密码修改相关
      showPasswordForm: false,
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      showCurrentPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      passwordLoading: false,
      passwordError: '',
      passwordSuccess: ''
    }
  },
  computed: {
    // 使用天数
    joinDays() {
      if (this.diaries.length === 0) return 0

      // 找到最早的日记日期
      const sortedDiaries = [...this.diaries].sort((a, b) =>
        new Date(a.date) - new Date(b.date)
      )
      const firstDate = new Date(sortedDiaries[0].date)
      const today = new Date()

      // 计算天数差
      const diffTime = Math.abs(today - firstDate)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

      return diffDays
    },

    // 统计数据
    stats() {
      return {
        conversations: this.diaries.length, // 暂时用日记数量代替对话次数
        diaries: this.diaries.length,
        usageDays: this.joinDays
      }
    },

    // 最近7天的情绪分析
    recentEmotions() {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)

      return this.diaries.filter(diary =>
        new Date(diary.date) >= sevenDaysAgo
      )
    },

    // 智能生成的个性化消息
    personalMessage() {
      if (this.diaries.length === 0) {
        return '欢迎来到小安！开始记录你的第一篇日记，我会陪伴你一起成长。'
      }

      if (this.diaries.length < 3) {
        return `你已经记录了${this.diaries.length}篇日记，很棒的开始！坚持记录会帮助你更好地了解自己的情绪变化。`
      }

      // 分析最近的情绪趋势
      const recentEmotionTypes = this.recentEmotions.map(d => d.emotion)
      const emotionCounts = {}
      recentEmotionTypes.forEach(type => {
        emotionCounts[type] = (emotionCounts[type] || 0) + 1
      })

      // 找到最常见的情绪
      const mostCommonEmotion = Object.keys(emotionCounts).reduce((a, b) =>
        emotionCounts[a] > emotionCounts[b] ? a : b
      )

      const emotionMessages = {
        'joy': `这一周你的心情大多是开心的，记录了${emotionCounts['joy']}次快乐时刻。保持这份积极的状态，继续发现生活中的美好！`,
        'calm': `这一周你大部分时间都很平静，这是一个很好的状态。内心的平和是应对压力的基础。`,
        'sadness': `这一周你有${emotionCounts['sadness']}次感到难过。允许自己感受这些情绪是很重要的，我一直在这里陪伴你。`,
        'anxiety': `这一周你感到焦虑了${emotionCounts['anxiety']}次。我注意到了，让我们一起找到缓解焦虑的方法。记住，你并不孤单。`,
        'anger': `这一周你有${emotionCounts['anger']}次感到生气。愤怒是正常的情绪，重要的是找到合适的方式来表达它。`,
        'fear': `这一周你感到害怕了${emotionCounts['fear']}次。面对恐惧需要勇气，而你正在这样做。我为你感到骄傲。`
      }

      // 检查高强度情绪
      const highIntensityDiaries = this.recentEmotions.filter(d => d.intensity >= 7)
      if (highIntensityDiaries.length >= 3) {
        return `这一周我注意到你有${highIntensityDiaries.length}次情绪强度较高的记录。这段时间可能对你来说比较艰难，但你一直在坚持记录，这本身就是一种成长。如果需要，记得寻求专业帮助。`
      }

      return emotionMessages[mostCommonEmotion] || `你已经坚持记录了${this.diaries.length}篇日记，每一次记录都是对自己的关爱。继续加油！`
    },

    displayUsername() {
      if (this.nickname) return this.nickname
      
      const storedUserInfo = localStorage.getItem('userInfo')
      if (storedUserInfo) {
        try {
          const userInfo = JSON.parse(storedUserInfo)
          if (userInfo.nickname) return userInfo.nickname
          if (userInfo.username) return userInfo.username
        } catch (e) {
          console.error('解析用户信息失败:', e)
        }
      }
      
      return '同学'
    },

    // 密码强度计算
    passwordStrength() {
      const password = this.passwordForm.newPassword
      if (!password) return 0

      let strength = 0

      // 长度检查
      if (password.length >= 6) strength += 25
      if (password.length >= 8) strength += 25
      if (password.length >= 12) strength += 25

      // 复杂度检查
      if (/[a-z]/.test(password)) strength += 10
      if (/[A-Z]/.test(password)) strength += 10
      if (/[0-9]/.test(password)) strength += 10
      if (/[^a-zA-Z0-9]/.test(password)) strength += 15

      return Math.min(strength, 100)
    },

    passwordStrengthClass() {
      const strength = this.passwordStrength
      if (strength < 40) return 'weak'
      if (strength < 70) return 'medium'
      return 'strong'
    },

    passwordStrengthWidth() {
      return this.passwordStrength + '%'
    },

    passwordStrengthText() {
      const strength = this.passwordStrength
      if (strength < 40) return '弱'
      if (strength < 70) return '中等'
      return '强'
    },

    // 密码是否匹配
    passwordsMatch() {
      return this.passwordForm.newPassword === this.passwordForm.confirmPassword
    },

    // 是否可以提交表单
    canSubmitPassword() {
      return (
        this.passwordForm.currentPassword &&
        this.passwordForm.newPassword.length >= 6 &&
        this.passwordsMatch
      )
    }
  },
  methods: {
    async loadDBTSkills() {
      this.skillsLoading = true

      try {
        const response = await getDBTSkills()

        // 按分类分组技能
        const skillsByCategory = {}
        Object.entries(response.data).forEach(([skillName, skillData]) => {
          const category = skillData.category
          if (!skillsByCategory[category]) {
            skillsByCategory[category] = []
          }
          skillsByCategory[category].push({
            name: skillName,
            category: category,
            introduction: skillData.introduction
          })
        })

        // 转换为显示格式，每个分类统计进度
        const categoryMap = {
          'mindfulness': { name: '正念', icon: '🧘' },
          'emotion_regulation': { name: '情绪调节', icon: '💚' },
          'interpersonal': { name: '人际效能', icon: '🤝' },
          'distress_tolerance': { name: '痛苦耐受', icon: '🌊' }
        }

        this.skills = Object.entries(categoryMap).map(([key, value]) => {
          const categorySkills = skillsByCategory[key] || []
          // 这里可以根据实际学习记录计算进度，暂时使用随机进度
          const progress = Math.floor(Math.random() * 40) + 30 // 30-70之间

          return {
            name: value.name,
            icon: value.icon,
            progress: progress,
            skillCount: categorySkills.length
          }
        })

        console.log('✅ DBT技能加载成功，共', Object.keys(response.data).length, '个技能')
      } catch (error) {
        console.error('❌ 加载DBT技能失败:', error)
        // 回退到默认数据
        this.skills = [
          { name: '正念', icon: '🧘', progress: 0, skillCount: 0 },
          { name: '情绪调节', icon: '💚', progress: 0, skillCount: 0 },
          { name: '人际效能', icon: '🤝', progress: 0, skillCount: 0 },
          { name: '痛苦耐受', icon: '🌊', progress: 0, skillCount: 0 }
        ]
      } finally {
        this.skillsLoading = false
      }
    },

    async loadData() {
      try {
        const response = await getUserInfo()
        if (response.data && response.data.data) {
          const userInfo = response.data.data
          this.nickname = userInfo.nickname || userInfo.username || ''
          localStorage.setItem('user_nickname', this.nickname)
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        const storedNickname = localStorage.getItem('user_nickname')
        if (storedNickname) {
          this.nickname = storedNickname
        } else {
          const storedUserInfo = localStorage.getItem('userInfo')
          if (storedUserInfo) {
            try {
              const userInfo = JSON.parse(storedUserInfo)
              this.nickname = userInfo.nickname || userInfo.username || ''
              localStorage.setItem('user_nickname', this.nickname)
            } catch (e) {
              console.error('解析用户信息失败:', e)
            }
          }
        }
      }

      try {
        const stored = localStorage.getItem('emotion_diaries')
        if (stored) {
          this.diaries = JSON.parse(stored)
        }
      } catch (error) {
        console.error('加载日记数据失败:', error)
      }
    },

    startEditUsername() {
      this.editingUsername = true
      this.tempUsername = this.nickname || ''
      // 下一帧聚焦输入框
      this.$nextTick(() => {
        const input = this.$refs.usernameInput
        if (input) input.focus()
      })
    },

    async saveUsername() {
      const newName = this.tempUsername.trim()
      if (newName && newName !== this.nickname) {
        try {
          await updateUserInfo({ nickname: newName })
          this.nickname = newName
          localStorage.setItem('user_nickname', newName)
        } catch (error) {
          console.error('保存昵称失败:', error)
          this.nickname = newName
          localStorage.setItem('user_nickname', newName)
        }
      } else if (newName) {
        localStorage.setItem('user_nickname', newName)
      }
      this.editingUsername = false
    },

    cancelEditUsername() {
      this.editingUsername = false
      this.tempUsername = ''
    },

    // 处理密码修改
    async handleChangePassword() {
      this.passwordError = ''
      this.passwordSuccess = ''

      if (!this.passwordForm.currentPassword) {
        this.passwordError = '请输入当前密码'
        return
      }

      if (this.passwordForm.newPassword.length < 6) {
        this.passwordError = '新密码长度至少为6位'
        return
      }

      if (!this.passwordsMatch) {
        this.passwordError = '两次输入的新密码不一致'
        return
      }

      if (this.passwordForm.currentPassword === this.passwordForm.newPassword) {
        this.passwordError = '新密码不能与当前密码相同'
        return
      }

      this.passwordLoading = true

      try {
        await changePassword({
          currentPassword: this.passwordForm.currentPassword,
          newPassword: this.passwordForm.newPassword
        })

        this.passwordSuccess = '密码修改成功！'

        setTimeout(() => {
          this.resetPasswordForm()
        }, 3000)

      } catch (error) {
        console.error('密码修改失败:', error)
        this.passwordError = error.response?.data?.detail?.message || error.message || '密码修改失败，请检查当前密码是否正确'
      } finally {
        this.passwordLoading = false
      }
    },

    // 取消密码修改
    cancelPasswordChange() {
      this.resetPasswordForm()
    },

    // 重置密码表单
    resetPasswordForm() {
      this.showPasswordForm = false
      this.passwordForm = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
      this.showCurrentPassword = false
      this.showNewPassword = false
      this.showConfirmPassword = false
      this.passwordError = ''
      this.passwordSuccess = ''
    },

    // 跳转到情绪历史页面
    goToEmotionHistory() {
      this.$router.push('/emotion-history')
    },

    async handleLogout() {
      try {
        await logout()
      } catch (error) {
        console.error('退出登录失败:', error)
      }
      localStorage.removeItem('token')
      localStorage.removeItem('admin_token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('user_nickname')
      localStorage.removeItem('emotion_diaries')
      this.$router.push('/login')
    }
  },
  mounted() {
    this.loadData()
    this.loadDBTSkills()
  }
}
</script>

<style scoped>
.profile-tab {
  height: 100%;
  overflow-y: auto;
  background: transparent;
  padding: 20px;
}

/* ========== 个人信息头部 ========== */
.profile-header {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.8),
    rgba(255, 255, 255, 0.6)
  );
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 28px;
  padding: 40px;
  margin-bottom: 28px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 16px 48px rgba(76, 175, 80, 0.2), inset 0 2px 0 rgba(255, 255, 255, 1);
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar-container {
  position: relative;
}

.avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  border: 4px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 12px 32px rgba(76, 175, 80, 0.3), inset 0 3px 0 rgba(255, 255, 255, 0.6);
  background: linear-gradient(135deg, #66BB6A, #81C784);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 42px;
  filter: drop-shadow(0 4px 12px rgba(76, 175, 80, 0.3));
}

.avatar-ring {
  position: absolute;
  top: -6px;
  left: -6px;
  width: calc(100% + 12px);
  height: calc(100% + 12px);
  border-radius: 50%;
  background: linear-gradient(135deg,
    rgba(102, 187, 106, 0.7),
    rgba(129, 199, 132, 0.7)
  );
  z-index: -1;
  filter: blur(12px);
  opacity: 0.7;
  animation: ringPulse 4s ease-in-out infinite;
}

@keyframes ringPulse {
  0%, 100% {
    opacity: 0.7;
    transform: scale(1);
  }
  50% {
    opacity: 0.9;
    transform: scale(1.08);
  }
}

.profile-info {
  flex: 1;
}

/* ========== 昵称显示和编辑 ========== */
.nickname-display {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.nickname {
  font-size: 24px;
  font-weight: 700;
  color: #1B5E20;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.edit-nickname-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(129, 199, 132, 0.2);
  border-radius: 50%;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
}

.edit-nickname-btn:hover {
  background: rgba(129, 199, 132, 0.3);
  opacity: 1;
  transform: scale(1.1);
}

.nickname-edit {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.nickname-input {
  flex: 1;
  padding: 8px 12px;
  border: 2px solid rgba(102, 187, 106, 0.4);
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  color: #1B5E20;
  background: rgba(255, 255, 255, 0.9);
  outline: none;
  transition: all 0.2s ease;
}

.nickname-input:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.save-btn,
.cancel-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.save-btn {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
}

.save-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.cancel-btn {
  background: rgba(158, 158, 158, 0.2);
  color: #666;
}

.cancel-btn:hover {
  background: rgba(158, 158, 158, 0.3);
  transform: scale(1.1);
}

.user-stats {
  font-size: 14px;
  color: #388E3C;
}

.stat-value {
  color: #2E7D32;
  font-weight: 600;
  margin-right: 20px;
}

/* ========== 数据卡片 ========== */
.data-card {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.7),
    rgba(255, 255, 255, 0.5)
  );
  backdrop-filter: blur(25px) saturate(180%);
  -webkit-backdrop-filter: blur(25px) saturate(180%);
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 24px;
  padding: 32px;
  margin-bottom: 28px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 12px 40px rgba(76, 175, 80, 0.15), inset 0 2px 0 rgba(255, 255, 255, 0.9);
}

.section-title {
  color: #1B5E20;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 24px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* ========== 进度条 ========== */
.skill-item {
  margin-bottom: 24px;
}

.skill-item:last-child {
  margin-bottom: 0;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.skill-label {
  font-size: 15px;
  font-weight: 600;
  color: #2E7D32;
}

.skill-percentage {
  font-size: 15px;
  font-weight: 700;
  color: #4CAF50;
}

.progress-track {
  height: 12px;
  background: linear-gradient(90deg,
    rgba(129, 199, 132, 0.2),
    rgba(102, 187, 106, 0.15)
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(129, 199, 132, 0.3);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #81C784 0%, #66BB6A 50%, #4CAF50 100%);
  background-size: 200% 100%;
  border-radius: 6px;
  box-shadow: 0 3px 12px rgba(76, 175, 80, 0.5), inset 0 2px 0 rgba(255, 255, 255, 0.4);
  position: relative;
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
  animation: progressFlow 3s ease-in-out infinite;
}

@keyframes progressFlow {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

/* 光泽效果 */
.progress-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent,
    rgba(255, 255, 255, 0.6),
    transparent
  );
  animation: shimmer 2.5s ease-in-out infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 200%;
  }
}

/* ========== 小安的话 ========== */
.message-card {
  /* 继承 data-card 样式 */
}

.message-text {
  color: #333;
  font-size: 15px;
  line-height: 1.8;
  margin: 0;
}

/* 滚动条样式 */
.profile-tab::-webkit-scrollbar {
  width: 6px;
}

.profile-tab::-webkit-scrollbar-track {
  background: transparent;
}

.profile-tab::-webkit-scrollbar-thumb {
  background: rgba(76, 175, 80, 0.3);
  border-radius: 3px;
}

.profile-tab::-webkit-scrollbar-thumb:hover {
  background: rgba(76, 175, 80, 0.5);
}

/* ========== 修改密码 ========== */
.password-prompt {
  text-align: center;
  padding: 20px 0;
}

.prompt-text {
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
}

.change-password-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.change-password-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

.password-form {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 8px;
}

.password-input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 12px 40px 12px 16px;
  border: 2px solid rgba(76, 175, 80, 0.3);
  border-radius: 12px;
  font-size: 15px;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #4CAF50;
  background: white;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.toggle-password {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 8px;
  transition: opacity 0.2s ease;
  opacity: 0.6;
}

.toggle-password:hover {
  opacity: 1;
}

/* 密码强度指示器 */
.password-strength {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.strength-bar {
  flex: 1;
  height: 6px;
  background: rgba(158, 158, 158, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.strength-fill.weak {
  background: linear-gradient(90deg, #EF5350, #F44336);
  width: 33%;
}

.strength-fill.medium {
  background: linear-gradient(90deg, #FFA726, #FF9800);
  width: 66%;
}

.strength-fill.strong {
  background: linear-gradient(90deg, #66BB6A, #4CAF50);
  width: 100%;
}

.strength-text {
  font-size: 12px;
  font-weight: 600;
  min-width: 40px;
}

.strength-text.weak {
  color: #F44336;
}

.strength-text.medium {
  color: #FF9800;
}

.strength-text.strong {
  color: #4CAF50;
}

/* 密码匹配提示 */
.password-match-hint {
  margin-top: 6px;
  font-size: 13px;
  font-weight: 600;
}

.match-success {
  color: #4CAF50;
}

.match-error {
  color: #F44336;
}

/* 错误和成功消息 */
.error-message {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  color: #D32F2F;
  font-size: 14px;
}

.success-message {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  color: #2E7D32;
  font-size: 14px;
  font-weight: 600;
}

/* 按钮组 */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.submit-btn {
  flex: 1;
  padding: 14px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.cancel-btn-form {
  padding: 14px 24px;
  background: rgba(158, 158, 158, 0.2);
  color: #666;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn-form:hover {
  background: rgba(158, 158, 158, 0.3);
}

/* ========== 快捷入口 ========== */
.quick-links {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quick-link-btn {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(129, 199, 132, 0.1);
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  width: 100%;
}

.quick-link-btn:hover {
  background: rgba(129, 199, 132, 0.2);
  border-color: rgba(76, 175, 80, 0.4);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
}

.link-icon {
  font-size: 32px;
  line-height: 1;
}

.link-info {
  flex: 1;
}

.link-title {
  font-size: 16px;
  font-weight: 700;
  color: #2E7D32;
  margin-bottom: 4px;
}

.link-desc {
  font-size: 13px;
  color: #666;
}

.link-arrow {
  font-size: 24px;
  color: #4CAF50;
  opacity: 0.6;
  transition: all 0.3s ease;
}

.quick-link-btn:hover .link-arrow {
  opacity: 1;
  transform: translateX(4px);
}

/* ========== 退出登录 ========== */
.logout-card {
  border-color: rgba(244, 67, 54, 0.2);
}

.logout-hint {
  color: #999;
  font-size: 14px;
  margin-bottom: 16px;
}

.logout-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #EF5350, #F44336);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(244, 67, 54, 0.4);
}

.logout-btn:active {
  transform: scale(0.98);
}
</style>
