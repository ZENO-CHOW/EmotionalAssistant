<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <!-- Logo区域 -->
      <div class="sidebar-header">
        <div class="logo">
          <span class="logo-icon">🔐</span>
          <span v-if="!sidebarCollapsed" class="logo-text">管理后台</span>
        </div>
        <button class="collapse-btn" @click="toggleSidebar">
          {{ sidebarCollapsed ? '→' : '←' }}
        </button>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: currentPath === item.path }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span v-if="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
          <span v-if="item.badge && !sidebarCollapsed" class="nav-badge">{{ item.badge }}</span>
        </router-link>
      </nav>

      <!-- 底部用户信息 -->
      <div class="sidebar-footer">
        <div class="admin-info">
          <div class="admin-avatar">{{ adminName.charAt(0) }}</div>
          <div v-if="!sidebarCollapsed" class="admin-details">
            <div class="admin-name">{{ adminName }}</div>
            <div class="admin-role">超级管理员</div>
          </div>
        </div>
        <button class="logout-btn" @click="handleLogout" :title="sidebarCollapsed ? '退出登录' : ''">
          <span class="logout-icon">🚪</span>
          <span v-if="!sidebarCollapsed">退出登录</span>
        </button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 顶部标题栏 -->
      <header class="content-header">
        <h1 class="page-title">{{ currentPageTitle }}</h1>
        <div class="header-actions">
          <button class="icon-btn" title="刷新">
            <span @click="handleRefresh">🔄</span>
          </button>
          <button class="icon-btn" title="通知">
            <span>🔔</span>
            <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
          </button>
        </div>
      </header>

      <!-- 路由内容区 -->
      <div class="content-body">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script>
import { adminLogout } from '@/api/admin.js'

export default {
  name: 'AdminLayout',
  data() {
    return {
      sidebarCollapsed: false,
      adminName: '管理员',
      unreadCount: 3,
      navItems: [
        {
          path: '/admin/dashboard',
          icon: '📊',
          label: '数据统计',
          badge: null
        },
        {
          path: '/admin/users',
          icon: '👥',
          label: '用户管理',
          badge: null
        },
        {
          path: '/admin/crisis',
          icon: '🚨',
          label: '危机预警',
          badge: 5
        },
        {
          path: '/admin/settings',
          icon: '⚙️',
          label: '系统设置',
          badge: null
        }
      ]
    }
  },
  computed: {
    currentPath() {
      return this.$route.path
    },
    currentPageTitle() {
      const item = this.navItems.find(item => item.path === this.currentPath)
      return item ? item.label : '管理后台'
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },

    handleRefresh() {
      location.reload()
    },

    async handleLogout() {
      if (!confirm('确定要退出登录吗？')) return

      try {
        await adminLogout()
      } catch (error) {
        console.error('退出登录失败:', error)
      } finally {
        // 清除本地存储
        localStorage.removeItem('admin_token')
        localStorage.removeItem('admin_info')
        // 跳转到登录页
        this.$router.push('/admin/login')
      }
    }
  },
  mounted() {
    // 检查登录状态
    const adminToken = localStorage.getItem('admin_token')
    if (!adminToken) {
      this.$router.push('/admin/login')
      return
    }

    // 加载管理员信息
    const adminInfo = localStorage.getItem('admin_info')
    if (adminInfo) {
      try {
        const info = JSON.parse(adminInfo)
        this.adminName = info.name || '管理员'
      } catch (error) {
        console.error('解析管理员信息失败:', error)
      }
    }
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
}

/* ========== 侧边栏 ========== */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 100;
}

.sidebar.collapsed {
  width: 80px;
}

/* ========== 侧边栏头部 ========== */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 32px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  white-space: nowrap;
}

.collapse-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

/* ========== 导航菜单 ========== */
.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.2s ease;
  margin-bottom: 8px;
  position: relative;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.nav-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.nav-label {
  font-size: 15px;
  font-weight: 500;
  white-space: nowrap;
}

.nav-badge {
  margin-left: auto;
  background: #ef4444;
  color: white;
  font-size: 12px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
}

/* ========== 侧边栏底部 ========== */
.sidebar-footer {
  padding: 16px 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-bottom: 12px;
}

.admin-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  flex-shrink: 0;
}

.admin-details {
  flex: 1;
  min-width: 0;
}

.admin-name {
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.admin-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 500;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.25);
  border-color: rgba(239, 68, 68, 0.5);
  color: #fecaca;
}

.logout-icon {
  font-size: 18px;
}

/* ========== 主内容区 ========== */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* ========== 内容头部 ========== */
.content-header {
  background: white;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 50;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.icon-btn {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: none;
  background: #f1f5f9;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  background: #e2e8f0;
  transform: translateY(-2px);
}

.notification-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ef4444;
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

/* ========== 内容主体 ========== */
.content-body {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}

/* ========== 滚动条样式 ========== */
.sidebar-nav::-webkit-scrollbar,
.content-body::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.content-body::-webkit-scrollbar-track {
  background: transparent;
}

.content-body::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

/* ========== 响应式 ========== */
@media (max-width: 1024px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
  }

  .main-content {
    margin-left: 260px;
  }

  .sidebar.collapsed + .main-content {
    margin-left: 80px;
  }
}

@media (max-width: 768px) {
  .content-header {
    padding: 16px 20px;
  }

  .content-body {
    padding: 20px;
  }

  .page-title {
    font-size: 20px;
  }
}
</style>
