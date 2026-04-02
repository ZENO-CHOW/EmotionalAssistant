<template>
  <Transition name="modal-fade">
    <div v-if="visible && user" class="user-detail-modal-overlay" @click="handleClose">
      <div class="user-detail-modal" @click.stop>
        <!-- 头部 -->
        <div class="modal-header">
          <h2 class="modal-title">用户详情</h2>
          <button class="close-btn" @click="handleClose">✕</button>
        </div>

        <!-- 用户基本信息 -->
        <div class="user-basic-info">
          <div class="user-avatar-large">{{ user.name.charAt(0) }}</div>
          <div class="user-info-text">
            <h3 class="user-name-large">{{ user.name }}</h3>
            <p class="user-id-text">ID: {{ user.id }}</p>
            <p class="user-email-text">{{ user.email }}</p>
          </div>
          <div class="risk-indicator" :class="user.riskLevel">
            {{ getRiskText(user.riskLevel) }}
          </div>
        </div>

        <!-- 统计数据 -->
        <div class="stats-grid">
          <div class="stat-box">
            <div class="stat-icon">📝</div>
            <div class="stat-number">{{ user.emotionCount || 0 }}</div>
            <div class="stat-label">情绪记录</div>
          </div>
          <div class="stat-box">
            <div class="stat-icon">📅</div>
            <div class="stat-number">{{ getDays(user.registerTime) }}</div>
            <div class="stat-label">使用天数</div>
          </div>
          <div class="stat-box">
            <div class="stat-icon">🕐</div>
            <div class="stat-number">{{ user.lastActive || '未知' }}</div>
            <div class="stat-label">最后活跃</div>
          </div>
        </div>

        <!-- 详细信息 -->
        <div class="detail-sections">
          <div class="detail-section">
            <h4 class="section-title">📊 情绪趋势</h4>
            <div class="emotion-trend">
              <p class="placeholder-text">近期情绪数据加载中...</p>
            </div>
          </div>

          <div class="detail-section">
            <h4 class="section-title">⚠️ 风险评估</h4>
            <div class="risk-assessment">
              <div class="risk-item">
                <span class="risk-item-label">风险等级：</span>
                <span class="risk-badge" :class="user.riskLevel">
                  {{ getRiskText(user.riskLevel) }}
                </span>
              </div>
              <div class="risk-item">
                <span class="risk-item-label">活跃状态：</span>
                <span class="status-badge" :class="user.status">
                  {{ getStatusText(user.status) }}
                </span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4 class="section-title">📌 系统信息</h4>
            <div class="system-info">
              <div class="info-row">
                <span class="info-label">注册时间：</span>
                <span class="info-value">{{ user.registerTime }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">账号状态：</span>
                <span class="info-value">{{ user.status === 'active' ? '正常' : '非活跃' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="modal-footer">
          <button class="footer-btn secondary" @click="handleClose">
            关闭
          </button>
          <button class="footer-btn primary" @click="viewFullHistory">
            查看完整记录
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'UserDetailModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    user: {
      type: Object,
      default: null
    }
  },
  emits: ['close'],
  methods: {
    handleClose() {
      this.$emit('close')
    },

    getRiskText(level) {
      const map = {
        high: '高危',
        medium: '中危',
        low: '低危'
      }
      return map[level] || '未知'
    },

    getStatusText(status) {
      const map = {
        active: '活跃',
        inactive: '非活跃'
      }
      return map[status] || '未知'
    },

    getDays(registerTime) {
      if (!registerTime) return 0
      const reg = new Date(registerTime)
      const now = new Date()
      const diff = now - reg
      return Math.floor(diff / (1000 * 60 * 60 * 24))
    },

    viewFullHistory() {
      // 跳转到用户完整记录页面
      this.$router.push(`/admin/users/${this.user.id}/history`)
      this.handleClose()
    }
  }
}
</script>

<style scoped>
/* ========== 遮罩层 ========== */
.user-detail-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* ========== 弹窗主体 ========== */
.user-detail-modal {
  background: white;
  border-radius: 20px;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.3);
  animation: modalSlideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* ========== 头部 ========== */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 32px;
  border-bottom: 1px solid #f1f5f9;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #f1f5f9;
  border-radius: 50%;
  font-size: 20px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: #e2e8f0;
  transform: scale(1.1);
}

/* ========== 用户基本信息 ========== */
.user-basic-info {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 32px;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
}

.user-avatar-large {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 36px;
  font-weight: 700;
  flex-shrink: 0;
}

.user-info-text {
  flex: 1;
}

.user-name-large {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.user-id-text {
  font-size: 14px;
  color: #64748b;
  font-family: 'Monaco', monospace;
  margin-bottom: 2px;
}

.user-email-text {
  font-size: 14px;
  color: #94a3b8;
}

.risk-indicator {
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.risk-indicator.high {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
}

.risk-indicator.medium {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
}

.risk-indicator.low {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
}

/* ========== 统计数据 ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 24px 32px;
  border-bottom: 1px solid #f1f5f9;
}

.stat-box {
  text-align: center;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
}

/* ========== 详细信息 ========== */
.detail-sections {
  padding: 24px 32px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #334155;
  margin-bottom: 12px;
}

.emotion-trend {
  padding: 32px;
  background: #f8fafc;
  border-radius: 12px;
  text-align: center;
}

.placeholder-text {
  color: #94a3b8;
  font-size: 14px;
}

.risk-assessment {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.risk-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 10px;
}

.risk-item-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.risk-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.risk-badge.high {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
}

.risk-badge.medium {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
}

.risk-badge.low {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
}

.status-badge.inactive {
  background: rgba(148, 163, 184, 0.15);
  color: #64748b;
}

.system-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 10px;
}

.info-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.info-value {
  font-size: 14px;
  color: #334155;
  font-weight: 600;
}

/* ========== 底部 ========== */
.modal-footer {
  display: flex;
  gap: 12px;
  padding: 24px 32px;
  border-top: 1px solid #f1f5f9;
}

.footer-btn {
  flex: 1;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.footer-btn.secondary {
  background: #f1f5f9;
  color: #64748b;
}

.footer-btn.secondary:hover {
  background: #e2e8f0;
}

.footer-btn.primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.footer-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.5);
}

/* ========== 过渡动画 ========== */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* ========== 滚动条 ========== */
.user-detail-modal::-webkit-scrollbar {
  width: 6px;
}

.user-detail-modal::-webkit-scrollbar-track {
  background: transparent;
}

.user-detail-modal::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

/* ========== 响应式 ========== */
@media (max-width: 640px) {
  .user-basic-info {
    flex-direction: column;
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .modal-footer {
    flex-direction: column;
  }
}
</style>
