<template>
  <Transition name="modal-fade">
    <div v-if="visible" class="crisis-modal-overlay" @click="handleOverlayClick">
      <div class="crisis-modal" @click.stop>
        <!-- 警示标题 -->
        <div class="crisis-header">
          <div class="crisis-icon">⚠️</div>
          <h2 class="crisis-title">我们注意到你的情绪强度较高</h2>
          <p class="crisis-subtitle">你的安全对我们很重要</p>
        </div>

        <!-- 危机热线 -->
        <div class="crisis-section">
          <h3 class="section-title">🆘 24小时危机干预热线</h3>
          <div class="hotline-list">
            <div class="hotline-item">
              <div class="hotline-name">全国心理危机干预热线</div>
              <a href="tel:400-161-9995" class="hotline-number">400-161-9995</a>
            </div>
            <div class="hotline-item">
              <div class="hotline-name">北京心理危机研究与干预中心</div>
              <a href="tel:010-82951332" class="hotline-number">010-82951332</a>
            </div>
            <div class="hotline-item">
              <div class="hotline-name">生命热线（上海）</div>
              <a href="tel:021-12320-5" class="hotline-number">021-12320-5</a>
            </div>
          </div>
        </div>

        <!-- 紧急建议 -->
        <div class="crisis-section">
          <h3 class="section-title">💚 现在可以做的事</h3>
          <ul class="suggestion-list">
            <li class="suggestion-item">
              <span class="bullet">🧘</span>
              <span class="text">深呼吸：吸气4秒 - 屏息4秒 - 呼气4秒</span>
            </li>
            <li class="suggestion-item">
              <span class="bullet">💬</span>
              <span class="text">找信任的人倾诉，不要独自承受</span>
            </li>
            <li class="suggestion-item">
              <span class="bullet">🚶</span>
              <span class="text">去安全的地方，远离可能伤害自己的物品</span>
            </li>
            <li class="suggestion-item">
              <span class="bullet">📞</span>
              <span class="text">如果感到无法控制，立即拨打上方热线</span>
            </li>
          </ul>
        </div>

        <!-- 重要提示 -->
        <div class="crisis-warning">
          <p>⚠️ 如果你有伤害自己或他人的想法，请立即寻求专业帮助</p>
        </div>

        <!-- 操作按钮 -->
        <div class="crisis-actions">
          <button class="action-btn primary" @click="callHotline">
            📞 拨打热线
          </button>
          <button class="action-btn secondary" @click="handleClose">
            我知道了
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'CrisisWarningModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'call-hotline'],
  methods: {
    handleClose() {
      this.$emit('close')
    },
    handleOverlayClick() {
      // 危机弹窗不允许点击遮罩关闭
      // 用户必须点击"我知道了"按钮
    },
    callHotline() {
      // 在移动端可以直接拨打电话
      window.location.href = 'tel:400-161-9995'
      this.$emit('call-hotline')
    }
  }
}
</script>

<style scoped>
/* ========== 遮罩层 ========== */
.crisis-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* ========== 弹窗主体 ========== */
.crisis-modal {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.95),
    rgba(255, 255, 255, 0.9)
  );
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border: 3px solid rgba(244, 67, 54, 0.3);
  border-radius: 28px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 40px 32px;
  box-shadow: 0 24px 80px rgba(244, 67, 54, 0.4), inset 0 2px 0 rgba(255, 255, 255, 1);
  animation: modalSlideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* ========== 标题区 ========== */
.crisis-header {
  text-align: center;
  margin-bottom: 32px;
}

.crisis-icon {
  font-size: 72px;
  margin-bottom: 16px;
  animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.crisis-title {
  font-size: 24px;
  font-weight: 700;
  color: #D32F2F;
  margin-bottom: 8px;
  line-height: 1.4;
}

.crisis-subtitle {
  font-size: 16px;
  color: #666;
  font-weight: 500;
}

/* ========== 内容区块 ========== */
.crisis-section {
  margin-bottom: 28px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #1B5E20;
  margin-bottom: 16px;
}

/* ========== 热线列表 ========== */
.hotline-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hotline-item {
  background: rgba(244, 67, 54, 0.05);
  border: 2px solid rgba(244, 67, 54, 0.2);
  border-radius: 16px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.hotline-item:hover {
  background: rgba(244, 67, 54, 0.1);
  border-color: rgba(244, 67, 54, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(244, 67, 54, 0.2);
}

.hotline-name {
  font-size: 14px;
  color: #333;
  font-weight: 600;
}

.hotline-number {
  font-size: 18px;
  font-weight: 700;
  color: #D32F2F;
  text-decoration: none;
  transition: all 0.2s ease;
}

.hotline-number:hover {
  color: #B71C1C;
  transform: scale(1.05);
}

/* ========== 建议列表 ========== */
.suggestion-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: rgba(76, 175, 80, 0.05);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: 12px;
  transition: all 0.25s ease;
}

.suggestion-item:hover {
  background: rgba(76, 175, 80, 0.1);
  border-color: rgba(76, 175, 80, 0.4);
  transform: translateX(4px);
}

.suggestion-item .bullet {
  font-size: 20px;
  flex-shrink: 0;
}

.suggestion-item .text {
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}

/* ========== 警告提示 ========== */
.crisis-warning {
  background: linear-gradient(135deg,
    rgba(255, 235, 59, 0.2),
    rgba(255, 193, 7, 0.15)
  );
  border: 2px solid rgba(255, 152, 0, 0.4);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 28px;
}

.crisis-warning p {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #E65100;
  text-align: center;
  line-height: 1.6;
}

/* ========== 操作按钮 ========== */
.crisis-actions {
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
  background: linear-gradient(135deg, #F44336, #EF5350);
  color: white;
  box-shadow: 0 6px 20px rgba(244, 67, 54, 0.4);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(244, 67, 54, 0.5);
}

.action-btn.secondary {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.8),
    rgba(255, 255, 255, 0.6)
  );
  color: #666;
  border: 2px solid rgba(158, 158, 158, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-btn.secondary:hover {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.9),
    rgba(255, 255, 255, 0.7)
  );
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

/* ========== 滚动条样式 ========== */
.crisis-modal::-webkit-scrollbar {
  width: 6px;
}

.crisis-modal::-webkit-scrollbar-track {
  background: transparent;
}

.crisis-modal::-webkit-scrollbar-thumb {
  background: rgba(244, 67, 54, 0.3);
  border-radius: 3px;
}

.crisis-modal::-webkit-scrollbar-thumb:hover {
  background: rgba(244, 67, 54, 0.5);
}

/* ========== 响应式 ========== */
@media (max-width: 640px) {
  .crisis-modal {
    padding: 32px 24px;
  }

  .crisis-title {
    font-size: 20px;
  }

  .crisis-actions {
    flex-direction: column;
  }

  .hotline-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
