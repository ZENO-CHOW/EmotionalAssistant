<template>
  <div class="crisis-monitor-tab">
    <!-- 预警概览卡片 -->
    <div class="alert-cards">
      <div class="alert-card critical">
        <div class="card-icon">🔴</div>
        <div class="card-content">
          <div class="card-number">{{ criticalCount }}</div>
          <div class="card-label">紧急预警</div>
        </div>
        <div class="card-action">
          <button class="quick-btn" @click="filterByLevel('critical')">
            查看
          </button>
        </div>
      </div>

      <div class="alert-card high">
        <div class="card-icon">🟡</div>
        <div class="card-content">
          <div class="card-number">{{ highCount }}</div>
          <div class="card-label">高危预警</div>
        </div>
        <div class="card-action">
          <button class="quick-btn" @click="filterByLevel('high')">
            查看
          </button>
        </div>
      </div>

      <div class="alert-card medium">
        <div class="card-icon">🟠</div>
        <div class="card-content">
          <div class="card-number">{{ mediumCount }}</div>
          <div class="card-label">中危预警</div>
        </div>
        <div class="card-action">
          <button class="quick-btn" @click="filterByLevel('medium')">
            查看
          </button>
        </div>
      </div>

      <div class="alert-card handled">
        <div class="card-icon">✅</div>
        <div class="card-content">
          <div class="card-number">{{ handledCount }}</div>
          <div class="card-label">已处理</div>
        </div>
        <div class="card-action">
          <button class="quick-btn" @click="showHandled = !showHandled">
            {{ showHandled ? '隐藏' : '查看' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 筛选工具栏 -->
    <div class="filter-toolbar">
      <div class="filter-group">
        <button
          v-for="filter in levelFilters"
          :key="filter.value"
          class="filter-chip"
          :class="{ active: selectedLevel === filter.value }"
          @click="selectedLevel = filter.value"
        >
          {{ filter.label }}
        </button>
      </div>

      <div class="filter-group">
        <select v-model="sortBy" class="sort-select">
          <option value="time_desc">时间↓</option>
          <option value="time_asc">时间↑</option>
          <option value="level_desc">风险↓</option>
        </select>

        <button class="refresh-btn" @click="loadCrisisList">
          <span class="refresh-icon">🔄</span>
          刷新
        </button>
      </div>
    </div>

    <!-- 危机列表 -->
    <div class="crisis-list">
      <div
        v-for="crisis in filteredCrisisList"
        :key="crisis.id"
        class="crisis-card"
        :class="[crisis.level, { handled: crisis.handled }]"
      >
        <!-- 左侧标记条 -->
        <div class="crisis-marker"></div>

        <!-- 主要内容 -->
        <div class="crisis-main">
          <!-- 头部信息 -->
          <div class="crisis-header">
            <div class="crisis-level-badge" :class="crisis.level">
              <span class="level-icon">{{ getLevelIcon(crisis.level) }}</span>
              <span class="level-text">{{ getLevelText(crisis.level) }}</span>
            </div>
            <div class="crisis-time">{{ crisis.time }}</div>
          </div>

          <!-- 用户信息 -->
          <div class="crisis-user-info">
            <div class="user-avatar-small">{{ crisis.userName.charAt(0) }}</div>
            <div class="user-text">
              <div class="user-name-bold">{{ crisis.userName }}</div>
              <div class="user-id-small">ID: {{ crisis.userId }}</div>
            </div>
          </div>

          <!-- 危机描述 -->
          <div class="crisis-description">
            <p class="crisis-text">{{ crisis.description }}</p>
          </div>

          <!-- 危机详情 -->
          <div class="crisis-details">
            <div class="detail-item" v-if="crisis.emotionIntensity">
              <span class="detail-icon">📊</span>
              <span class="detail-label">情绪强度：</span>
              <span class="detail-value">{{ crisis.emotionIntensity }}/10</span>
            </div>
            <div class="detail-item" v-if="crisis.triggerCount">
              <span class="detail-icon">🔔</span>
              <span class="detail-label">触发次数：</span>
              <span class="detail-value">{{ crisis.triggerCount }}次</span>
            </div>
            <div class="detail-item" v-if="crisis.keywords">
              <span class="detail-icon">🏷️</span>
              <span class="detail-label">关键词：</span>
              <span class="detail-value">{{ crisis.keywords.join(', ') }}</span>
            </div>
          </div>

          <!-- 处理信息（已处理） -->
          <div v-if="crisis.handled" class="handled-info">
            <div class="handled-badge">
              <span class="handled-icon">✅</span>
              <span>已处理</span>
            </div>
            <div class="handled-text">
              <span class="handled-by">处理人：{{ crisis.handledBy }}</span>
              <span class="handled-time">{{ crisis.handledTime }}</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="crisis-actions">
            <button
              v-if="!crisis.handled"
              class="action-btn primary"
              @click="handleCrisis(crisis)"
            >
              <span class="btn-icon">🚑</span>
              立即处理
            </button>
            <button class="action-btn secondary" @click="viewDetails(crisis)">
              <span class="btn-icon">👁️</span>
              查看详情
            </button>
            <button class="action-btn info" @click="contactUser(crisis)">
              <span class="btn-icon">📞</span>
              联系用户
            </button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredCrisisList.length === 0" class="empty-state">
        <div class="empty-icon">✨</div>
        <p class="empty-title">暂无危机预警</p>
        <p class="empty-desc">当前没有需要处理的危机事件</p>
      </div>
    </div>

    <!-- 处理危机弹窗 -->
    <CrisisHandleModal
      :visible="showHandleModal"
      :crisis="selectedCrisis"
      @close="showHandleModal = false"
      @confirm="onCrisisHandled"
    />
  </div>
</template>

<script>
import { getCrisisList, handleCrisis } from '@/api/admin.js'
import CrisisHandleModal from '@/components/admin/CrisisHandleModal.vue'

export default {
  name: 'CrisisMonitorTab',
  components: {
    CrisisHandleModal
  },
  data() {
    return {
      criticalCount: 3,
      highCount: 8,
      mediumCount: 12,
      handledCount: 45,
      selectedLevel: '',
      sortBy: 'time_desc',
      showHandled: false,
      crisisList: [],
      showHandleModal: false,
      selectedCrisis: null,
      levelFilters: [
        { label: '全部', value: '' },
        { label: '紧急', value: 'critical' },
        { label: '高危', value: 'high' },
        { label: '中危', value: 'medium' }
      ]
    }
  },
  computed: {
    filteredCrisisList() {
      let list = [...this.crisisList]

      // 筛选等级
      if (this.selectedLevel) {
        list = list.filter(c => c.level === this.selectedLevel)
      }

      // 筛选是否显示已处理
      if (!this.showHandled) {
        list = list.filter(c => !c.handled)
      }

      // 排序
      if (this.sortBy === 'time_desc') {
        list.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      } else if (this.sortBy === 'time_asc') {
        list.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
      } else if (this.sortBy === 'level_desc') {
        const levelOrder = { critical: 3, high: 2, medium: 1 }
        list.sort((a, b) => levelOrder[b.level] - levelOrder[a.level])
      }

      return list
    }
  },
  methods: {
    async loadCrisisList() {
      try {
        const response = await getCrisisList({
          level: this.selectedLevel,
          showHandled: this.showHandled
        })
        this.crisisList = response.data.list
      } catch (error) {
        console.error('加载危机列表失败:', error)
        // 使用模拟数据
        this.loadMockData()
      }
    },

    loadMockData() {
      this.crisisList = [
        {
          id: 1,
          level: 'critical',
          userId: 10234,
          userName: '张三',
          description: '连续多次表达自我伤害意图，情绪极度不稳定',
          time: '5分钟前',
          timestamp: new Date(Date.now() - 5 * 60 * 1000),
          emotionIntensity: 9,
          triggerCount: 5,
          keywords: ['自我伤害', '结束生命', '无法承受'],
          handled: false
        },
        {
          id: 2,
          level: 'high',
          userId: 10567,
          userName: '李四',
          description: '连续7天出现重度抑郁情绪，社交功能严重受损',
          time: '1小时前',
          timestamp: new Date(Date.now() - 60 * 60 * 1000),
          emotionIntensity: 8,
          triggerCount: 3,
          keywords: ['抑郁', '孤独', '绝望'],
          handled: false
        },
        {
          id: 3,
          level: 'medium',
          userId: 10892,
          userName: '王五',
          description: '夜间焦虑情绪明显，睡眠质量差',
          time: '3小时前',
          timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000),
          emotionIntensity: 7,
          triggerCount: 2,
          keywords: ['焦虑', '失眠', '压力'],
          handled: false
        },
        {
          id: 4,
          level: 'high',
          userId: 11023,
          userName: '赵六',
          description: '情绪崩溃，多次提及无法继续学业',
          time: '昨天',
          timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000),
          emotionIntensity: 8,
          triggerCount: 4,
          keywords: ['崩溃', '放弃', '学业压力'],
          handled: true,
          handledBy: '管理员A',
          handledTime: '昨天 18:30'
        }
      ]
    },

    filterByLevel(level) {
      this.selectedLevel = level
    },

    handleCrisis(crisis) {
      this.selectedCrisis = crisis
      this.showHandleModal = true
    },

    viewDetails(crisis) {
      this.$router.push(`/admin/crisis/${crisis.id}`)
    },

    contactUser(crisis) {
      alert(`联系用户 ${crisis.userName} (ID: ${crisis.userId})`)
    },

    async onCrisisHandled(handleData) {
      try {
        await handleCrisis(this.selectedCrisis.id, handleData)
        // 刷新列表
        this.loadCrisisList()
        alert('危机事件已标记为已处理')
      } catch (error) {
        console.error('处理危机失败:', error)
        alert('处理失败，请稍后重试')
      }
    },

    getLevelIcon(level) {
      const icons = {
        critical: '🔴',
        high: '🟡',
        medium: '🟠'
      }
      return icons[level] || '⚪'
    },

    getLevelText(level) {
      const texts = {
        critical: '紧急',
        high: '高危',
        medium: '中危'
      }
      return texts[level] || '未知'
    }
  },
  mounted() {
    this.loadCrisisList()
    // 每30秒自动刷新
    this.refreshTimer = setInterval(() => {
      this.loadCrisisList()
    }, 30000)
  },
  beforeUnmount() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer)
    }
  }
}
</script>

<style scoped>
.crisis-monitor-tab {
  max-width: 1200px;
  margin: 0 auto;
}

/* ========== 预警概览卡片 ========== */
.alert-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.alert-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-left: 4px solid;
  transition: all 0.3s ease;
}

.alert-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.alert-card.critical {
  border-color: #dc2626;
  background: linear-gradient(135deg, white, rgba(239, 68, 68, 0.05));
}

.alert-card.high {
  border-color: #f59e0b;
  background: linear-gradient(135deg, white, rgba(245, 158, 11, 0.05));
}

.alert-card.medium {
  border-color: #f97316;
  background: linear-gradient(135deg, white, rgba(249, 115, 22, 0.05));
}

.alert-card.handled {
  border-color: #10b981;
  background: linear-gradient(135deg, white, rgba(16, 185, 129, 0.05));
}

.card-icon {
  font-size: 40px;
}

.card-content {
  flex: 1;
}

.card-number {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.card-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.quick-btn {
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.05);
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #475569;
}

.quick-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

/* ========== 筛选工具栏 ========== */
.filter-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

.filter-chip {
  padding: 10px 20px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-chip:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
}

.filter-chip.active {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-color: #3b82f6;
  color: white;
}

.sort-select {
  padding: 10px 16px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #475569;
  cursor: pointer;
}

.sort-select:focus {
  outline: none;
  border-color: #3b82f6;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.refresh-icon {
  font-size: 16px;
}

/* ========== 危机列表 ========== */
.crisis-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.crisis-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  transition: all 0.3s ease;
}

.crisis-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  transform: translateX(4px);
}

.crisis-card.handled {
  opacity: 0.7;
}

.crisis-marker {
  width: 6px;
  flex-shrink: 0;
}

.crisis-card.critical .crisis-marker {
  background: linear-gradient(180deg, #dc2626, #ef4444);
}

.crisis-card.high .crisis-marker {
  background: linear-gradient(180deg, #d97706, #f59e0b);
}

.crisis-card.medium .crisis-marker {
  background: linear-gradient(180deg, #ea580c, #f97316);
}

.crisis-main {
  flex: 1;
  padding: 24px;
}

/* ========== 危机头部 ========== */
.crisis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.crisis-level-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 14px;
}

.crisis-level-badge.critical {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
}

.crisis-level-badge.high {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
}

.crisis-level-badge.medium {
  background: rgba(249, 115, 22, 0.15);
  color: #ea580c;
}

.level-icon {
  font-size: 18px;
}

.crisis-time {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 500;
}

/* ========== 用户信息 ========== */
.crisis-user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.user-avatar-small {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: 700;
  flex-shrink: 0;
}

.user-name-bold {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 2px;
}

.user-id-small {
  font-size: 13px;
  color: #94a3b8;
  font-family: 'Monaco', monospace;
}

/* ========== 危机描述 ========== */
.crisis-description {
  margin-bottom: 16px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 3px solid #ef4444;
}

.crisis-text {
  font-size: 15px;
  line-height: 1.6;
  color: #334155;
  font-weight: 500;
}

/* ========== 危机详情 ========== */
.crisis-details {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}

.detail-icon {
  font-size: 16px;
}

.detail-label {
  color: #64748b;
  font-weight: 500;
}

.detail-value {
  color: #1e293b;
  font-weight: 700;
}

/* ========== 已处理信息 ========== */
.handled-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 10px;
  margin-bottom: 16px;
}

.handled-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 700;
  color: #059669;
}

.handled-icon {
  font-size: 18px;
}

.handled-text {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #64748b;
}

/* ========== 操作按钮 ========== */
.crisis-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.5);
}

.action-btn.secondary {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.action-btn.secondary:hover {
  background: rgba(59, 130, 246, 0.2);
}

.action-btn.info {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.action-btn.info:hover {
  background: rgba(16, 185, 129, 0.2);
}

.btn-icon {
  font-size: 16px;
}

/* ========== 空状态 ========== */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 14px;
  color: #94a3b8;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .alert-cards {
    grid-template-columns: 1fr 1fr;
  }

  .filter-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    flex-wrap: wrap;
  }

  .crisis-actions {
    flex-direction: column;
  }

  .action-btn {
    justify-content: center;
  }
}
</style>
