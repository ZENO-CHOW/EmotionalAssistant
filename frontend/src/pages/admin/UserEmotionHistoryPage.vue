<template>
  <div class="user-emotion-history-page">
    <!-- 头部导航 -->
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        ← 返回用户管理
      </button>
      <h1 class="page-title">用户情绪历史详情</h1>
      <div class="header-actions">
        <button class="action-btn" @click="generateReport">
          📄 生成报告
        </button>
        <button class="action-btn" @click="exportUserData">
          📊 导出数据
        </button>
      </div>
    </div>

    <!-- 用户基本信息 -->
    <div class="user-info-card">
      <div class="user-avatar">{{ userInfo.avatar || '👤' }}</div>
      <div class="user-details">
        <h2 class="user-name">{{ userInfo.name }}</h2>
        <div class="user-meta">
          <span class="meta-item">📧 {{ userInfo.email }}</span>
          <span class="meta-item">📱 {{ userInfo.phone }}</span>
          <span class="meta-item">🎓 {{ userInfo.school }}</span>
        </div>
        <div class="user-stats-row">
          <div class="stat-chip">
            <span class="stat-label">注册时间</span>
            <span class="stat-value">{{ userInfo.registerDate }}</span>
          </div>
          <div class="stat-chip">
            <span class="stat-label">情绪记录</span>
            <span class="stat-value">{{ totalEmotionRecords }}次</span>
          </div>
          <div class="stat-chip">
            <span class="stat-label">风险等级</span>
            <span class="stat-value" :class="`risk-${userInfo.riskLevel}`">
              {{ getRiskLabelChinese(userInfo.riskLevel) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 危机预警提示 -->
    <div v-if="hasCrisisWarning" class="crisis-alert">
      <div class="alert-icon">🚨</div>
      <div class="alert-content">
        <div class="alert-title">危机预警</div>
        <div class="alert-message">
          该用户最近{{ crisisWarningDays }}天内出现了{{ crisisCount }}次高危情绪记录，建议及时关注并采取干预措施。
        </div>
      </div>
      <button class="alert-action-btn" @click="handleCrisis">
        立即处理
      </button>
    </div>

    <!-- 情绪统计概览 -->
    <div class="stats-section">
      <h2 class="section-title">情绪统计概览</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">😊</div>
          <div class="stat-info">
            <div class="stat-number">{{ emotionStats.positive }}</div>
            <div class="stat-label">积极情绪</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">😐</div>
          <div class="stat-info">
            <div class="stat-number">{{ emotionStats.neutral }}</div>
            <div class="stat-label">中性情绪</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">😢</div>
          <div class="stat-info">
            <div class="stat-number">{{ emotionStats.negative }}</div>
            <div class="stat-label">消极情绪</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <div class="stat-number">{{ averageIntensity }}</div>
            <div class="stat-label">平均强度</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 情绪趋势图表 -->
    <div class="chart-section">
      <h2 class="section-title">情绪趋势分析（最近30天）</h2>
      <div class="trend-chart-container">
        <div class="chart-wrapper">
          <svg class="trend-chart" viewBox="0 0 100 50" preserveAspectRatio="none">
            <!-- 趋势线 -->
            <polyline
              :points="trendLinePoints"
              fill="none"
              stroke="#3b82f6"
              stroke-width="1"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <!-- 填充区域 -->
            <polygon
              :points="trendAreaPoints"
              fill="url(#areaGradient)"
              opacity="0.3"
            />
            <defs>
              <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#3b82f6" />
                <stop offset="100%" stop-color="#3b82f6" stop-opacity="0" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div class="chart-legend">
          <div class="legend-item">
            <div class="legend-dot" style="background: #ef5350"></div>
            <span>高危（≥8）</span>
          </div>
          <div class="legend-item">
            <div class="legend-dot" style="background: #ffb74d"></div>
            <span>中等（5-7）</span>
          </div>
          <div class="legend-item">
            <div class="legend-dot" style="background: #66bb6a"></div>
            <span>正常（<5）</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 情绪分布饼图 -->
    <div class="chart-section">
      <h2 class="section-title">情绪类型分布</h2>
      <div class="emotion-distribution">
        <div
          v-for="emotion in emotionDistribution"
          :key="emotion.type"
          class="distribution-bar"
        >
          <div class="bar-label">
            <span class="emotion-emoji">{{ emotion.emoji }}</span>
            <span class="emotion-name">{{ emotion.name }}</span>
            <span class="emotion-count">{{ emotion.count }}次</span>
          </div>
          <div class="bar-track">
            <div
              class="bar-fill"
              :style="{
                width: emotion.percentage + '%',
                background: emotion.color
              }"
            ></div>
          </div>
          <div class="bar-percentage">{{ emotion.percentage.toFixed(1) }}%</div>
        </div>
      </div>
    </div>

    <!-- 详细情绪记录 -->
    <div class="records-section">
      <h2 class="section-title">详细情绪记录</h2>

      <!-- 筛选器 -->
      <div class="filter-bar">
        <select v-model="filterTimeRange" class="filter-select">
          <option value="all">全部时间</option>
          <option value="week">最近一周</option>
          <option value="month">最近一月</option>
          <option value="3months">最近三月</option>
        </select>

        <select v-model="filterEmotion" class="filter-select">
          <option value="">所有情绪</option>
          <option value="joy">开心</option>
          <option value="calm">平静</option>
          <option value="sadness">难过</option>
          <option value="anxiety">焦虑</option>
          <option value="anger">愤怒</option>
          <option value="fear">恐惧</option>
        </select>

        <select v-model="filterRisk" class="filter-select">
          <option value="">所有风险等级</option>
          <option value="high">高危</option>
          <option value="medium">中等</option>
          <option value="low">正常</option>
        </select>
      </div>

      <!-- 记录列表 -->
      <div class="records-timeline">
        <div
          v-for="record in filteredRecords"
          :key="record.id"
          class="timeline-record"
          :class="`risk-level-${record.riskLevel}`"
        >
          <div class="record-timestamp">
            <div class="timestamp-date">{{ formatDate(record.date) }}</div>
            <div class="timestamp-time">{{ formatTime(record.date) }}</div>
          </div>

          <div class="record-indicator">
            <div class="indicator-dot" :class="`risk-${record.riskLevel}`"></div>
            <div class="indicator-line"></div>
          </div>

          <div class="record-content-card">
            <div class="record-header">
              <div class="emotion-tag">
                <span class="emotion-emoji">{{ record.emoji }}</span>
                <span class="emotion-label">{{ record.emotionLabel }}</span>
              </div>
              <div class="intensity-badge">
                强度 {{ record.intensity }}/10
              </div>
            </div>

            <p class="record-text">{{ record.content }}</p>

            <div v-if="record.triggers && record.triggers.length" class="record-triggers">
              <span
                v-for="trigger in record.triggers"
                :key="trigger"
                class="trigger-chip"
              >
                {{ trigger }}
              </span>
            </div>

            <div v-if="record.aiResponse" class="ai-response">
              <div class="ai-label">🤖 AI分析建议</div>
              <p class="ai-text">{{ record.aiResponse }}</p>
            </div>
          </div>
        </div>

        <div v-if="filteredRecords.length === 0" class="empty-records">
          <div class="empty-icon">📭</div>
          <p class="empty-text">暂无符合条件的情绪记录</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserEmotionHistoryPage',
  data() {
    return {
      userId: null,
      userInfo: {
        name: '张三',
        email: 'zhangsan@example.com',
        phone: '138****5678',
        school: '某某大学',
        registerDate: '2024-01-15',
        avatar: '👨',
        riskLevel: 'medium'
      },
      emotionRecords: [],
      filterTimeRange: 'all',
      filterEmotion: '',
      filterRisk: ''
    }
  },
  computed: {
    totalEmotionRecords() {
      return this.emotionRecords.length
    },

    // 危机预警
    hasCrisisWarning() {
      const recentRecords = this.getRecentRecords(7)
      const highRiskCount = recentRecords.filter(r => r.intensity >= 8).length
      return highRiskCount >= 3
    },

    crisisWarningDays() {
      return 7
    },

    crisisCount() {
      const recentRecords = this.getRecentRecords(7)
      return recentRecords.filter(r => r.intensity >= 8).length
    },

    // 情绪统计
    emotionStats() {
      const positive = this.emotionRecords.filter(r =>
        ['joy', 'calm'].includes(r.emotion)
      ).length

      const negative = this.emotionRecords.filter(r =>
        ['sadness', 'anxiety', 'anger', 'fear'].includes(r.emotion)
      ).length

      const neutral = this.emotionRecords.length - positive - negative

      return { positive, neutral, negative }
    },

    averageIntensity() {
      if (this.emotionRecords.length === 0) return 0
      const sum = this.emotionRecords.reduce((acc, r) => acc + r.intensity, 0)
      return (sum / this.emotionRecords.length).toFixed(1)
    },

    // 情绪分布
    emotionDistribution() {
      const emotionMap = {
        joy: { name: '开心', emoji: '😊', color: 'linear-gradient(135deg, #ffa726, #ffb74d)', count: 0 },
        calm: { name: '平静', emoji: '😌', color: 'linear-gradient(135deg, #42a5f5, #64b5f6)', count: 0 },
        sadness: { name: '难过', emoji: '😢', color: 'linear-gradient(135deg, #7e57c2, #9575cd)', count: 0 },
        anxiety: { name: '焦虑', emoji: '😰', color: 'linear-gradient(135deg, #ffca28, #ffd54f)', count: 0 },
        anger: { name: '愤怒', emoji: '😠', color: 'linear-gradient(135deg, #ef5350, #e57373)', count: 0 },
        fear: { name: '恐惧', emoji: '😨', color: 'linear-gradient(135deg, #ab47bc, #ba68c8)', count: 0 }
      }

      this.emotionRecords.forEach(r => {
        if (emotionMap[r.emotion]) {
          emotionMap[r.emotion].count++
        }
      })

      const total = this.emotionRecords.length
      return Object.keys(emotionMap)
        .map(type => ({
          type,
          ...emotionMap[type],
          percentage: total > 0 ? (emotionMap[type].count / total) * 100 : 0
        }))
        .sort((a, b) => b.count - a.count)
    },

    // 趋势数据
    trendData() {
      const now = new Date()
      const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)

      const recentRecords = this.emotionRecords.filter(r =>
        new Date(r.date) >= thirtyDaysAgo
      )

      // 按日期分组
      const dataByDate = {}
      recentRecords.forEach(r => {
        const dateKey = r.date.split(' ')[0]
        if (!dataByDate[dateKey]) {
          dataByDate[dateKey] = []
        }
        dataByDate[dateKey].push(r)
      })

      // 计算每天的平均强度
      return Object.keys(dataByDate)
        .sort()
        .map(date => {
          const dayRecords = dataByDate[date]
          const avgIntensity = dayRecords.reduce((sum, r) => sum + r.intensity, 0) / dayRecords.length
          return { date, intensity: avgIntensity }
        })
    },

    trendLinePoints() {
      if (this.trendData.length === 0) return ''

      return this.trendData
        .map((point, index) => {
          const x = (index / Math.max(1, this.trendData.length - 1)) * 100
          const y = 50 - (point.intensity / 10) * 50
          return `${x},${y}`
        })
        .join(' ')
    },

    trendAreaPoints() {
      if (this.trendData.length === 0) return ''

      const linePoints = this.trendLinePoints
      return `${linePoints} 100,50 0,50`
    },

    // 筛选后的记录
    filteredRecords() {
      let filtered = [...this.emotionRecords]

      // 时间筛选
      if (this.filterTimeRange !== 'all') {
        const now = new Date()
        let daysAgo = 7
        if (this.filterTimeRange === 'month') daysAgo = 30
        else if (this.filterTimeRange === '3months') daysAgo = 90

        const startDate = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000)
        filtered = filtered.filter(r => new Date(r.date) >= startDate)
      }

      // 情绪类型筛选
      if (this.filterEmotion) {
        filtered = filtered.filter(r => r.emotion === this.filterEmotion)
      }

      // 风险等级筛选
      if (this.filterRisk) {
        filtered = filtered.filter(r => r.riskLevel === this.filterRisk)
      }

      return filtered.sort((a, b) => new Date(b.date) - new Date(a.date))
    }
  },
  methods: {
    loadUserData() {
      // 从路由参数获取用户ID
      this.userId = this.$route.params.userId || '1'

      // 🔧 开发模式：使用Mock数据
      this.emotionRecords = this.generateMockRecords()
    },

    generateMockRecords() {
      const emotions = [
        { type: 'joy', label: '开心', emoji: '😊' },
        { type: 'calm', label: '平静', emoji: '😌' },
        { type: 'sadness', label: '难过', emoji: '😢' },
        { type: 'anxiety', label: '焦虑', emoji: '😰' },
        { type: 'anger', label: '愤怒', emoji: '😠' },
        { type: 'fear', label: '恐惧', emoji: '😨' }
      ]

      const triggers = ['学业压力', '人际关系', '家庭问题', '健康担忧', '经济压力', '未来迷茫']
      const mockRecords = []

      for (let i = 0; i < 45; i++) {
        const date = new Date()
        date.setDate(date.getDate() - i)

        const emotion = emotions[Math.floor(Math.random() * emotions.length)]
        const intensity = Math.floor(Math.random() * 10) + 1

        let riskLevel = 'low'
        if (intensity >= 8) riskLevel = 'high'
        else if (intensity >= 5) riskLevel = 'medium'

        mockRecords.push({
          id: `record-${i}`,
          date: date.toISOString(),
          emotion: emotion.type,
          emotionLabel: emotion.label,
          emoji: emotion.emoji,
          intensity,
          riskLevel,
          content: `第${i}天的情绪记录内容，描述了当时的心理状态和遇到的情况...`,
          triggers: [triggers[Math.floor(Math.random() * triggers.length)]],
          aiResponse: intensity >= 7
            ? '检测到您的情绪强度较高，建议进行深呼吸练习，或者尝试与信任的朋友交流。'
            : null
        })
      }

      return mockRecords
    },

    getRecentRecords(days) {
      const now = new Date()
      const startDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000)
      return this.emotionRecords.filter(r => new Date(r.date) >= startDate)
    },

    getRiskLabelChinese(level) {
      const map = {
        high: '高危',
        medium: '中等',
        low: '正常'
      }
      return map[level] || '未知'
    },

    formatDate(dateStr) {
      const date = new Date(dateStr)
      const month = date.getMonth() + 1
      const day = date.getDate()
      return `${month}月${day}日`
    },

    formatTime(dateStr) {
      const date = new Date(dateStr)
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      return `${hours}:${minutes}`
    },

    goBack() {
      this.$router.push('/admin/users')
    },

    generateReport() {
      alert('正在生成用户情绪分析报告...')
    },

    exportUserData() {
      const headers = ['日期', '情绪', '强度', '风险等级', '内容', '触发因素']
      const rows = this.emotionRecords.map(r => [
        r.date,
        r.emotionLabel,
        r.intensity,
        this.getRiskLabelChinese(r.riskLevel),
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
      link.download = `用户${this.userInfo.name}_情绪历史_${new Date().toISOString().split('T')[0]}.csv`
      link.click()

      alert('用户数据导出成功！')
    },

    handleCrisis() {
      alert('打开危机干预处理面板...')
    }
  },
  mounted() {
    this.loadUserData()
  }
}
</script>

<style scoped>
.user-emotion-history-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
  padding: 24px;
}

/* ========== 页面头部 ========== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

.back-btn {
  padding: 10px 20px;
  background: white;
  border: 2px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #1e40af;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  transform: translateX(-4px);
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e3a8a;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

/* ========== 用户信息卡片 ========== */
.user-info-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 24px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 24px;
}

.user-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 64px;
  flex-shrink: 0;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 28px;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 12px;
}

.user-meta {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.meta-item {
  font-size: 14px;
  color: #64748b;
}

.user-stats-row {
  display: flex;
  gap: 16px;
}

.stat-chip {
  padding: 12px 20px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #1e40af;
}

.stat-value.risk-high {
  color: #dc2626;
}

.stat-value.risk-medium {
  color: #f59e0b;
}

.stat-value.risk-low {
  color: #10b981;
}

/* ========== 危机预警 ========== */
.crisis-alert {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(248, 113, 113, 0.1));
  border: 2px solid rgba(239, 68, 68, 0.3);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
  display: flex;
  align-items: center;
  gap: 16px;
  animation: alertPulse 2s ease-in-out infinite;
}

@keyframes alertPulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(239, 68, 68, 0);
  }
}

.alert-icon {
  font-size: 40px;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-size: 18px;
  font-weight: 700;
  color: #dc2626;
  margin-bottom: 4px;
}

.alert-message {
  font-size: 14px;
  color: #991b1b;
}

.alert-action-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #ef5350, #f44336);
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.alert-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
}

/* ========== 统计区域 ========== */
.stats-section {
  margin-bottom: 24px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  font-size: 48px;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #1e40af;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
}

/* ========== 图表区域 ========== */
.chart-section {
  background: white;
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 24px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.trend-chart-container {
  margin-top: 16px;
}

.chart-wrapper {
  height: 300px;
  margin-bottom: 16px;
}

.trend-chart {
  width: 100%;
  height: 100%;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #64748b;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

/* ========== 情绪分布 ========== */
.emotion-distribution {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}

.distribution-bar {
  display: grid;
  grid-template-columns: 180px 1fr 60px;
  gap: 12px;
  align-items: center;
}

.bar-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
}

.emotion-emoji {
  font-size: 20px;
}

.emotion-count {
  font-size: 13px;
  color: #64748b;
}

.bar-track {
  height: 24px;
  background: rgba(148, 163, 184, 0.1);
  border-radius: 12px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 12px;
  transition: width 1s ease;
}

.bar-percentage {
  text-align: right;
  font-size: 14px;
  font-weight: 600;
  color: #3b82f6;
}

/* ========== 记录区域 ========== */
.records-section {
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

.filter-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.filter-select {
  padding: 12px 16px;
  border: 2px solid rgba(59, 130, 246, 0.2);
  border-radius: 12px;
  font-size: 14px;
  background: white;
  transition: all 0.3s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* ========== 时间线记录 ========== */
.records-timeline {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.timeline-record {
  display: grid;
  grid-template-columns: 100px 40px 1fr;
  gap: 16px;
}

.record-timestamp {
  text-align: right;
  padding-top: 8px;
}

.timestamp-date {
  font-size: 14px;
  font-weight: 600;
  color: #1e40af;
}

.timestamp-time {
  font-size: 13px;
  color: #64748b;
}

.record-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 8px;
}

.indicator-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  flex-shrink: 0;
}

.indicator-dot.risk-high {
  background: #ef5350;
}

.indicator-dot.risk-medium {
  background: #ffb74d;
}

.indicator-dot.risk-low {
  background: #66bb6a;
}

.indicator-line {
  width: 2px;
  flex: 1;
  background: rgba(148, 163, 184, 0.3);
  margin-top: 8px;
}

.timeline-record:last-child .indicator-line {
  display: none;
}

.record-content-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.record-content-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  transform: translateX(4px);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.emotion-tag {
  display: flex;
  align-items: center;
  gap: 8px;
}

.emotion-emoji {
  font-size: 24px;
}

.emotion-label {
  font-size: 16px;
  font-weight: 600;
  color: #1e40af;
}

.intensity-badge {
  padding: 4px 12px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #3b82f6;
}

.record-text {
  font-size: 15px;
  line-height: 1.6;
  color: #334155;
  margin-bottom: 12px;
}

.record-triggers {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.trigger-chip {
  padding: 4px 12px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: #1e40af;
}

.ai-response {
  background: rgba(147, 51, 234, 0.05);
  border-left: 3px solid #9333ea;
  padding: 12px;
  border-radius: 8px;
  margin-top: 12px;
}

.ai-label {
  font-size: 13px;
  font-weight: 600;
  color: #7c3aed;
  margin-bottom: 4px;
}

.ai-text {
  font-size: 14px;
  color: #6b21a8;
  margin: 0;
}

.empty-records {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  color: #64748b;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .user-info-card {
    flex-direction: column;
    text-align: center;
  }

  .user-stats-row {
    flex-direction: column;
  }

  .timeline-record {
    grid-template-columns: 1fr;
  }

  .record-timestamp {
    text-align: left;
  }

  .record-indicator {
    display: none;
  }

  .distribution-bar {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
</style>
