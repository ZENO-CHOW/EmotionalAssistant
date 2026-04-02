<template>
  <Transition name="modal-fade">
    <div v-if="visible" class="diary-modal-overlay" @click="handleOverlayClick">
      <div class="diary-modal" @click.stop>
        <!-- 头部 -->
        <div class="diary-header">
          <h2 class="diary-title">📝 记录今天</h2>
          <button class="close-btn" @click="handleClose">✕</button>
        </div>

        <!-- 日期显示 -->
        <div class="date-display">
          <span class="date-icon">📅</span>
          <span class="date-text">{{ formattedDate }}</span>
        </div>

        <!-- 情绪选择 -->
        <div class="form-section">
          <label class="section-label">今天的心情</label>
          <div class="emotion-grid">
            <div
              v-for="emotion in emotions"
              :key="emotion.type"
              class="emotion-option"
              :class="{ selected: selectedEmotion === emotion.type }"
              @click="selectEmotion(emotion.type)"
            >
              <div class="emotion-emoji">{{ emotion.emoji }}</div>
              <div class="emotion-label">{{ emotion.label }}</div>
            </div>
          </div>
        </div>

        <!-- 情绪强度 -->
        <div class="form-section">
          <label class="section-label">
            情绪强度
            <span class="intensity-value">{{ intensity }}/10</span>
          </label>
          <input
            type="range"
            class="intensity-slider"
            :min="0"
            :max="10"
            v-model.number="intensity"
            :style="intensitySliderStyle"
          />
        </div>

        <!-- 文字记录 -->
        <div class="form-section">
          <label class="section-label">
            今天发生了什么？
            <span class="char-count">{{ content.length }}/500</span>
          </label>
          <textarea
            v-model="content"
            class="diary-textarea"
            placeholder="记录下今天的心情、想法、发生的事情...&#10;&#10;你可以写下：&#10;• 今天遇到了什么事&#10;• 当时的感受是什么&#10;• 现在想对自己说的话"
            maxlength="500"
            rows="8"
          ></textarea>
        </div>

        <!-- 操作按钮 -->
        <div class="diary-actions">
          <button class="action-btn secondary" @click="handleClose">
            取消
          </button>
          <button
            class="action-btn primary"
            :disabled="!canSave"
            @click="handleSave"
          >
            💾 保存日记
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'DiaryRecordForm',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    // 如果是编辑模式，传入日记数据
    diaryData: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'save'],
  data() {
    return {
      selectedEmotion: '',
      intensity: 5,
      content: '',
      emotions: [
        { type: 'joy', emoji: '😊', label: '开心' },
        { type: 'calm', emoji: '😌', label: '平静' },
        { type: 'sadness', emoji: '😢', label: '难过' },
        { type: 'anxiety', emoji: '😰', label: '焦虑' },
        { type: 'anger', emoji: '😠', label: '生气' },
        { type: 'fear', emoji: '😨', label: '害怕' }
      ]
    }
  },
  computed: {
    formattedDate() {
      const now = new Date()
      const month = now.getMonth() + 1
      const date = now.getDate()
      const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
      const weekday = weekdays[now.getDay()]
      return `${month}月${date}日 ${weekday}`
    },
    canSave() {
      return this.selectedEmotion && this.content.trim().length > 0
    },
    intensitySliderStyle() {
      const percent = (this.intensity / 10) * 100
      let color = '#4CAF50'
      if (this.intensity > 6) {
        color = '#F44336'
      } else if (this.intensity > 3) {
        color = '#FF9800'
      }
      return {
        background: `linear-gradient(to right, ${color} 0%, ${color} ${percent}%, #ddd ${percent}%)`
      }
    }
  },
  watch: {
    visible(newVal) {
      if (newVal) {
        // 弹窗打开时，加载数据（如果是编辑模式）
        if (this.diaryData) {
          this.loadDiaryData()
        } else {
          this.resetForm()
        }
      }
    }
  },
  methods: {
    selectEmotion(type) {
      this.selectedEmotion = type
    },

    handleClose() {
      this.$emit('close')
    },

    handleOverlayClick() {
      // 点击遮罩关闭
      this.handleClose()
    },

    handleSave() {
      if (!this.canSave) return

      const diaryEntry = {
        date: new Date().toISOString(),
        emotion: this.selectedEmotion,
        emotionLabel: this.emotions.find(e => e.type === this.selectedEmotion)?.label,
        emoji: this.emotions.find(e => e.type === this.selectedEmotion)?.emoji,
        intensity: this.intensity,
        content: this.content.trim()
      }

      this.$emit('save', diaryEntry)
      this.resetForm()
    },

    resetForm() {
      this.selectedEmotion = ''
      this.intensity = 5
      this.content = ''
    },

    loadDiaryData() {
      if (!this.diaryData) return
      this.selectedEmotion = this.diaryData.emotion
      this.intensity = this.diaryData.intensity
      this.content = this.diaryData.content
    }
  }
}
</script>

<style scoped>
/* ========== 遮罩层 ========== */
.diary-modal-overlay {
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
.diary-modal {
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
.diary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.diary-title {
  font-size: 24px;
  font-weight: 700;
  color: #2E7D32;
  margin: 0;
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

/* ========== 日期显示 ========== */
.date-display {
  background: linear-gradient(135deg,
    rgba(129, 199, 132, 0.2),
    rgba(102, 187, 106, 0.15)
  );
  border: 1px solid rgba(102, 187, 106, 0.3);
  border-radius: 16px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
}

.date-icon {
  font-size: 20px;
}

.date-text {
  font-size: 16px;
  font-weight: 600;
  color: #2E7D32;
}

/* ========== 表单区块 ========== */
.form-section {
  margin-bottom: 24px;
}

.section-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 15px;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 12px;
}

.intensity-value,
.char-count {
  font-size: 13px;
  color: #81C784;
  font-weight: 500;
}

/* ========== 情绪选择 ========== */
.emotion-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.emotion-option {
  background: rgba(255, 255, 255, 0.7);
  border: 2px solid rgba(129, 199, 132, 0.2);
  border-radius: 16px;
  padding: 16px 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.emotion-option:hover {
  background: rgba(129, 199, 132, 0.1);
  border-color: rgba(102, 187, 106, 0.4);
  transform: translateY(-2px);
}

.emotion-option.selected {
  background: linear-gradient(135deg,
    rgba(129, 199, 132, 0.3),
    rgba(102, 187, 106, 0.2)
  );
  border-color: #4CAF50;
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
}

.emotion-emoji {
  font-size: 36px;
  margin-bottom: 8px;
}

.emotion-label {
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
}

/* ========== 强度滑块 ========== */
.intensity-slider {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  appearance: none;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
}

.intensity-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  cursor: grab;
  border: 3px solid #4CAF50;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.intensity-slider::-webkit-slider-thumb:active {
  cursor: grabbing;
}

.intensity-slider::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  cursor: grab;
  border: 3px solid #4CAF50;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

/* ========== 文本输入 ========== */
.diary-textarea {
  width: 100%;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(129, 199, 132, 0.3);
  border-radius: 16px;
  padding: 16px;
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  resize: vertical;
  outline: none;
  transition: all 0.3s ease;
  font-family: inherit;
}

.diary-textarea::placeholder {
  color: #999;
  line-height: 1.8;
}

.diary-textarea:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

/* ========== 操作按钮 ========== */
.diary-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
}

.action-btn {
  flex: 1;
  padding: 16px 24px;
  border: none;
  border-radius: 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.action-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(76, 175, 80, 0.5);
}

.action-btn.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: linear-gradient(135deg, #9E9E9E, #BDBDBD);
  box-shadow: none;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.8);
  color: #666;
  border: 2px solid rgba(158, 158, 158, 0.3);
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(158, 158, 158, 0.5);
  transform: translateY(-2px);
}

.action-btn:active {
  transform: scale(0.98);
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
.diary-modal::-webkit-scrollbar {
  width: 6px;
}

.diary-modal::-webkit-scrollbar-track {
  background: transparent;
}

.diary-modal::-webkit-scrollbar-thumb {
  background: rgba(76, 175, 80, 0.3);
  border-radius: 3px;
}

.diary-modal::-webkit-scrollbar-thumb:hover {
  background: rgba(76, 175, 80, 0.5);
}

/* ========== 响应式 ========== */
@media (max-width: 640px) {
  .diary-modal {
    padding: 24px;
  }

  .emotion-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .diary-actions {
    flex-direction: column;
  }
}
</style>
