<template>
  <div class="diary-tab">
    <!-- 日记记录表单 -->
    <DiaryRecordForm
      :visible="showRecordForm"
      @close="showRecordForm = false"
      @save="handleSaveDiary"
    />

    <!-- 日记详情查看 -->
    <DiaryDetailModal
      :visible="showDetailModal"
      :diary="selectedDiary"
      @close="showDetailModal = false"
    />

    <div class="timeline">
      <div class="timeline-line"></div>

      <!-- 过去的日记 -->
      <div
        v-for="diary in pastDiaries"
        :key="diary.id"
        class="timeline-item past"
      >
        <div class="timeline-dot"></div>
        <div class="diary-card clickable" @click="viewDiary(diary)">
          <div class="date-text">{{ diary.date }}</div>
          <div class="emotion-tag">{{ diary.emoji }} {{ diary.emotionLabel }}</div>
        </div>
      </div>

      <!-- 今天 -->
      <div class="timeline-item today">
        <!-- 今天还没有记录 -->
        <div v-if="!todayDiary" class="today-card" @click="recordToday">
          <div class="date-text">
            {{ todayDate }}
            <span class="badge">今天</span>
          </div>
          <div class="hint-text">✨ 点击记录今天的心情</div>
        </div>

        <!-- 今天已有记录 -->
        <div v-else class="diary-card today-recorded">
          <div class="date-text">
            {{ todayDate }}
            <span class="badge">今天</span>
          </div>
          <div class="emotion-tag">{{ todayDiary.emoji }} {{ todayDiary.emotionLabel }}</div>
          <p class="diary-preview">{{ todayDiary.content }}</p>
          <button class="edit-btn" @click="recordToday">✏️ 编辑</button>
        </div>
      </div>

      <!-- 未来的日期 -->
      <div
        v-for="future in futureDates"
        :key="future.id"
        class="timeline-item future"
      >
        <div class="timeline-dot"></div>
        <div class="diary-card">
          <div class="date-text" style="color: #81C784;">{{ future.date }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DiaryRecordForm from '@/components/DiaryRecordForm.vue'
import DiaryDetailModal from '@/components/DiaryDetailModal.vue'
import { createDiary, updateDiary, getDiaryList } from '@/api/emotion'

export default {
  name: 'DiaryTab',
  components: {
    DiaryRecordForm,
    DiaryDetailModal
  },
  data() {
    return {
      showRecordForm: false,
      showDetailModal: false,
      selectedDiary: null,
      editingDiary: null,
      diaries: [],
      futureDates: [],
      isEditing: false
    }
  },
  computed: {
    todayDate() {
      const now = new Date()
      const month = now.getMonth() + 1
      const date = now.getDate()
      const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
      const weekday = weekdays[now.getDay()]
      return `${month}月${date}日 ${weekday}`
    },
    todayDiary() {
      // 检查今天是否已经有日记
      const today = new Date().toDateString()
      return this.diaries.find(diary => {
        const diaryDate = new Date(diary.date).toDateString()
        return diaryDate === today
      })
    },
    pastDiaries() {
      // 过去的日记（不包括今天）
      const today = new Date()
      today.setHours(0, 0, 0, 0)

      return this.diaries
        .filter(diary => new Date(diary.date) < today)
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .map(diary => ({
          ...diary,
          date: this.formatDate(diary.date)
        }))
    }
  },
  methods: {
    recordToday() {
      this.isEditing = !!this.todayDiary
      this.editingDiary = this.todayDiary ? { ...this.todayDiary } : null
      this.showRecordForm = true
    },

    async handleSaveDiary(diaryEntry) {
      try {
        const diaryData = {
          emotion: diaryEntry.emotion,
          emotionLabel: diaryEntry.emotionLabel,
          emoji: diaryEntry.emoji,
          intensity: diaryEntry.intensity,
          content: diaryEntry.content,
          triggers: diaryEntry.triggers,
          body_parts: diaryEntry.bodyParts,
          selected_images: diaryEntry.selectedImages
        }

        let response
        if (this.isEditing && this.editingDiary) {
          response = await updateDiary(this.editingDiary.id, diaryData)
        } else {
          response = await createDiary({
            ...diaryData,
            diary_date: new Date().toISOString().split('T')[0]
          })
        }

        console.log('后端返回响应:', response)

        const savedDiary = {
          id: response.id || this.editingDiary?.id,
          emotion: response.emotion || response.emotion_type,
          emotionLabel: response.emotionLabel || response.emotion_label,
          emoji: response.emoji,
          intensity: response.intensity,
          content: response.content,
          triggers: response.triggers,
          bodyParts: response.body_parts,
          selectedImages: response.selected_images,
          date: response.diary_date,
          created_at: response.created_at
        }

        if (this.isEditing && this.editingDiary) {
          const index = this.diaries.findIndex(d => d.id === savedDiary.id)
          if (index !== -1) {
            this.diaries.splice(index, 1, savedDiary)
          }
        } else {
          this.diaries.push(savedDiary)
        }

        this.saveDiariesToStorage()
        this.showRecordForm = false
        this.editingDiary = null
        this.isEditing = false

        console.log('日记已保存:', savedDiary)
      } catch (error) {
        console.error('保存日记失败:', error)
        if (error.response?.status === 409) {
          alert('今天已经写过日记了，不能重复创建')
        } else if (error.response?.status === 404) {
          alert('日记不存在或已被删除')
          this.loadDiariesFromBackend()
        } else {
          alert('保存失败，请稍后重试')
        }
      }
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      const month = date.getMonth() + 1
      const day = date.getDate()
      const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
      const weekday = weekdays[date.getDay()]
      return `${month}月${day}日 ${weekday}`
    },

    loadDiariesFromStorage() {
      try {
        const stored = localStorage.getItem('emotion_diaries')
        if (stored) {
          this.diaries = JSON.parse(stored)
        }
      } catch (error) {
        console.error('加载日记失败:', error)
      }
    },

    async loadDiariesFromBackend() {
      try {
        const response = await getDiaryList({ page: 1, pageSize: 100 })
        if (response.list && response.list.length > 0) {
          this.diaries = response.list.map(diary => ({
            id: diary.id,
            emotion: diary.emotion || diary.emotion_type,
            emotionLabel: diary.emotionLabel || diary.emotion_label,
            emoji: diary.emoji,
            intensity: diary.intensity,
            content: diary.content,
            triggers: diary.triggers,
            bodyParts: diary.body_parts,
            selectedImages: diary.selected_images,
            date: diary.diary_date,
            created_at: diary.created_at
          }))
          this.saveDiariesToStorage()
          console.log('从后端加载日记成功:', this.diaries.length, '条')
        }
      } catch (error) {
        console.error('从后端加载日记失败:', error)
        this.loadDiariesFromStorage()
      }
    },

    saveDiariesToStorage() {
      try {
        localStorage.setItem('emotion_diaries', JSON.stringify(this.diaries))
      } catch (error) {
        console.error('保存日记失败:', error)
      }
    },

    generateFutureDates() {
      // 生成未来3天的日期
      const dates = []
      for (let i = 1; i <= 3; i++) {
        const future = new Date()
        future.setDate(future.getDate() + i)
        dates.push({
          id: `future-${i}`,
          date: this.formatDate(future)
        })
      }
      this.futureDates = dates
    },

    viewDiary(diary) {
      // 查看日记详情
      this.selectedDiary = {
        ...diary,
        date: this.formatDate(diary.date)
      }
      this.showDetailModal = true
    }
  },
  mounted() {
    this.loadDiariesFromBackend()
    this.generateFutureDates()
  }
}
</script>

<style scoped>
.diary-tab {
  height: 100%;
  overflow-y: auto;
  background: transparent;
}

/* ========== 时间轴 ========== */
.timeline {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  padding: 48px 24px;
}

.timeline-line {
  position: absolute;
  left: 48px;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg,
    rgba(129, 199, 132, 0.3) 0%,
    rgba(102, 187, 106, 0.7) 50%,
    rgba(129, 199, 132, 0.3) 100%
  );
  box-shadow: 0 0 8px rgba(102, 187, 106, 0.3);
}

.timeline-item {
  position: relative;
  padding-left: 96px;
  margin-bottom: 40px;
}

.timeline-dot {
  position: absolute;
  left: 41px;
  top: 12px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  z-index: 10;
}

.timeline-item.past .timeline-dot {
  background: linear-gradient(135deg, #66BB6A, #4CAF50);
  border: 4px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4), 0 0 0 4px rgba(129, 199, 132, 0.2);
}

.timeline-item.future .timeline-dot {
  background: rgba(255, 255, 255, 0.6);
  border: 3px solid rgba(129, 199, 132, 0.4);
  box-shadow: 0 2px 8px rgba(129, 199, 132, 0.2);
}

/* ========== 日记卡片 ========== */
.diary-card {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.7),
    rgba(255, 255, 255, 0.5)
  );
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(46, 125, 50, 0.15), inset 0 2px 0 rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
}

.diary-card.clickable {
  cursor: pointer;
}

.diary-card.clickable:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(46, 125, 50, 0.25), inset 0 2px 0 rgba(255, 255, 255, 1);
}

.diary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 36px rgba(46, 125, 50, 0.2), inset 0 2px 0 rgba(255, 255, 255, 1);
}

.date-text {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #2E7D32;
}

.emotion-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg,
    rgba(129, 199, 132, 0.3),
    rgba(102, 187, 106, 0.2)
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 187, 106, 0.4);
  border-radius: 14px;
  padding: 6px 14px;
  color: #2E7D32;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
}

.emotion-tag:hover {
  background: linear-gradient(135deg,
    rgba(129, 199, 132, 0.4),
    rgba(102, 187, 106, 0.3)
  );
  border-color: rgba(76, 175, 80, 0.6);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
  transform: translateY(-2px);
}

/* ========== 今日卡片 ========== */
.timeline-item.today {
  padding-left: 24px;
}

.today-card {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.85),
    rgba(255, 255, 255, 0.7)
  );
  backdrop-filter: blur(25px) saturate(180%);
  -webkit-backdrop-filter: blur(25px) saturate(180%);
  border: 3px solid rgba(102, 187, 106, 0.5);
  border-radius: 24px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 16px 48px rgba(76, 175, 80, 0.25), inset 0 2px 0 rgba(255, 255, 255, 0.9);
  transition: all 0.4s ease;
  animation: todayPulse 3s ease-in-out infinite;
}

@keyframes todayPulse {
  0%, 100% {
    box-shadow: 0 16px 48px rgba(76, 175, 80, 0.25), inset 0 2px 0 rgba(255, 255, 255, 0.9);
    border-color: rgba(102, 187, 106, 0.5);
  }
  50% {
    box-shadow: 0 20px 56px rgba(76, 175, 80, 0.4), inset 0 2px 0 rgba(255, 255, 255, 1);
    border-color: rgba(76, 175, 80, 0.7);
  }
}

.today-card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 24px 64px rgba(76, 175, 80, 0.35), inset 0 2px 0 rgba(255, 255, 255, 1);
}

.today-card .date-text {
  color: #2E7D32;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 12px;
}

.badge {
  display: inline-block;
  background: linear-gradient(135deg,
    rgba(102, 187, 106, 0.3),
    rgba(129, 199, 132, 0.2)
  );
  color: #2E7D32;
  font-size: 13px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 10px;
  margin-left: 8px;
  border: 1px solid rgba(102, 187, 106, 0.3);
}

.hint-text {
  color: #66BB6A;
  font-size: 14px;
  margin-top: 10px;
  font-weight: 500;
}

/* ========== 今天已记录状态 ========== */
.today-recorded {
  cursor: default;
}

.today-recorded:hover {
  transform: translateY(-2px);
}

.diary-preview {
  font-size: 14px;
  line-height: 1.6;
  color: #555;
  margin: 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.edit-btn {
  background: linear-gradient(135deg,
    rgba(102, 187, 106, 0.2),
    rgba(129, 199, 132, 0.15)
  );
  border: 1px solid rgba(102, 187, 106, 0.3);
  color: #2E7D32;
  padding: 8px 16px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: linear-gradient(135deg,
    rgba(102, 187, 106, 0.3),
    rgba(129, 199, 132, 0.2)
  );
  border-color: rgba(76, 175, 80, 0.5);
  transform: translateY(-1px);
}

/* 滚动条样式 */
.diary-tab::-webkit-scrollbar {
  width: 6px;
}

.diary-tab::-webkit-scrollbar-track {
  background: transparent;
}

.diary-tab::-webkit-scrollbar-thumb {
  background: rgba(76, 175, 80, 0.3);
  border-radius: 3px;
}

.diary-tab::-webkit-scrollbar-thumb:hover {
  background: rgba(76, 175, 80, 0.5);
}
</style>
