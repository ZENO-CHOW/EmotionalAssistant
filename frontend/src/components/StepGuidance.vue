<template>
  <div v-if="visible" class="step-guidance">
    <div class="guidance-card">
      <div class="step-indicator">
        <span class="step-badge">第{{ stepNumber }}步</span>
        <span class="step-total">/ 共{{ totalSteps }}步</span>
      </div>
      <div class="step-content">
        <p class="content-text">{{ content }}</p>
      </div>
      <div class="step-actions">
        <button class="complete-btn" @click="handleComplete">
          {{ isLastStep ? '✓ 完成练习' : '✓ 已完成，继续下一步' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StepGuidance',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    stepNumber: {
      type: Number,
      default: 1
    },
    totalSteps: {
      type: Number,
      default: 1
    },
    content: {
      type: String,
      default: ''
    },
    isLastStep: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    handleComplete() {
      this.$emit('complete')
    }
  }
}
</script>

<style scoped>
.step-guidance {
  margin: 20px auto;
  padding: 16px;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.guidance-card {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.95),
    rgba(255, 255, 255, 0.85)
  );
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 2px solid rgba(33, 150, 243, 0.3);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(33, 150, 243, 0.2);
  padding: 28px;
  max-width: 500px;
  margin: 0 auto;
}

.step-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  justify-content: center;
}

.step-badge {
  background: linear-gradient(135deg, #2196F3, #42A5F5);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.step-total {
  color: #999;
  font-size: 14px;
}

.step-content {
  margin-bottom: 24px;
}

.content-text {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  text-align: center;
  margin: 0;
  padding: 16px;
  background: rgba(33, 150, 243, 0.05);
  border-radius: 12px;
}

.step-actions {
  display: flex;
  justify-content: center;
}

.complete-btn {
  background: linear-gradient(135deg, #2196F3, #42A5F5);
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(33, 150, 243, 0.3);
}

.complete-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
}

.complete-btn:active {
  transform: translateY(0);
}
</style>
