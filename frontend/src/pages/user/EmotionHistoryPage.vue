<template>
  <div class="emotion-history-page">
    <!-- 顶部导航栏 -->
    <div class="page-header">
      <button class="back-btn" @click="goBack">← 返回</button>
      <h1 class="page-title">情绪历史分析</h1>
      <button class="export-btn" @click="exportData">📊 导出数据</button>
    </div>

    <!-- 统计概览卡片 -->
    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <div class="stat-value">{{ totalRecords }}</div>
          <div class="stat-label">总记录数</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-info">
          <div class="stat-value">{{ continuousDays }}</div>
          <div class="stat-label">连续记录天数</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">{{ mostCommonEmotionEmoji }}</div>
        <div class="stat-info">
          <div class="stat-value">{{ mostCommonEmotion }}</div>
          <div class="stat-label">最常见情绪</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📈</div>
        <div class="stat-info">
          <div class="stat-value">{{ averageIntensity }}</div>
          <div class="stat-label">平均强度</div>
        </div>
      </div>
    </div>

    <!-- 情绪分布图表 -->
    <div class="chart-section">
      <h2 class="section-title">情绪分布</h2>
      <div class="emotion-distribution">
        <div
          v-for="emotion in emotionStats"
          :key="emotion.type"
          class="emotion-bar-item"
        >
          <div class="emotion-label">
            <span class="emotion-emoji">{{ emotion.emoji }}</span>
            <span class="emotion-name">{{ emotion.name }}</span>
            <span class="emotion-count">{{ emotion.count }}次</span>
          </div>
          <div class="emotion-bar-track">
            <div
              class="emotion-bar-fill"
              :style="{
                width: emotion.percentage + '%',
                background: emotion.color
              }"
            ></div>
          </div>
          <div class="emotion-percentage">{{ emotion.percentage.toFixed(1) }}%</div>
        </div>
      </div>
    </div>

    <!-- 情绪趋势图表 -->
    <div class="chart-section">
      <h2 class="section-title">情绪趋势（最近30天）</h2>
      <div class="trend-chart">
        <div class="chart-grid">
          <!-- Y轴刻度 -->
          <div class="y-axis">
            <div class="y-tick" v-for="i in 11" :key="i">{{ 10 - i + 1 }}</div>
          </div>

          <!-- 趋势线区域 -->
          <div class="chart-area">
            <svg class="trend-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
              <polyline
                :points="trendLinePoints"
                fill="none"
                stroke="url(#lineGradient)"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <defs>
                <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#66BB6A" />
                  <stop offset="50%" stop-color="#4CAF50" />
                  <stop offset="100%" stop-color="#2E7D32" />
                </linearGradient>
              </defs>
            </svg>

            <!-- 数据点 -->
            <div
              v-for="(point, index) in trendData"
              :key="index"
              class="data-point"
              :style="{
                left: (index / (trendData.length - 1)) * 100 + '%',
                bottom: (point.intensity / 10) * 100 + '%'
              }"
              :title="`${point.date}: ${point.intensity}/10`"
            >
              <div class="point-dot" :style="{ background: point.color }"></div>
            </div>
          </div>
        </div>

        <!-- X轴日期 -->
        <div class="x-axis">
          <div
            v-for="(label, index) in trendLabels"
            :key="index"
            class="x-tick"
          >
            {{ label }}
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选和搜索 -->
    <div class="filter-section">
      <h2 class="section-title">详细记录</h2>

      <div class="filter-controls">
        <select v-model="filterEmotion" class="filter-select">
          <option value="">所有情绪</option>
          <option value="joy">开心</option>
          <option value="calm">平静</option>
          <option value="sadness">难过</option>
          <option value="anxiety">焦虑</option>
          <option value="anger">愤怒</option>
          <option value="fear">恐惧</option>
        </select>

        <select v-model="filterTimeRange" class="filter-select">
          <option value="all">全部时间</option>
          <option value="week">最近一周</option>
          <option value="month">最近一月</option>
          <option value="3months">最近三月</option>
        </select>

        <input
          v-model="searchKeyword"
          type="text"
          class="search-input"
          placeholder="搜索日记内容..."
        />
      </div>
    </div>

    <!-- 记录列表 -->
    <div class="records-list">
      <div
        v-for="record in filteredRecords"
        :key="record.id"
        class="record-card"
        @click="viewRecordDetail(record)"
      >
        <div class="record-header">
          <div class="record-emotion">
            <span class="emotion-emoji-large">{{ record.emoji }}</span>
            <span class="emotion-name-large">{{ record.emotionLabel }}</span>
          </div>
          <div class="record-date">{{ record.date }}</div>
        </div>

        <div class="record-intensity">
          <span class="intensity-label">强度:</span>
          <div class="intensity-dots">
            <div
              v-for="i in 10"
              :key="i"
              class="intensity-dot"
              :class="{ active: i <= record.intensity }"
            ></div>
          </div>
          <span class="intensity-value">{{ record.intensity }}/10</span>
        </div>

        <p class="record-content">{{ record.content }}</p>

        <div v-if="record.triggers && record.triggers.length" class="record-triggers">
          <span class="trigger-label">触发因素:</span>
          <span
            v-for="trigger in record.triggers"
            :key="trigger"
            class="trigger-tag"
          >
            {{ trigger }}
          </span>
        </div>
      </div>

      <div v-if="filteredRecords.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <p class="empty-text">暂无符合条件的记录</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmotionHistoryPage',
  data() {
    return {
      diaries: [],
      filterEmotion: '',
      filterTimeRange: 'all',
      searchKeyword: ''
    }
  },
  computed: {
    // 总记录数
    totalRecords() {
      return this.diaries.length
    },

    // 连续记录天数
    continuousDays() {
      if (this.diaries.length === 0) return 0

      const sortedDates = this.diaries
        .map(d => new Date(d.date))
        .sort((a, b) => b - a)

      let continuous = 1
      for (let i = 0; i < sortedDates.length - 1; i++) {
        const diff = Math.abs(sortedDates[i] - sortedDates[i + 1])
        const daysDiff = Math.ceil(diff / (1000 * 60 * 60 * 24))
        if (daysDiff === 1) {
          continuous++
        } else {
          break
        }
      }

      return continuous
    },

    // 最常见情绪
    mostCommonEmotion() {
      if (this.diaries.length === 0) return '-'

      const emotionCounts = {}
      this.diaries.forEach(d => {
        emotionCounts[d.emotionLabel] = (emotionCounts[d.emotionLabel] || 0) + 1
      })

      return Object.keys(emotionCounts).reduce((a, b) =>
        emotionCounts[a] > emotionCounts[b] ? a : b
      )
    },

    mostCommonEmotionEmoji() {
      if (this.diaries.length === 0) return '😊'

      const diary = this.diaries.find(d => d.emotionLabel === this.mostCommonEmotion)
      return diary ? diary.emoji : '😊'
    },

    // 平均强度
    averageIntensity() {
      if (this.diaries.length === 0) return 0

      const sum = this.diaries.reduce((acc, d) => acc + d.intensity, 0)
      return (sum / this.diaries.length).toFixed(1)
    },

    // 情绪统计
    emotionStats() {
      const emotionMap = {
        joy: { name: '开心', emoji: '😊', color: 'linear-gradient(135deg, #FFA726, #FFB74D)', count: 0 },
        calm: { name: '平静', emoji: '😌', color: 'linear-gradient(135deg, #42A5F5, #64B5F6)', count: 0 },
        sadness: { name: '难过', emoji: '😢', color: 'linear-gradient(135deg, #7E57C2, #9575CD)', count: 0 },
        anxiety: { name: '焦虑', emoji: '😰', color: 'linear-gradient(135deg, #FFCA28, #FFD54F)', count: 0 },
        anger: { name: '愤怒', emoji: '😠', color: 'linear-gradient(135deg, #EF5350, #E57373)', count: 0 },
        fear: { name: '恐惧', emoji: '😨', color: 'linear-gradient(135deg, #AB47BC, #BA68C8)', count: 0 }
      }

      this.diaries.forEach(d => {
        if (emotionMap[d.emotion]) {
          emotionMap[d.emotion].count++
        }
      })

      const stats = Object.keys(emotionMap).map(type => ({
        type,
        ...emotionMap[type],
        percentage: this.totalRecords > 0
          ? (emotionMap[type].count / this.totalRecords) * 100
          : 0
      }))

      return stats.sort((a, b) => b.count - a.count)
    },

    // 趋势数据（最近30天）
    trendData() {
      const now = new Date()
      const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)

      const recentDiaries = this.diaries.filter(d =>
        new Date(d.date) >= thirtyDaysAgo
      )

      // 按日期分组
      const dataByDate = {}
      recentDiaries.forEach(d => {
        const dateKey = d.date.split(' ')[0]
        if (!dataByDate[dateKey]) {
          dataByDate[dateKey] = []
        }
        dataByDate[dateKey].push(d)
      })

      // 计算每天的平均强度
      return Object.keys(dataByDate)
        .sort()
        .map(date => {
          const dayDiaries = dataByDate[date]
          const avgIntensity = dayDiaries.reduce((sum, d) => sum + d.intensity, 0) / dayDiaries.length

          // 根据平均强度选择颜色
          let color = '#66BB6A'
          if (avgIntensity >= 7) color = '#EF5350'
          else if (avgIntensity >= 5) color = '#FFB74D'

          return {
            date,
            intensity: avgIntensity,
            color
          }
        })
    },

    // 趋势线坐标点
    trendLinePoints() {
      if (this.trendData.length === 0) return ''

      return this.trendData
        .map((point, index) => {
          const x = (index / (this.trendData.length - 1)) * 100
          const y = 100 - (point.intensity / 10) * 100
          return `${x},${y}`
        })
        .join(' ')
    },

    // 趋势图X轴标签
    trendLabels() {
      if (this.trendData.length === 0) return []

      // 显示5个日期标签
      const step = Math.max(1, Math.floor(this.trendData.length / 5))
      const labels = []

      for (let i = 0; i < this.trendData.length; i += step) {
        const date = this.trendData[i].date
        const [month, day] = date.split('-').slice(1)
        labels.push(`${month}/${day}`)
      }

      return labels
    },

    // 筛选后的记录
    filteredRecords() {
      let filtered = [...this.diaries]

      // 按情绪筛选
      if (this.filterEmotion) {
        filtered = filtered.filter(d => d.emotion === this.filterEmotion)
      }

      // 按时间范围筛选
      if (this.filterTimeRange !== 'all') {
        const now = new Date()
        let daysAgo = 7

        if (this.filterTimeRange === 'month') daysAgo = 30
        else if (this.filterTimeRange === '3months') daysAgo = 90

        const startDate = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000)
        filtered = filtered.filter(d => new Date(d.date) >= startDate)
      }

      // 按关键词搜索
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase()
        filtered = filtered.filter(d =>
          d.content.toLowerCase().includes(keyword)
        )
      }

      // 按日期倒序排序
      return filtered.sort((a, b) => new Date(b.date) - new Date(a.date))
    }
  },
  methods: {
    loadData() {
      try {
        const stored = localStorage.getItem('emotion_diaries')
        if (stored) {
          this.diaries = JSON.parse(stored)
        } else {
          // Mock数据（开发模式）
          this.diaries = this.generateMockData()
        }
      } catch (error) {
        console.error('加载情绪历史失败:', error)
      }
    },

    generateMockData() {
      const emotions = [
        { type: 'joy', label: '开心', emoji: '😊' },
        { type: 'calm', label: '平静', emoji: '😌' },
        { type: 'sadness', label: '难过', emoji: '😢' },
        { type: 'anxiety', label: '焦虑', emoji: '😰' },
        { type: 'anger', label: '愤怒', emoji: '😠' },
        { type: 'fear', label: '恐惧', emoji: '😨' }
      ]

      const triggers = ['学业压力', '人际关系', '家庭', '健康', '财务', '未来规划']
      const mockDiaries = []

      // 生成最近60天的数据
      for (let i = 0; i < 60; i++) {
        const date = new Date()
        date.setDate(date.getDate() - i)

        const emotion = emotions[Math.floor(Math.random() * emotions.length)]
        const intensity = Math.floor(Math.random() * 10) + 1

        mockDiaries.push({
          id: `mock-${i}`,
          date: date.toISOString().split('T')[0],
          emotion: emotion.type,
          emotionLabel: emotion.label,
          emoji: emotion.emoji,
          intensity,
          content: `这是第${i}天的日记内容，记录了今天的情绪状态...`,
          triggers: [triggers[Math.floor(Math.random() * triggers.length)]]
        })
      }

      return mockDiaries
    },

    goBack() {
      this.$router.back()
    },

    exportData() {
      // 导出为CSV格式
      const headers = ['日期', '情绪', '强度', '内容', '触发因素']
      const rows = this.filteredRecords.map(r => [
        r.date,
        r.emotionLabel,
        r.intensity,
        r.content,
        (r.triggers || []).join('; ')
      ])

      const csv = [
        headers.join(','),
        ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
      ].join('\n')

      const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `情绪历史_${new Date().toISOString().split('T')[0]}.csv`
      link.click()

      alert('数据导出成功！')
    },

    viewRecordDetail(record) {
      // 跳转到详细页面或打开模态框
      console.log('查看记录详情:', record)
    }
  },
  mounted() {
    this.loadData()
  }
}
</script>

<style scoped>
.emotion-history-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 50%, #A5D6A7 100%);
  padding: 20px;
  padding-bottom: 40px;
}

/* ========== 页面头部 ========== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.back-btn {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(76, 175, 80, 0.3);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: white;
  transform: translateX(-4px);
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1B5E20;
  margin: 0;
}

.export-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.export-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

/* ========== 统计概览 ========== */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.stat-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.15);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(76, 175, 80, 0.25);
}

.stat-icon {
  font-size: 48px;
  line-height: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #2E7D32;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

/* ========== 图表区域 ========== */
.chart-section {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 32px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.15);
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #1B5E20;
  margin-bottom: 24px;
}

/* 情绪分布条形图 */
.emotion-distribution {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.emotion-bar-item {
  display: grid;
  grid-template-columns: 180px 1fr 60px;
  gap: 12px;
  align-items: center;
}

.emotion-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.emotion-emoji {
  font-size: 20px;
}

.emotion-count {
  color: #666;
  font-size: 13px;
}

.emotion-bar-track {
  height: 24px;
  background: rgba(158, 158, 158, 0.1);
  border-radius: 12px;
  overflow: hidden;
}

.emotion-bar-fill {
  height: 100%;
  border-radius: 12px;
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.emotion-percentage {
  text-align: right;
  font-size: 14px;
  font-weight: 600;
  color: #4CAF50;
}

/* 趋势图 */
.trend-chart {
  margin-top: 16px;
}

.chart-grid {
  display: grid;
  grid-template-columns: 40px 1fr;
  gap: 12px;
  height: 300px;
  margin-bottom: 12px;
}

.y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-top: 8px;
  padding-bottom: 8px;
}

.y-tick {
  font-size: 12px;
  color: #666;
  text-align: right;
  line-height: 1;
}

.chart-area {
  position: relative;
  background: rgba(129, 199, 132, 0.05);
  border: 1px solid rgba(129, 199, 132, 0.2);
  border-radius: 12px;
  overflow: hidden;
}

.trend-svg {
  width: 100%;
  height: 100%;
}

.data-point {
  position: absolute;
  transform: translate(-50%, 50%);
  z-index: 10;
}

.point-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.data-point:hover .point-dot {
  transform: scale(1.5);
}

.x-axis {
  display: flex;
  justify-content: space-between;
  padding: 0 40px 0 52px;
}

.x-tick {
  font-size: 12px;
  color: #666;
  text-align: center;
}

/* ========== 筛选区域 ========== */
.filter-section {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 24px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.15);
}

.filter-controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.filter-select,
.search-input {
  padding: 12px 16px;
  border: 2px solid rgba(76, 175, 80, 0.3);
  border-radius: 12px;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.filter-select:focus,
.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  background: white;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

/* ========== 记录列表 ========== */
.records-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.record-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
}

.record-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(76, 175, 80, 0.25);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.record-emotion {
  display: flex;
  align-items: center;
  gap: 12px;
}

.emotion-emoji-large {
  font-size: 32px;
}

.emotion-name-large {
  font-size: 18px;
  font-weight: 700;
  color: #2E7D32;
}

.record-date {
  font-size: 14px;
  color: #666;
}

.record-intensity {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.intensity-label {
  font-size: 14px;
  font-weight: 600;
  color: #666;
}

.intensity-dots {
  display: flex;
  gap: 4px;
}

.intensity-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(158, 158, 158, 0.2);
  transition: all 0.3s ease;
}

.intensity-dot.active {
  background: linear-gradient(135deg, #66BB6A, #4CAF50);
  box-shadow: 0 2px 6px rgba(76, 175, 80, 0.4);
}

.intensity-value {
  font-size: 14px;
  font-weight: 600;
  color: #4CAF50;
}

.record-content {
  color: #333;
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 12px;
}

.record-triggers {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.trigger-label {
  font-size: 13px;
  font-weight: 600;
  color: #666;
}

.trigger-tag {
  padding: 4px 12px;
  background: rgba(102, 187, 106, 0.15);
  border: 1px solid rgba(102, 187, 106, 0.3);
  border-radius: 12px;
  font-size: 12px;
  color: #2E7D32;
  font-weight: 600;
}

/* ========== 空状态 ========== */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  color: #666;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .page-title {
    text-align: center;
  }

  .stats-overview {
    grid-template-columns: 1fr;
  }

  .emotion-bar-item {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .chart-section {
    padding: 20px;
  }

  .filter-controls {
    grid-template-columns: 1fr;
  }
}
</style>
