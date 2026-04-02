<template>
  <div class="emotion-selector">
    <!-- 标题和说明 -->
    <div class="selector-header">
      <h3 class="title">请选择能代表你当前感受的图片</h3>
      <p class="subtitle">可以多选，选完后点击确认</p>
    </div>

    <!-- 图片网格 -->
    <div class="image-grid">
      <div
        v-for="image in images"
        :key="image.id"
        class="image-item"
        :class="{ selected: isSelected(image.id) }"
        @click="toggleImage(image.id)"
      >
        <img :src="image.url" :alt="'图片' + image.id" />
        <div v-if="isSelected(image.id)" class="check-mark">✓</div>
      </div>
    </div>

    <!-- 确认按钮 -->
    <div class="selector-footer">
      <button
        class="confirm-btn"
        :disabled="selectedImages.length === 0"
        @click="handleConfirm"
      >
        确认选择 ({{ selectedImages.length }}/{{ images.length }})
      </button>
    </div>
  </div>
</template>

<script>
import { getEmotionImages } from '@/api/emotion'

export default {
  name: 'EmotionImageSelector',
  data() {
    return {
      images: [],
      selectedImages: [], // 存储选中的图片信息 [{imageId, url, selectionTime}]
      loading: true,
      loadError: false
    }
  },
  methods: {
    async loadImages() {
      this.loading = true
      this.loadError = false

      try {
        const response = await getEmotionImages({
          limit: 12,
          random_select: true
        })

        // 转换为组件需要的格式
        this.images = response.images.map(img => ({
          id: img.imageId,
          url: img.url,
          category: img.category,
          name: img.name
        }))

        console.log('✅ CAPS图片加载成功，共', this.images.length, '张')
      } catch (error) {
        console.error('❌ 加载CAPS图片失败:', error)
        this.loadError = true
      } finally {
        this.loading = false
      }
    },

    isSelected(imageId) {
      return this.selectedImages.some(item => item.imageId === imageId)
    },

    toggleImage(imageId) {
      const index = this.selectedImages.findIndex(item => item.imageId === imageId)

      const imageData = this.images.find(img => img.id === imageId)

      if (index > -1) {
        // 已选中，取消选择
        this.selectedImages.splice(index, 1)
      } else {
        // 未选中，添加选择
        this.selectedImages.push({
          imageId: imageId,
          url: imageData ? imageData.url : '',
          selectionTime: Date.now() // 记录选择时间（后端可能需要）
        })
      }
    },

    handleConfirm() {
      if (this.selectedImages.length === 0) {
        return
      }

      // 触发事件，将选择结果传递给父组件
      this.$emit('confirm', {
        selectedImages: this.selectedImages,
        totalImages: this.images.length
      })

      console.log('用户选择的图片:', this.selectedImages)
    }
  },

  mounted() {
    this.loadImages()
  }
}
</script>

<style scoped>
.emotion-selector {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

/* ========== 头部 ========== */
.selector-header {
  text-align: center;
  margin-bottom: 32px;
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

/* ========== 图片网格 ========== */
.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

@media (max-width: 768px) {
  .image-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.image-item {
  position: relative;
  aspect-ratio: 3/2;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  border: 3px solid transparent;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(46, 125, 50, 0.3);
}

/* 选中状态 */
.image-item.selected {
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2),
              0 8px 24px rgba(46, 125, 50, 0.4);
}

.check-mark {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.5);
  animation: checkPop 0.3s ease;
}

@keyframes checkPop {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

/* ========== 底部按钮 ========== */
.selector-footer {
  text-align: center;
}

.confirm-btn {
  padding: 16px 48px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  border: none;
  border-radius: 28px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
  transition: all 0.3s ease;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(76, 175, 80, 0.5);
}

.confirm-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: linear-gradient(135deg, #9E9E9E, #BDBDBD);
  box-shadow: none;
}
</style>
