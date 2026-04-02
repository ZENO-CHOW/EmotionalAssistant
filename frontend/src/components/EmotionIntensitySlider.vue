<template>
  <div class="slider-container">
    <div class="slider-header">
      <div class="slider-label">{{ label }}</div>
      <div class="slider-value" :style="{ color: intensityColor.primary }">
        {{ tempValue }}/{{ max }}
      </div>
    </div>

    <div class="slider-wrapper">
      <!-- 使用原生input[type="range"]获得最流畅的体验 -->
      <input
        type="range"
        class="slider-input"
        :min="min"
        :max="max"
        :value="tempValue"
        :style="sliderTrackStyle"
        @input="handleInput"
        @change="handleChange"
      />
    </div>

    <!-- 刻度标签 -->
    <div class="slider-labels">
      <span>{{ min }}</span>
      <span v-if="showMiddle">{{ Math.round((min + max) / 2) }}</span>
      <span>{{ max }}</span>
    </div>

    <!-- 确认按钮 -->
    <button
      class="confirm-btn"
      :class="{ 'changed': hasChanged }"
      :style="confirmButtonStyle"
      @click="handleConfirm"
    >
      {{ hasChanged ? '✓ 确认调整' : '已确认' }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'EmotionIntensitySlider',
  props: {
    // 当前值
    modelValue: {
      type: Number,
      default: 5
    },
    // 最小值
    min: {
      type: Number,
      default: 0
    },
    // 最大值
    max: {
      type: Number,
      default: 10
    },
    // 标签文字
    label: {
      type: String,
      default: '情绪强度'
    },
    // 是否显示中间刻度
    showMiddle: {
      type: Boolean,
      default: true
    }
  },
  emits: ['update:modelValue', 'confirm'],
  data() {
    return {
      tempValue: this.modelValue, // 临时值（拖动时实时更新）
      confirmedValue: this.modelValue // 确认后的值
    }
  },
  computed: {
    percentage() {
      return ((this.tempValue - this.min) / (this.max - this.min)) * 100
    },
    hasChanged() {
      return this.tempValue !== this.confirmedValue
    },
    // 根据情绪强度返回颜色配置
    intensityColor() {
      const value = this.tempValue

      // 低强度 (0-3): 绿色系
      if (value <= 3) {
        return {
          primary: '#4CAF50',
          secondary: '#66BB6A',
          light: '#81C784'
        }
      }
      // 中等强度 (4-6): 黄橙色系
      else if (value <= 6) {
        return {
          primary: '#FF9800',
          secondary: '#FFB74D',
          light: '#FFCC80'
        }
      }
      // 高强度 (7-10): 红色系（危机）
      else {
        return {
          primary: '#F44336',
          secondary: '#EF5350',
          light: '#E57373'
        }
      }
    },
    // 滑块轨道渐变样式
    sliderTrackStyle() {
      const percent = this.percentage
      return {
        background: `linear-gradient(to right,
          ${this.intensityColor.light} 0%,
          ${this.intensityColor.secondary} ${percent}%,
          ${this.intensityColor.primary} ${percent}%,
          rgba(200, 200, 200, 0.3) ${percent}%
        )`
      }
    },
    // 确认按钮样式
    confirmButtonStyle() {
      if (this.hasChanged) {
        return {
          background: `linear-gradient(135deg, ${this.intensityColor.primary}, ${this.intensityColor.secondary})`,
          borderColor: this.intensityColor.primary,
          color: '#fff'
        }
      }
      return {}
    }
  },
  watch: {
    modelValue(newVal) {
      this.tempValue = newVal
      this.confirmedValue = newVal
    }
  },
  methods: {
    handleInput(event) {
      // 拖动时实时更新临时值
      this.tempValue = parseInt(event.target.value)
    },

    handleChange(event) {
      // 拖动结束时更新临时值
      this.tempValue = parseInt(event.target.value)
    },

    handleConfirm() {
      if (!this.hasChanged) return

      // 确认后更新确认值
      this.confirmedValue = this.tempValue

      // 触发更新事件
      this.$emit('update:modelValue', this.tempValue)
      this.$emit('confirm', this.tempValue)
    }
  }
}
</script>

<style scoped>
.slider-container {
  padding: 20px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(46, 125, 50, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.8);
  user-select: none;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.slider-label {
  color: #2E7D32;
  font-size: 15px;
  font-weight: 600;
}

.slider-value {
  font-size: 18px;
  font-weight: 700;
  transition: color 0.3s ease;
}

.slider-wrapper {
  padding: 12px 0;
  margin-bottom: 8px;
}

/* ========== 原生range input样式 ========== */
.slider-input {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  outline: none;
  cursor: pointer;
}

/* Webkit浏览器（Chrome, Safari, Edge）的轨道 */
.slider-input::-webkit-slider-runnable-track {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Webkit浏览器的滑块 */
.slider-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FFFFFF, #F1F8E9);
  cursor: grab;
  border: 3px solid currentColor;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3), inset 0 2px 0 rgba(255, 255, 255, 0.9);
  margin-top: -10px;
  transition: transform 0.2s ease;
}

.slider-input::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.slider-input::-webkit-slider-thumb:active {
  cursor: grabbing;
  transform: scale(1.1);
}

/* Firefox浏览器的轨道 */
.slider-input::-moz-range-track {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Firefox浏览器的滑块 */
.slider-input::-moz-range-thumb {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FFFFFF, #F1F8E9);
  cursor: grab;
  border: 3px solid currentColor;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3), inset 0 2px 0 rgba(255, 255, 255, 0.9);
  transition: transform 0.2s ease;
}

.slider-input::-moz-range-thumb:hover {
  transform: scale(1.15);
}

.slider-input::-moz-range-thumb:active {
  cursor: grabbing;
  transform: scale(1.1);
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  font-size: 12px;
  color: #81C784;
  padding: 0 2px;
}

/* ========== 确认按钮 ========== */
.confirm-btn {
  width: 100%;
  padding: 14px 24px;
  border: 2px solid rgba(158, 158, 158, 0.3);
  border-radius: 20px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.6);
  color: #999;
  transition: all 0.3s ease;
  outline: none;
}

.confirm-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.confirm-btn.changed {
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
  animation: btnPulse 2s ease-in-out infinite;
}

.confirm-btn.changed:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(76, 175, 80, 0.5);
}

.confirm-btn.changed:active {
  transform: scale(0.98);
}

@keyframes btnPulse {
  0%, 100% {
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
  }
  50% {
    box-shadow: 0 8px 28px rgba(76, 175, 80, 0.6);
  }
}
</style>
