<template>
  <div class="body-selector">
    <!-- 标题和说明 -->
    <div class="selector-header">
      <h3 class="title">情绪影响下，身体有哪里不舒服吗？</h3>
      <p class="subtitle">点击身体部位标记情绪带来的身体感受（可多选）</p>
    </div>

    <!-- 人体图 -->
    <div class="body-container">
      <svg
        class="body-svg"
        viewBox="0 0 300 600"
        xmlns="http://www.w3.org/2000/svg"
      >
        <!-- 背景轮廓（不可点击，用于美化） -->
        <g class="body-outline">
          <!-- 头部轮廓 -->
          <ellipse cx="150" cy="60" rx="40" ry="50" fill="none" stroke="#E8F5E9" stroke-width="2"/>
          <!-- 颈部轮廓 -->
          <path d="M 130 105 Q 140 110, 150 110 Q 160 110, 170 105" fill="none" stroke="#E8F5E9" stroke-width="2"/>
          <!-- 躯干轮廓 -->
          <path d="M 100 120 Q 90 180, 95 240 Q 97 280, 110 320 L 110 380 L 125 560 L 150 560 L 175 560 L 190 380 L 190 320 Q 203 280, 205 240 Q 210 180, 200 120 Z"
                fill="none" stroke="#E8F5E9" stroke-width="2"/>
          <!-- 手臂轮廓 -->
          <path d="M 100 120 L 70 140 L 65 240 L 70 245" fill="none" stroke="#E8F5E9" stroke-width="2"/>
          <path d="M 200 120 L 230 140 L 235 240 L 230 245" fill="none" stroke="#E8F5E9" stroke-width="2"/>
        </g>

        <!-- 可点击的身体部位 -->
        <!-- 头部 -->
        <ellipse
          cx="150"
          cy="60"
          rx="38"
          ry="48"
          :class="['body-part', { selected: isSelected('head') }]"
          @click="togglePart('head')"
        />

        <!-- 颈部 -->
        <path
          d="M 132 105 Q 150 115, 168 105 L 165 120 Q 150 125, 135 120 Z"
          :class="['body-part', { selected: isSelected('neck') }]"
          @click="togglePart('neck')"
        />

        <!-- 左肩 -->
        <ellipse
          cx="105"
          cy="130"
          rx="20"
          ry="25"
          transform="rotate(-10 105 130)"
          :class="['body-part', { selected: isSelected('left_shoulder') }]"
          @click="togglePart('left_shoulder')"
        />

        <!-- 右肩 -->
        <ellipse
          cx="195"
          cy="130"
          rx="20"
          ry="25"
          transform="rotate(10 195 130)"
          :class="['body-part', { selected: isSelected('right_shoulder') }]"
          @click="togglePart('right_shoulder')"
        />

        <!-- 胸部 -->
        <path
          d="M 125 125 Q 150 140, 175 125 L 175 190 Q 150 200, 125 190 Z"
          :class="['body-part', { selected: isSelected('chest') }]"
          @click="togglePart('chest')"
        />

        <!-- 腹部 -->
        <path
          d="M 125 195 Q 150 205, 175 195 L 172 265 Q 150 275, 128 265 Z"
          :class="['body-part', { selected: isSelected('abdomen') }]"
          @click="togglePart('abdomen')"
        />

        <!-- 骨盆 -->
        <path
          d="M 128 270 Q 150 280, 172 270 L 168 310 Q 150 318, 132 310 Z"
          :class="['body-part', { selected: isSelected('pelvis') }]"
          @click="togglePart('pelvis')"
        />

        <!-- 左上臂 -->
        <path
          d="M 100 150 Q 85 155, 75 165 L 72 235 Q 75 240, 80 240 L 85 165 Q 95 155, 100 155 Z"
          :class="['body-part', { selected: isSelected('left_arm') }]"
          @click="togglePart('left_arm')"
        />

        <!-- 右上臂 -->
        <path
          d="M 200 150 Q 215 155, 225 165 L 228 235 Q 225 240, 220 240 L 215 165 Q 205 155, 200 155 Z"
          :class="['body-part', { selected: isSelected('right_arm') }]"
          @click="togglePart('right_arm')"
        />

        <!-- 左前臂 -->
        <path
          d="M 73 240 Q 70 245, 68 290 L 70 335 Q 72 340, 76 340 L 78 290 Q 80 245, 78 240 Z"
          :class="['body-part', { selected: isSelected('left_forearm') }]"
          @click="togglePart('left_forearm')"
        />

        <!-- 右前臂 -->
        <path
          d="M 227 240 Q 230 245, 232 290 L 230 335 Q 228 340, 224 340 L 222 290 Q 220 245, 222 240 Z"
          :class="['body-part', { selected: isSelected('right_forearm') }]"
          @click="togglePart('right_forearm')"
        />

        <!-- 左手 -->
        <ellipse
          cx="73"
          cy="355"
          rx="12"
          ry="18"
          :class="['body-part', { selected: isSelected('left_hand') }]"
          @click="togglePart('left_hand')"
        />

        <!-- 右手 -->
        <ellipse
          cx="227"
          cy="355"
          rx="12"
          ry="18"
          :class="['body-part', { selected: isSelected('right_hand') }]"
          @click="togglePart('right_hand')"
        />

        <!-- 左大腿 -->
        <path
          d="M 132 315 Q 125 320, 120 400 L 122 455 Q 124 460, 128 460 L 130 400 Q 135 320, 138 315 Z"
          :class="['body-part', { selected: isSelected('left_thigh') }]"
          @click="togglePart('left_thigh')"
        />

        <!-- 右大腿 -->
        <path
          d="M 168 315 Q 175 320, 180 400 L 178 455 Q 176 460, 172 460 L 170 400 Q 165 320, 162 315 Z"
          :class="['body-part', { selected: isSelected('right_thigh') }]"
          @click="togglePart('right_thigh')"
        />

        <!-- 左小腿 -->
        <path
          d="M 122 460 Q 120 465, 120 530 L 122 555 Q 124 560, 128 560 L 130 530 Q 130 465, 128 460 Z"
          :class="['body-part', { selected: isSelected('left_calf') }]"
          @click="togglePart('left_calf')"
        />

        <!-- 右小腿 -->
        <path
          d="M 178 460 Q 180 465, 180 530 L 178 555 Q 176 560, 172 560 L 170 530 Q 170 465, 172 460 Z"
          :class="['body-part', { selected: isSelected('right_calf') }]"
          @click="togglePart('right_calf')"
        />

        <!-- 左脚 -->
        <ellipse
          cx="125"
          cy="575"
          rx="15"
          ry="12"
          :class="['body-part', { selected: isSelected('left_foot') }]"
          @click="togglePart('left_foot')"
        />

        <!-- 右脚 -->
        <ellipse
          cx="175"
          cy="575"
          rx="15"
          ry="12"
          :class="['body-part', { selected: isSelected('right_foot') }]"
          @click="togglePart('right_foot')"
        />
      </svg>

      <!-- 已选择部位列表 -->
      <div v-if="selectedParts.length > 0" class="selected-parts">
        <div class="selected-header">已选择部位：</div>
        <div class="selected-tags">
          <span
            v-for="part in selectedParts"
            :key="part"
            class="selected-tag"
            @click="togglePart(part)"
          >
            {{ getPartLabel(part) }} ✕
          </span>
        </div>
      </div>
    </div>

    <!-- 确认按钮 -->
    <div class="selector-footer">
      <button class="action-btn secondary" @click="handleSkip">
        跳过此步
      </button>
      <button
        class="action-btn primary"
        :disabled="selectedParts.length === 0"
        @click="handleConfirm"
      >
        确认 {{ selectedParts.length > 0 ? `(${selectedParts.length})` : '' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BodySelector',
  emits: ['confirm', 'skip'],
  data() {
    return {
      selectedParts: [],
      partLabels: {
        'head': '头部',
        'neck': '颈部',
        'chest': '胸部',
        'left_shoulder': '左肩',
        'right_shoulder': '右肩',
        'left_arm': '左上臂',
        'right_arm': '右上臂',
        'left_forearm': '左前臂',
        'right_forearm': '右前臂',
        'left_hand': '左手',
        'right_hand': '右手',
        'abdomen': '腹部',
        'pelvis': '骨盆',
        'left_thigh': '左大腿',
        'right_thigh': '右大腿',
        'left_calf': '左小腿',
        'right_calf': '右小腿',
        'left_foot': '左脚',
        'right_foot': '右脚'
      }
    }
  },
  methods: {
    isSelected(part) {
      return this.selectedParts.includes(part)
    },

    togglePart(part) {
      const index = this.selectedParts.indexOf(part)
      if (index > -1) {
        // 已选中，取消选择
        this.selectedParts.splice(index, 1)
      } else {
        // 未选中，添加选择
        this.selectedParts.push(part)
      }
    },

    getPartLabel(part) {
      return this.partLabels[part] || part
    },

    handleConfirm() {
      if (this.selectedParts.length === 0) return

      this.$emit('confirm', {
        selectedParts: this.selectedParts,
        labels: this.selectedParts.map(p => this.getPartLabel(p))
      })
    },

    handleSkip() {
      this.$emit('skip')
    }
  }
}
</script>

<style scoped>
.body-selector {
  max-width: 500px;
  margin: 0 auto;
  padding: 24px;
}

/* ========== 头部 ========== */
.selector-header {
  text-align: center;
  margin-bottom: 24px;
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: #81C784;
}

/* ========== 人体图容器 ========== */
.body-container {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.8),
    rgba(255, 255, 255, 0.6)
  );
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 2px solid rgba(102, 187, 106, 0.3);
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(46, 125, 50, 0.2);
}

/* ========== SVG人体图 ========== */
.body-svg {
  width: 100%;
  max-width: 300px;
  height: auto;
  display: block;
  margin: 0 auto;
  user-select: none;
}

.body-part {
  fill: rgba(129, 199, 132, 0.15);
  stroke: rgba(102, 187, 106, 0.4);
  stroke-width: 1.5;
  cursor: pointer;
  transition: all 0.3s ease;
}

.body-part:hover {
  fill: rgba(129, 199, 132, 0.3);
  stroke: rgba(76, 175, 80, 0.6);
  stroke-width: 2;
  filter: drop-shadow(0 0 8px rgba(76, 175, 80, 0.5));
}

.body-part.selected {
  fill: rgba(244, 67, 54, 0.4);
  stroke: #F44336;
  stroke-width: 2.5;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    filter: drop-shadow(0 0 4px rgba(244, 67, 54, 0.6));
  }
  50% {
    filter: drop-shadow(0 0 12px rgba(244, 67, 54, 0.8));
  }
}

.part-label {
  fill: #2E7D32;
  font-size: 14px;
  font-weight: 600;
  text-anchor: middle;
  pointer-events: none;
  user-select: none;
}

/* ========== 已选择部位列表 ========== */
.selected-parts {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 2px dashed rgba(102, 187, 106, 0.3);
}

.selected-header {
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 12px;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.selected-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg,
    rgba(244, 67, 54, 0.15),
    rgba(239, 83, 80, 0.1)
  );
  border: 1px solid rgba(244, 67, 54, 0.4);
  border-radius: 12px;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 600;
  color: #D32F2F;
  cursor: pointer;
  transition: all 0.2s ease;
}

.selected-tag:hover {
  background: linear-gradient(135deg,
    rgba(244, 67, 54, 0.25),
    rgba(239, 83, 80, 0.2)
  );
  border-color: rgba(244, 67, 54, 0.6);
  transform: translateY(-1px);
}

/* ========== 底部按钮 ========== */
.selector-footer {
  display: flex;
  gap: 12px;
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

/* ========== 响应式 ========== */
@media (max-width: 640px) {
  .body-selector {
    padding: 16px;
  }

  .selector-footer {
    flex-direction: column;
  }
}
</style>
