<template>
  <div v-if="visible" class="skill-confirmation">
    <div class="confirmation-card">
      <div class="card-header">
        <span class="header-icon">💡</span>
        <h3 class="header-title">技能推荐</h3>
      </div>
      <div class="skill-info">
        <h4 class="skill-name">{{ skillName }}</h4>
        <p class="skill-intro">{{ introduction }}</p>
      </div>
      <div class="options">
        <button
          v-for="option in options"
          :key="option"
          class="option-btn"
          :class="option === '愿意' ? 'primary-btn' : 'secondary-btn'"
          @click="handleOptionClick(option)"
        >
          {{ option }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkillConfirmation',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    skillName: {
      type: String,
      default: ''
    },
    introduction: {
      type: String,
      default: ''
    },
    options: {
      type: Array,
      default: () => ['愿意', '再想想']
    }
  },
  methods: {
    handleOptionClick(option) {
      this.$emit('confirm', { choice: option })
    }
  }
}
</script>

<style scoped>
.skill-confirmation {
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

.confirmation-card {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.95),
    rgba(255, 255, 255, 0.85)
  );
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 2px solid rgba(102, 187, 106, 0.3);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(46, 125, 50, 0.2);
  padding: 28px;
  max-width: 500px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.header-icon {
  font-size: 32px;
}

.header-title {
  font-size: 20px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0;
}

.skill-info {
  margin-bottom: 24px;
}

.skill-name {
  font-size: 22px;
  font-weight: 700;
  color: #2E7D32;
  margin: 0 0 12px 0;
}

.skill-intro {
  font-size: 15px;
  line-height: 1.7;
  color: #555;
  margin: 0;
}

.options {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.option-btn {
  flex: 1;
  max-width: 160px;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-btn {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.secondary-btn {
  background: #f0f0f0;
  color: #666;
}

.secondary-btn:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}
</style>
