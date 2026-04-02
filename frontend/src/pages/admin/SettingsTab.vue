<template>
  <div class="settings-tab">
    <!-- 页面标题 -->
    <div class="settings-header">
      <h2 class="settings-title">系统设置</h2>
      <p class="settings-subtitle">配置系统参数和危机预警规则</p>
    </div>

    <!-- 设置分组 -->
    <div class="settings-sections">
      <!-- 危机预警设置 -->
      <div class="settings-section">
        <div class="section-header">
          <div class="section-title-row">
            <span class="section-icon">🚨</span>
            <h3 class="section-title">危机预警设置</h3>
          </div>
          <p class="section-desc">配置危机预警的触发条件和阈值</p>
        </div>

        <div class="section-content">
          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">情绪强度阈值</label>
              <p class="setting-help">当用户情绪强度达到此值时触发预警</p>
            </div>
            <div class="setting-control">
              <input
                v-model.number="settings.crisis.intensityThreshold"
                type="number"
                min="1"
                max="10"
                class="number-input"
              />
              <span class="unit-text">/10</span>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">连续触发次数</label>
              <p class="setting-help">在时间窗口内触发多少次后升级为高危</p>
            </div>
            <div class="setting-control">
              <input
                v-model.number="settings.crisis.triggerCount"
                type="number"
                min="1"
                max="10"
                class="number-input"
              />
              <span class="unit-text">次</span>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">时间窗口</label>
              <p class="setting-help">统计触发次数的时间范围</p>
            </div>
            <div class="setting-control">
              <select v-model="settings.crisis.timeWindow" class="select-input">
                <option value="1">1小时</option>
                <option value="3">3小时</option>
                <option value="6">6小时</option>
                <option value="12">12小时</option>
                <option value="24">24小时</option>
              </select>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">关键词监控</label>
              <p class="setting-help">检测到这些关键词时自动触发预警</p>
            </div>
            <div class="setting-control full-width">
              <div class="keyword-tags">
                <span
                  v-for="(keyword, index) in settings.crisis.keywords"
                  :key="index"
                  class="keyword-tag"
                >
                  {{ keyword }}
                  <button
                    class="keyword-remove"
                    @click="removeKeyword(index)"
                  >
                    ×
                  </button>
                </span>
                <input
                  v-model="newKeyword"
                  type="text"
                  class="keyword-input"
                  placeholder="输入关键词后按回车"
                  @keypress.enter="addKeyword"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 通知设置 -->
      <div class="settings-section">
        <div class="section-header">
          <div class="section-title-row">
            <span class="section-icon">🔔</span>
            <h3 class="section-title">通知设置</h3>
          </div>
          <p class="section-desc">配置管理员通知方式和频率</p>
        </div>

        <div class="section-content">
          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">邮件通知</label>
              <p class="setting-help">发生危机事件时发送邮件通知</p>
            </div>
            <div class="setting-control">
              <label class="toggle-switch">
                <input
                  v-model="settings.notification.emailEnabled"
                  type="checkbox"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="setting-item" v-if="settings.notification.emailEnabled">
            <div class="setting-label-group">
              <label class="setting-label">通知邮箱</label>
              <p class="setting-help">接收通知的管理员邮箱地址</p>
            </div>
            <div class="setting-control full-width">
              <input
                v-model="settings.notification.email"
                type="email"
                class="text-input"
                placeholder="admin@example.com"
              />
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">短信通知</label>
              <p class="setting-help">紧急情况下发送短信通知</p>
            </div>
            <div class="setting-control">
              <label class="toggle-switch">
                <input
                  v-model="settings.notification.smsEnabled"
                  type="checkbox"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="setting-item" v-if="settings.notification.smsEnabled">
            <div class="setting-label-group">
              <label class="setting-label">通知手机</label>
              <p class="setting-help">接收短信的手机号码</p>
            </div>
            <div class="setting-control full-width">
              <input
                v-model="settings.notification.phone"
                type="tel"
                class="text-input"
                placeholder="13800138000"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 数据保留设置 -->
      <div class="settings-section">
        <div class="section-header">
          <div class="section-title-row">
            <span class="section-icon">💾</span>
            <h3 class="section-title">数据保留</h3>
          </div>
          <p class="section-desc">配置用户数据的保留期限</p>
        </div>

        <div class="section-content">
          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">情绪记录保留期</label>
              <p class="setting-help">情绪分析记录自动删除期限</p>
            </div>
            <div class="setting-control">
              <select v-model.number="settings.retention.emotionData" class="select-input">
                <option :value="90">3个月</option>
                <option :value="180">6个月</option>
                <option :value="365">1年</option>
                <option :value="730">2年</option>
                <option :value="-1">永久保留</option>
              </select>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">日记保留期</label>
              <p class="setting-help">用户日记自动删除期限</p>
            </div>
            <div class="setting-control">
              <select v-model.number="settings.retention.diaryData" class="select-input">
                <option :value="180">6个月</option>
                <option :value="365">1年</option>
                <option :value="730">2年</option>
                <option :value="-1">永久保留</option>
              </select>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">非活跃用户清理</label>
              <p class="setting-help">超过此期限未登录的用户将被标记</p>
            </div>
            <div class="setting-control">
              <select v-model.number="settings.retention.inactiveUser" class="select-input">
                <option :value="90">3个月</option>
                <option :value="180">6个月</option>
                <option :value="365">1年</option>
                <option :value="-1">不清理</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- 系统参数 -->
      <div class="settings-section">
        <div class="section-header">
          <div class="section-title-row">
            <span class="section-icon">⚙️</span>
            <h3 class="section-title">系统参数</h3>
          </div>
          <p class="section-desc">配置系统运行参数</p>
        </div>

        <div class="section-content">
          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">用户注册</label>
              <p class="setting-help">是否允许新用户注册</p>
            </div>
            <div class="setting-control">
              <label class="toggle-switch">
                <input
                  v-model="settings.system.allowRegistration"
                  type="checkbox"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-label-group">
              <label class="setting-label">维护模式</label>
              <p class="setting-help">开启后用户将无法访问系统</p>
            </div>
            <div class="setting-control">
              <label class="toggle-switch">
                <input
                  v-model="settings.system.maintenanceMode"
                  type="checkbox"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 保存按钮 -->
    <div class="settings-footer">
      <button class="reset-btn" @click="resetSettings">
        恢复默认
      </button>
      <button class="save-btn" @click="saveSettings" :disabled="saving">
        {{ saving ? '保存中...' : '保存设置' }}
      </button>
    </div>

    <!-- 成功提示 -->
    <Transition name="toast-fade">
      <div v-if="showSuccess" class="success-toast">
        ✅ 设置已保存
      </div>
    </Transition>
  </div>
</template>

<script>
import { getSystemSettings, updateSystemSettings } from '@/api/admin.js'

export default {
  name: 'SettingsTab',
  data() {
    return {
      settings: {
        crisis: {
          intensityThreshold: 7,
          triggerCount: 3,
          timeWindow: 24,
          keywords: ['自杀', '结束生命', '自我伤害', '无法坚持', '放弃活着']
        },
        notification: {
          emailEnabled: true,
          email: 'admin@example.com',
          smsEnabled: false,
          phone: ''
        },
        retention: {
          emotionData: 365,
          diaryData: 730,
          inactiveUser: 180
        },
        system: {
          allowRegistration: true,
          maintenanceMode: false
        }
      },
      newKeyword: '',
      saving: false,
      showSuccess: false
    }
  },
  methods: {
    async loadSettings() {
      try {
        const response = await getSystemSettings()
        this.settings = response.data
      } catch (error) {
        console.error('加载设置失败:', error)
      }
    },

    async saveSettings() {
      this.saving = true
      try {
        await updateSystemSettings(this.settings)
        this.showSuccessToast()
      } catch (error) {
        console.error('保存设置失败:', error)
        alert('保存失败，请稍后重试')
      } finally {
        this.saving = false
      }
    },

    resetSettings() {
      if (!confirm('确定要恢复默认设置吗？')) return

      this.settings = {
        crisis: {
          intensityThreshold: 7,
          triggerCount: 3,
          timeWindow: 24,
          keywords: ['自杀', '结束生命', '自我伤害', '无法坚持', '放弃活着']
        },
        notification: {
          emailEnabled: true,
          email: 'admin@example.com',
          smsEnabled: false,
          phone: ''
        },
        retention: {
          emotionData: 365,
          diaryData: 730,
          inactiveUser: 180
        },
        system: {
          allowRegistration: true,
          maintenanceMode: false
        }
      }
    },

    addKeyword() {
      const keyword = this.newKeyword.trim()
      if (keyword && !this.settings.crisis.keywords.includes(keyword)) {
        this.settings.crisis.keywords.push(keyword)
        this.newKeyword = ''
      }
    },

    removeKeyword(index) {
      this.settings.crisis.keywords.splice(index, 1)
    },

    showSuccessToast() {
      this.showSuccess = true
      setTimeout(() => {
        this.showSuccess = false
      }, 3000)
    }
  },
  mounted() {
    this.loadSettings()
  }
}
</script>

<style scoped>
.settings-tab {
  max-width: 900px;
  margin: 0 auto;
  padding-bottom: 100px;
}

/* ========== 页面头部 ========== */
.settings-header {
  margin-bottom: 32px;
}

.settings-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.settings-subtitle {
  font-size: 14px;
  color: #64748b;
}

/* ========== 设置分组 ========== */
.settings-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.settings-section {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.section-header {
  padding: 24px;
  border-bottom: 1px solid #f1f5f9;
}

.section-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.section-icon {
  font-size: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.section-desc {
  font-size: 13px;
  color: #64748b;
  margin-left: 36px;
}

.section-content {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========== 设置项 ========== */
.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.setting-label-group {
  flex: 1;
}

.setting-label {
  display: block;
  font-size: 15px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 4px;
}

.setting-help {
  font-size: 13px;
  color: #64748b;
  line-height: 1.4;
}

.setting-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.setting-control.full-width {
  width: 100%;
}

.number-input,
.select-input,
.text-input {
  padding: 10px 14px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  color: #334155;
  background: white;
  transition: all 0.2s ease;
}

.number-input {
  width: 80px;
}

.select-input {
  min-width: 140px;
}

.text-input {
  width: 100%;
}

.number-input:focus,
.select-input:focus,
.text-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.unit-text {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

/* ========== 开关按钮 ========== */
.toggle-switch {
  position: relative;
  width: 52px;
  height: 28px;
  cursor: pointer;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #cbd5e1;
  border-radius: 28px;
  transition: all 0.3s ease;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  width: 22px;
  height: 22px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-switch input:checked + .toggle-slider {
  background: linear-gradient(135deg, #10b981, #059669);
}

.toggle-switch input:checked + .toggle-slider::before {
  transform: translateX(24px);
}

/* ========== 关键词标签 ========== */
.keyword-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
  padding: 12px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
}

.keyword-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.keyword-remove {
  background: none;
  border: none;
  color: #dc2626;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  padding: 0;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.keyword-remove:hover {
  background: rgba(239, 68, 68, 0.2);
}

.keyword-input {
  flex: 1;
  min-width: 120px;
  border: none;
  outline: none;
  font-size: 14px;
  color: #334155;
}

/* ========== 底部按钮 ========== */
.settings-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: white;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: center;
  gap: 16px;
  z-index: 50;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.05);
}

.reset-btn,
.save-btn {
  padding: 14px 32px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-btn {
  background: #f1f5f9;
  color: #64748b;
}

.reset-btn:hover {
  background: #e2e8f0;
}

.save-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.5);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #9ca3af;
  box-shadow: none;
}

/* ========== 成功提示 ========== */
.success-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
  z-index: 9999;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.3s ease;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .setting-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .setting-control {
    width: 100%;
  }

  .settings-footer {
    flex-direction: column;
  }

  .reset-btn,
  .save-btn {
    width: 100%;
  }
}
</style>
