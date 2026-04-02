import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/user/LoginPage.vue'
import RegisterPage from '../pages/user/RegisterPage.vue'
import ForgotPasswordPage from '../pages/user/ForgotPasswordPage.vue'
import HomePage from '../pages/user/HomePage.vue'
import EmotionHistoryPage from '../pages/user/EmotionHistoryPage.vue'

// 管理员页面（懒加载）
const AdminLoginPage = () => import('../pages/admin/AdminLoginPage.vue')
const AdminLayout = () => import('../pages/admin/AdminLayout.vue')
const DashboardTab = () => import('../pages/admin/DashboardTab.vue')
const UserManagementTab = () => import('../pages/admin/UserManagementTab.vue')
const CrisisMonitorTab = () => import('../pages/admin/CrisisMonitorTab.vue')
const SettingsTab = () => import('../pages/admin/SettingsTab.vue')
const UserEmotionHistoryPage = () => import('../pages/admin/UserEmotionHistoryPage.vue')

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPasswordPage
  },
  {
    path: '/home',
    name: 'Home',
    component: HomePage,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/emotion-history',
    name: 'EmotionHistory',
    component: EmotionHistoryPage,
    meta: { requiresAuth: true }  // 需要登录
  },
  // ========== 管理员路由 ==========
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLoginPage
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAdminAuth: true },  // 需要管理员权限
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: DashboardTab
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagementTab
      },
      {
        path: 'crisis',
        name: 'CrisisMonitor',
        component: CrisisMonitorTab
      },
      {
        path: 'settings',
        name: 'Settings',
        component: SettingsTab
      },
      {
        path: 'user-emotion-history/:userId',
        name: 'UserEmotionHistory',
        component: UserEmotionHistoryPage
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userToken = localStorage.getItem('token')  // 用户token
  const adminToken = localStorage.getItem('admin_token')  // 管理员token

  // 检查用户登录
  if (to.meta.requiresAuth && !userToken) {
    next('/login')
    return
  }

  // 检查管理员权限
  if (to.meta.requiresAdminAuth && !adminToken) {
    next('/admin/login')
    return
  }

  next()
})

export default router
