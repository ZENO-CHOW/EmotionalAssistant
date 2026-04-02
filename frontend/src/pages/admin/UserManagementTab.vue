<template>
  <div class="user-management-tab">
    <!-- 搜索和筛选栏 -->
    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input
          v-model="searchKeyword"
          type="text"
          class="search-input"
          placeholder="搜索用户ID、姓名、邮箱..."
          @input="handleSearch"
        />
      </div>

      <div class="filters">
        <select v-model="statusFilter" class="filter-select" @change="loadUsers">
          <option value="">全部状态</option>
          <option value="active">活跃</option>
          <option value="inactive">非活跃</option>
          <option value="suspended">已禁用</option>
        </select>

        <button class="export-btn" @click="handleExport">
          📥 导出数据
        </button>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="stats-bar">
      <div class="stat-item">
        <span class="stat-label">总用户数</span>
        <span class="stat-value">{{ totalUsers }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">今日新增</span>
        <span class="stat-value text-green">+{{ todayNew }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">高危用户</span>
        <span class="stat-value text-red">{{ riskUsers }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">活跃用户（7天）</span>
        <span class="stat-value text-blue">{{ activeUsers }}</span>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="user-table-wrapper">
      <table class="user-table">
        <thead>
          <tr>
            <th>用户ID</th>
            <th>用户信息</th>
            <th>注册时间</th>
            <th>最后活跃</th>
            <th>情绪记录</th>
            <th>风险等级</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in userList" :key="user.id" class="user-row">
            <td class="user-id">{{ user.id }}</td>
            <td class="user-info-cell">
              <div class="user-avatar">{{ user.name.charAt(0) }}</div>
              <div class="user-details">
                <div class="user-name">{{ user.name }}</div>
                <div class="user-email">{{ user.email }}</div>
              </div>
            </td>
            <td class="register-time">{{ user.registerTime }}</td>
            <td class="last-active">{{ user.lastActive }}</td>
            <td class="emotion-count">
              <span class="count-badge">{{ user.emotionCount }}</span>
            </td>
            <td class="risk-level">
              <span class="risk-badge" :class="user.riskLevel">
                {{ getRiskText(user.riskLevel) }}
              </span>
            </td>
            <td class="status">
              <span class="status-badge" :class="user.status">
                {{ getStatusText(user.status) }}
              </span>
            </td>
            <td class="actions">
              <button class="action-btn view" @click="viewUser(user)">
                查看
              </button>
              <button
                class="action-btn crisis"
                v-if="user.riskLevel === 'high'"
                @click="handleCrisisIntervention(user)"
              >
                干预
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 空状态 -->
      <div v-if="userList.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <p class="empty-text">没有找到匹配的用户</p>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <button
        class="page-btn"
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        ← 上一页
      </button>
      <div class="page-numbers">
        <button
          v-for="page in visiblePages"
          :key="page"
          class="page-number"
          :class="{ active: page === currentPage }"
          @click="changePage(page)"
        >
          {{ page }}
        </button>
      </div>
      <button
        class="page-btn"
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        下一页 →
      </button>
    </div>

    <!-- 用户详情弹窗 -->
    <UserDetailModal
      :visible="showDetailModal"
      :user="selectedUser"
      @close="showDetailModal = false"
    />

    <!-- 数据导出配置弹窗 -->
    <ExportDataModal
      :visible="showExportModal"
      :totalRecords="totalUsers"
      @close="showExportModal = false"
    />
  </div>
</template>

<script>
import { getUserList, exportUserData } from '@/api/admin.js'
import UserDetailModal from '@/components/admin/UserDetailModal.vue'
import ExportDataModal from '@/components/admin/ExportDataModal.vue'

export default {
  name: 'UserManagementTab',
  components: {
    UserDetailModal,
    ExportDataModal
  },
  data() {
    return {
      searchKeyword: '',
      statusFilter: '',
      currentPage: 1,
      pageSize: 10,
      totalUsers: 0,
      todayNew: 0,
      riskUsers: 0,
      activeUsers: 0,
      userList: [],
      totalPages: 1,
      showDetailModal: false,
      selectedUser: null,
      showExportModal: false
    }
  },
  computed: {
    visiblePages() {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2))
      let end = Math.min(this.totalPages, start + maxVisible - 1)

      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1)
      }

      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    }
  },
  methods: {
    async loadUsers() {
      try {
        const response = await getUserList({
          page: this.currentPage,
          pageSize: this.pageSize,
          keyword: this.searchKeyword,
          status: this.statusFilter
        })

        this.userList = response.data.list
        this.totalPages = response.data.totalPages
        this.totalUsers = response.data.total

        this.activeUsers = this.userList.filter(u => u.status === 'active').length
        this.riskUsers = this.userList.filter(u => u.riskLevel === 'high').length
      } catch (error) {
        console.error('加载用户列表失败:', error)
        this.userList = []
        this.totalPages = 0
        this.totalUsers = 0
      }
    },

    handleSearch() {
      // 防抖搜索
      clearTimeout(this.searchTimer)
      this.searchTimer = setTimeout(() => {
        this.currentPage = 1
        this.loadUsers()
      }, 500)
    },

    changePage(page) {
      if (page < 1 || page > this.totalPages) return
      this.currentPage = page
      this.loadUsers()
    },

    viewUser(user) {
      this.selectedUser = user
      this.showDetailModal = true
    },

    handleCrisisIntervention(user) {
      this.$router.push(`/admin/crisis?userId=${user.id}`)
    },

    handleExport() {
      // 打开导出配置弹窗
      this.showExportModal = true
    },

    getRiskText(level) {
      const map = {
        high: '高危',
        medium: '中危',
        low: '低危'
      }
      return map[level] || '未知'
    },

    getStatusText(status) {
      const map = {
        active: '活跃',
        inactive: '非活跃'
      }
      return map[status] || '未知'
    }
  },
  mounted() {
    this.loadUsers()
  }
}
</script>

<style scoped>
.user-management-tab {
  max-width: 1400px;
  margin: 0 auto;
}

/* ========== 工具栏 ========== */
.toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 300px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.search-box:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.search-icon {
  font-size: 20px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  color: #334155;
}

.filters {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-select {
  padding: 12px 16px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-select:hover {
  border-color: #cbd5e1;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.export-btn {
  padding: 12px 20px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.export-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}

/* ========== 统计栏 ========== */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-item {
  background: white;
  padding: 16px 20px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.stat-value.text-green {
  color: #10b981;
}

.stat-value.text-red {
  color: #ef4444;
}

.stat-value.text-blue {
  color: #3b82f6;
}

/* ========== 用户表格 ========== */
.user-table-wrapper {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table thead {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

.user-table th {
  padding: 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 700;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.user-row {
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.2s ease;
}

.user-row:hover {
  background: #f8fafc;
}

.user-table td {
  padding: 16px;
  font-size: 14px;
  color: #334155;
  vertical-align: middle;
}

.user-id {
  font-family: 'Monaco', 'Courier New', monospace;
  font-weight: 600;
  color: #64748b;
}

.user-info-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  font-weight: 700;
  flex-shrink: 0;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 2px;
}

.user-email {
  font-size: 12px;
  color: #94a3b8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.register-time,
.last-active {
  color: #64748b;
  font-size: 13px;
}

.count-badge {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border-radius: 12px;
  font-weight: 600;
  font-size: 13px;
}

.risk-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.risk-badge.high {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
}

.risk-badge.medium {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
}

.risk-badge.low {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
}

.status-badge.inactive {
  background: rgba(148, 163, 184, 0.15);
  color: #64748b;
}

.actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.action-btn.view {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.action-btn.view:hover {
  background: rgba(59, 130, 246, 0.2);
}

.action-btn.crisis {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.action-btn.crisis:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* ========== 空状态 ========== */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  color: #64748b;
}

/* ========== 分页 ========== */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.page-btn {
  padding: 10px 20px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  border-color: #3b82f6;
  color: #3b82f6;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 6px;
}

.page-number {
  width: 40px;
  height: 40px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-number:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.page-number.active {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-color: #3b82f6;
  color: white;
}

/* ========== 响应式 ========== */
@media (max-width: 1024px) {
  .user-table-wrapper {
    overflow-x: auto;
  }

  .user-table {
    min-width: 900px;
  }
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
  }

  .search-box {
    min-width: 100%;
  }

  .filters {
    width: 100%;
  }

  .filter-select,
  .export-btn {
    flex: 1;
  }

  .stats-bar {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
