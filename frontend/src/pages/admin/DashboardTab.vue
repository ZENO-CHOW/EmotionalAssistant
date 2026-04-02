<template>
  <div class="dashboard-tab">
    <!-- 核心指标卡片 -->
    <div class="metrics-grid">
      <div
        v-for="metric in metrics"
        :key="metric.key"
        class="metric-card"
        :style="{ borderColor: metric.color }"
      >
        <div class="metric-header">
          <span class="metric-icon">{{ metric.icon }}</span>
          <span class="metric-label">{{ metric.label }}</span>
        </div>
        <div class="metric-value" :style="{ color: metric.color }">
          {{ metric.value }}
        </div>
        <div class="metric-footer">
          <span class="metric-change" :class="metric.trend">
            {{ metric.change }}
          </span>
          <span class="metric-text">较上周</span>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-grid">
      <!-- 情绪分布图 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3 class="chart-title">📊 情绪类型分布</h3>
          <select v-model="emotionPeriod" class="period-select">
            <option value="week">最近7天</option>
            <option value="month">最近30天</option>
            <option value="year">最近一年</option>
          </select>
        </div>
        <div class="chart-body">
          <div class="emotion-chart">
            <div
              v-for="emotion in emotionDistribution"
              :key="emotion.type"
              class="emotion-bar"
            >
              <div class="emotion-info">
                <span class="emotion-emoji">{{ emotion.emoji }}</span>
                <span class="emotion-name">{{ emotion.name }}</span>
              </div>
              <div class="bar-wrapper">
                <div
                  class="bar-fill"
                  :style="{
                    width: emotion.percentage + '%',
                    background: emotion.color
                  }"
                ></div>
              </div>
              <span class="emotion-count">{{ emotion.count }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 活跃用户趋势 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3 class="chart-title">📈 活跃用户趋势</h3>
          <select v-model="userPeriod" class="period-select">
            <option value="week">最近7天</option>
            <option value="month">最近30天</option>
          </select>
        </div>
        <div class="chart-body">
          <div class="line-chart">
            <div
              v-for="(day, index) in userTrendData"
              :key="index"
              class="chart-column"
            >
              <div class="column-bar-wrapper">
                <div
                  class="column-bar"
                  :style="{
                    height: (day.count / maxUserCount) * 100 + '%',
                    background: 'linear-gradient(180deg, #3b82f6, #60a5fa)'
                  }"
                  :title="`${day.count} 人`"
                ></div>
              </div>
              <div class="column-label">{{ day.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 近期危机事件 -->
    <div class="section-card">
      <div class="section-header">
        <h3 class="section-title">🚨 近期危机预警</h3>
        <router-link to="/admin/crisis" class="view-all-link">
          查看全部 →
        </router-link>
      </div>
      <div class="crisis-list">
        <div
          v-for="crisis in recentCrisis"
          :key="crisis.id"
          class="crisis-item"
          :class="crisis.level"
        >
          <div class="crisis-badge">
            <span class="crisis-level-icon">{{ crisis.levelIcon }}</span>
            <span class="crisis-level-text">{{ crisis.levelText }}</span>
          </div>
          <div class="crisis-info">
            <div class="crisis-user">用户: {{ crisis.userName }}</div>
            <div class="crisis-desc">{{ crisis.description }}</div>
          </div>
          <div class="crisis-time">{{ crisis.time }}</div>
          <button
            class="crisis-action-btn"
            :class="{ handled: crisis.handled }"
            @click="handleCrisisClick(crisis)"
          >
            {{ crisis.handled ? '已处理' : '立即处理' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 系统健康状态 -->
    <div class="system-status-grid">
      <div class="status-card">
        <div class="status-icon">🖥️</div>
        <div class="status-info">
          <div class="status-label">服务器状态</div>
          <div class="status-value online">运行正常</div>
        </div>
      </div>
      <div class="status-card">
        <div class="status-icon">💾</div>
        <div class="status-info">
          <div class="status-label">数据库连接</div>
          <div class="status-value online">连接正常</div>
        </div>
      </div>
      <div class="status-card">
        <div class="status-icon">🔄</div>
        <div class="status-info">
          <div class="status-label">最后更新</div>
          <div class="status-value">{{ lastUpdateTime }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getStatisticsOverview, getCrisisList, getEmotionStatistics, getUserActivityStatistics, getRecentCrisisList } from '@/api/admin.js'

export default {
  name: 'DashboardTab',
  data() {
    return {
      emotionPeriod: 'week',
      userPeriod: 'week',
      lastUpdateTime: '刚刚',
      // 核心指标
      metrics: [],
      // 情绪分布
      emotionDistribution: [],
      // 用户趋势
      userTrendData: [],
      // 近期危机
      recentCrisis: []
    }
  },
  computed: {
    maxUserCount() {
      if (!this.userTrendData || this.userTrendData.length === 0) return 1
      return Math.max(...this.userTrendData.map(d => d.count), 1)
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await getStatisticsOverview()
        const data = response.data

        this.metrics = [
          {
            key: 'users',
            icon: '👥',
            label: '总用户数',
            value: data.users?.total?.toLocaleString() || '0',
            change: '',
            trend: 'up',
            color: '#3b82f6'
          },
          {
            key: 'emotions',
            icon: '😊',
            label: '情绪分析次数',
            value: data.totalDiaries?.toLocaleString() || '0',
            change: '',
            trend: 'up',
            color: '#10b981'
          },
          {
            key: 'crisis',
            icon: '🚨',
            label: '危机预警',
            value: data.pendingCrisisCount?.toLocaleString() || '0',
            change: '',
            trend: 'down',
            color: '#ef4444'
          },
          {
            key: 'active',
            icon: '📱',
            label: '今日活跃',
            value: data.todayActiveUsers?.toLocaleString() || '0',
            change: '',
            trend: 'up',
            color: '#8b5cf6'
          }
        ]
      } catch (error) {
        console.error('加载统计数据失败:', error)
      }

      await this.loadEmotionDistribution()
      await this.loadUserActivity()
      await this.loadRecentCrisis()
    },

    async loadEmotionDistribution() {
      try {
        const response = await getEmotionStatistics({ period: this.emotionPeriod })
        this.emotionDistribution = response.data || []
      } catch (error) {
        console.error('加载情绪分布失败:', error)
        this.emotionDistribution = []
      }
    },

    async loadUserActivity() {
      try {
        const response = await getUserActivityStatistics({ period: this.userPeriod })
        this.userTrendData = response.data || []
      } catch (error) {
        console.error('加载用户活跃度失败:', error)
        this.userTrendData = []
      }
    },

    async loadRecentCrisis() {
      try {
        const response = await getRecentCrisisList({ limit: 10 })
        this.recentCrisis = response.data || []
      } catch (error) {
        console.error('加载最近危机事件失败:', error)
        this.recentCrisis = []
      }
    },

    handleCrisisClick(crisis) {
      if (crisis.handled) return
      this.$router.push(`/admin/crisis?id=${crisis.id}`)
    },

    updateTime() {
      const now = new Date()
      this.lastUpdateTime = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`
    }
  },
  watch: {
    emotionPeriod() {
      this.loadEmotionDistribution()
    },
    userPeriod() {
      this.loadUserActivity()
    }
  },
  mounted() {
    this.loadData()
    this.updateTime()
    // 每分钟更新时间
    setInterval(() => {
      this.updateTime()
    }, 60000)
  }
}
</script>

<style scoped>
.dashboard-tab {
  max-width: 1400px;
  margin: 0 auto;
}

/* ========== 核心指标网格 ========== */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.metric-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border-left: 4px solid;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.metric-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.metric-icon {
  font-size: 28px;
}

.metric-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.metric-value {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 12px;
}

.metric-footer {
  display: flex;
  align-items: center;
  gap: 8px;
}

.metric-change {
  font-size: 14px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
}

.metric-change.up {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.metric-change.down {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.metric-text {
  font-size: 13px;
  color: #94a3b8;
}

/* ========== 图表网格 ========== */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.chart-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.period-select {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  color: #475569;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.period-select:hover {
  border-color: #3b82f6;
}

.period-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* ========== 情绪分布图 ========== */
.emotion-chart {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.emotion-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.emotion-info {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 100px;
}

.emotion-emoji {
  font-size: 24px;
}

.emotion-name {
  font-size: 14px;
  font-weight: 500;
  color: #475569;
}

.bar-wrapper {
  flex: 1;
  height: 32px;
  background: #f1f5f9;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.bar-fill {
  height: 100%;
  border-radius: 8px;
  transition: width 1s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.emotion-count {
  min-width: 60px;
  text-align: right;
  font-size: 16px;
  font-weight: 700;
  color: #334155;
}

/* ========== 折线图 ========== */
.line-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 8px;
  height: 200px;
  padding-top: 20px;
}

.chart-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.column-bar-wrapper {
  width: 100%;
  height: 180px;
  display: flex;
  align-items: flex-end;
}

.column-bar {
  width: 100%;
  border-radius: 8px 8px 0 0;
  transition: height 0.8s ease;
  cursor: pointer;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
}

.column-bar:hover {
  opacity: 0.8;
}

.column-label {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

/* ========== 危机列表 ========== */
.section-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.view-all-link {
  color: #3b82f6;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s ease;
}

.view-all-link:hover {
  color: #2563eb;
}

.crisis-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.crisis-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid;
  transition: all 0.2s ease;
}

.crisis-item.high {
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.05);
}

.crisis-item.medium {
  border-color: #f59e0b;
  background: rgba(245, 158, 11, 0.05);
}

.crisis-item:hover {
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.crisis-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.crisis-item.high .crisis-badge {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
}

.crisis-item.medium .crisis-badge {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
}

.crisis-level-icon {
  font-size: 16px;
}

.crisis-info {
  flex: 1;
  min-width: 0;
}

.crisis-user {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 4px;
}

.crisis-desc {
  font-size: 13px;
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.crisis-time {
  font-size: 12px;
  color: #94a3b8;
  white-space: nowrap;
}

.crisis-action-btn {
  padding: 8px 16px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.crisis-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.crisis-action-btn.handled {
  background: linear-gradient(135deg, #10b981, #059669);
  cursor: default;
}

.crisis-action-btn.handled:hover {
  transform: none;
  box-shadow: none;
}

/* ========== 系统状态 ========== */
.system-status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.status-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.status-icon {
  font-size: 36px;
}

.status-info {
  flex: 1;
}

.status-label {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
}

.status-value {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

.status-value.online {
  color: #10b981;
}

/* ========== 响应式 ========== */
@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .crisis-item {
    flex-wrap: wrap;
  }

  .crisis-action-btn {
    width: 100%;
  }
}
</style>
