<template>
  <Transition name="modal-fade">
    <div v-if="visible && diary" class="detail-modal-overlay" @click="handleClose">
      <div class="detail-modal" @click.stop>
        <!-- 头部 -->
        <div class="detail-header">
          <button class="back-btn" @click="handleClose">← 返回</button>
          <button class="close-btn" @click="handleClose">✕</button>
        </div>

        <!-- 日期和情绪 -->
        <div class="detail-info">
          <div class="detail-date">{{ diary.date }}</div>
          <div class="emotion-badge">
            <span class="emotion-emoji-large">{{ diary.emoji }}</span>
            <span class="emotion-label-large">{{ diary.emotionLabel }}</span>
          </div>
        </div>

        <!-- 情绪强度 -->
        <div class="intensity-display" v-if="diary.intensity">
          <div class="intensity-label">情绪强度</div>
          <div class="intensity-bar-wrapper">
            <div class="intensity-bar" :style="{ width: (diary.intensity * 10) + '%', background: intensityColor }"></div>
          </div>
          <div class="intensity-text">{{ diary.intensity }}/10</div>
        </div>

        <!-- 日记内容 -->
        <div class="detail-content">
          <div class="content-label">📝 记录</div>
          <div class="content-text">{{ diary.content }}</div>
        </div>

        <!-- 时间戳 -->
        <div class="detail-timestamp">
          记录于 {{ formatTime(diary.date) }}
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'DiaryDetailModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    diary: {
      type: Object,
      default: null
    }
  },
  emits: ['close'],
  computed: {
    intensityColor() {
      if (!this.diary || !this.diary.intensity) return '#4CAF50'
      const value = this.diary.intensity
      if (value <= 3) return '#4CAF50'
      if (value <= 6) return '#FF9800'
      return '#F44336'
    }
  },
  methods: {
    handleClose() {
      this.$emit('close')
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      return `${hours}:${minutes}`
    }
  }
}
</script>

<style scoped>
/* ========== 遮罩层 ========== */
.detail-modal-overlay {
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
.detail-modal {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.95),
    rgba(255, 255, 255, 0.9)
  );
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border: 2px solid rgba(102, 187, 106, 0.3);
  border-radius: 28px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 32px;
  box-shadow: 0 24px 80px rgba(46, 125, 50, 0.3), inset 0 2px 0 rgba(255, 255, 255, 1);
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
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.back-btn {
  padding: 8px 16px;
  background: rgba(129, 199, 132, 0.15);
  border: 1px solid rgba(102, 187, 106, 0.3);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(129, 199, 132, 0.25);
  transform: translateX(-2px);
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(158, 158, 158, 0.15);
  border-radius: 50%;
  font-size: 20px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(158, 158, 158, 0.25);
  transform: scale(1.1);
}

/* ========== 信息区 ========== */
.detail-info {
  text-align: center;
  margin-bottom: 32px;
}

.detail-date {
  font-size: 18px;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 16px;
}

.emotion-badge {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg,
    rgba(129, 199, 132, 0.2),
    rgba(102, 187, 106, 0.15)
  );
  border: 2px solid rgba(102, 187, 106, 0.3);
  border-radius: 20px;
  padding: 20px 40px;
}

.emotion-emoji-large {
  font-size: 64px;
}

.emotion-label-large {
  font-size: 20px;
  font-weight: 700;
  color: #2E7D32;
}

/* ========== 情绪强度显示 ========== */
.intensity-display {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(129, 199, 132, 0.2);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 24px;
}

.intensity-label {
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 8px;
}

.intensity-bar-wrapper {
  height: 12px;
  background: rgba(200, 200, 200, 0.3);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 8px;
}

.intensity-bar {
  height: 100%;
  border-radius: 6px;
  transition: width 0.5s ease, background 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.intensity-text {
  text-align: right;
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
}

/* ========== 内容区 ========== */
.detail-content {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(129, 199, 132, 0.2);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.content-label {
  font-size: 15px;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 12px;
}

.content-text {
  font-size: 15px;
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* ========== 时间戳 ========== */
.detail-timestamp {
  text-align: center;
  font-size: 13px;
  color: #999;
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
.detail-modal::-webkit-scrollbar {
  width: 6px;
}

.detail-modal::-webkit-scrollbar-track {
  background: transparent;
}

.detail-modal::-webkit-scrollbar-thumb {
  background: rgba(76, 175, 80, 0.3);
  border-radius: 3px;
}

.detail-modal::-webkit-scrollbar-thumb:hover {
  background: rgba(76, 175, 80, 0.5);
}

/* ========== 响应式 ========== */
@media (max-width: 640px) {
  .detail-modal {
    padding: 24px;
  }

  .emotion-emoji-large {
    font-size: 48px;
  }

  .emotion-label-large {
    font-size: 18px;
  }
}
</style>
