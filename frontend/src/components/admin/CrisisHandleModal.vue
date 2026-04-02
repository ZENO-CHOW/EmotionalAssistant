<template>
  <Transition name="modal-fade">
    <div v-if="visible && crisis" class="handle-modal-overlay" @click="handleClose">
      <div class="handle-modal" @click.stop>
        <!-- 头部 -->
        <div class="modal-header">
          <h2 class="modal-title">处理危机事件</h2>
          <button class="close-btn" @click="handleClose">✕</button>
        </div>

        <!-- 危机信息 -->
        <div class="crisis-info-section">
          <div class="info-row">
            <span class="info-label">用户：</span>
            <span class="info-value">{{ crisis.userName }} (ID: {{ crisis.userId }})</span>
          </div>
          <div class="info-row">
            <span class="info-label">风险等级：</span>
            <span class="risk-badge" :class="crisis.level">
              {{ getLevelText(crisis.level) }}
            </span>
          </div>
          <div class="info-row full-width">
            <span class="info-label">危机描述：</span>
            <p class="crisis-desc-text">{{ crisis.description }}</p>
          </div>
        </div>

        <!-- 处理表单 -->
        <form class="handle-form" @submit.prevent="handleSubmit">
          <div class="form-group">
            <label class="form-label">处理措施 *</label>
            <textarea
              v-model="form.action"
              class="form-textarea"
              placeholder="请详细描述您采取的处理措施&#10;例如：已电话联系用户，了解其当前状态；建议用户前往心理咨询中心；已通知辅导员跟进..."
              rows="5"
              required
            ></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">处理结果 *</label>
            <select v-model="form.result" class="form-select" required>
              <option value="">请选择处理结果</option>
              <option value="resolved">已解决</option>
              <option value="following">持续跟进中</option>
              <option value="escalated">已上报</option>
              <option value="referred">已转介</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">后续建议</label>
            <textarea
              v-model="form.followup"
              class="form-textarea"
              placeholder="后续跟进建议（选填）"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="form.notifyUser" type="checkbox" />
              <span>通知用户已处理</span>
            </label>
          </div>

          <div class="form-actions">
            <button type="button" class="form-btn cancel" @click="handleClose">
              取消
            </button>
            <button type="submit" class="form-btn submit" :disabled="!canSubmit">
              确认处理
            </button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'CrisisHandleModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    crisis: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'confirm'],
  data() {
    return {
      form: {
        action: '',
        result: '',
        followup: '',
        notifyUser: true
      }
    }
  },
  computed: {
    canSubmit() {
      return this.form.action.trim().length > 0 && this.form.result
    }
  },
  methods: {
    handleClose() {
      this.$emit('close')
      this.resetForm()
    },

    handleSubmit() {
      if (!this.canSubmit) return

      const handleData = {
        crisisId: this.crisis.id,
        action: this.form.action,
        result: this.form.result,
        followup: this.form.followup,
        notifyUser: this.form.notifyUser,
        handledBy: '管理员', // TODO: 从登录信息获取
        handledTime: new Date().toISOString()
      }

      this.$emit('confirm', handleData)
      this.handleClose()
    },

    resetForm() {
      this.form = {
        action: '',
        result: '',
        followup: '',
        notifyUser: true
      }
    },

    getLevelText(level) {
      const texts = {
        critical: '紧急',
        high: '高危',
        medium: '中危'
      }
      return texts[level] || '未知'
    }
  }
}
</script>

<style scoped>
/* ========== 遮罩层 ========== */
.handle-modal-overlay {
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
.handle-modal {
  background: white;
  border-radius: 20px;
  max-width: 600px;
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

/* ========== 危机信息区 ========== */
.crisis-info-section {
  padding: 24px 32px;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-row.full-width {
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.info-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 600;
}

.info-value {
  font-size: 14px;
  color: #1e293b;
  font-weight: 600;
}

.risk-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
}

.risk-badge.critical {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
}

.risk-badge.high {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
}

.risk-badge.medium {
  background: rgba(249, 115, 22, 0.15);
  color: #ea580c;
}

.crisis-desc-text {
  font-size: 14px;
  line-height: 1.6;
  color: #334155;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border-left: 3px solid #ef4444;
  width: 100%;
}

/* ========== 表单 ========== */
.handle-form {
  padding: 24px 32px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 8px;
}

.form-textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #334155;
  font-family: inherit;
  resize: vertical;
  transition: all 0.2s ease;
}

.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.form-select {
  width: 100%;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #334155;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
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

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.form-btn {
  flex: 1;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.form-btn.cancel {
  background: #f1f5f9;
  color: #64748b;
}

.form-btn.cancel:hover {
  background: #e2e8f0;
}

.form-btn.submit {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.form-btn.submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.5);
}

.form-btn.submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #9ca3af;
  box-shadow: none;
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
.handle-modal::-webkit-scrollbar {
  width: 6px;
}

.handle-modal::-webkit-scrollbar-track {
  background: transparent;
}

.handle-modal::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

/* ========== 响应式 ========== */
@media (max-width: 640px) {
  .form-actions {
    flex-direction: column;
  }
}
</style>
