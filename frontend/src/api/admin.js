import request from './request'

/**
 * 管理员相关API
 * 对应后端路由: /api/admin/*
 */

// ==================== 认证相关 ====================

/**
 * 管理员登录
 * @param {Object} data
 * @param {string} data.username - 管理员账号
 * @param {string} data.password - 密码
 * @param {boolean} [data.remember] - 是否记住登录（7天）
 * @returns {Promise} 返回token和管理员信息
 */
export function adminLogin(data) {
  return request({
    url: '/api/admin/login',
    method: 'post',
    data
  })
}

/**
 * 管理员退出登录
 * @returns {Promise}
 */
export function adminLogout() {
  return request({
    url: '/api/admin/logout',
    method: 'post'
  })
}

/**
 * 获取管理员信息
 * @returns {Promise} 返回管理员信息
 */
export function getAdminInfo() {
  return request({
    url: '/api/admin/info',
    method: 'get'
  })
}

// ==================== 数据统计 ====================

/**
 * 获取数据统计概览（Dashboard）
 * @returns {Promise} 返回统计数据
 */
export function getStatisticsOverview() {
  return request({
    url: '/api/admin/statistics/overview',
    method: 'get'
  })
}

/**
 * 获取情绪分析统计
 * @param {Object} params
 * @param {string} [params.timeRange] - 时间范围 (week/month/quarter/year)
 * @returns {Promise} 返回情绪统计数据
 */
export function getEmotionStatistics(params) {
  return request({
    url: '/api/admin/statistics/emotions',
    method: 'get',
    params
  })
}

/**
 * 获取用户活跃度统计
 * @param {Object} params
 * @param {number} [params.days] - 最近天数
 * @returns {Promise} 返回活跃度数据
 */
export function getUserActivityStatistics(params) {
  return request({
    url: '/api/admin/statistics/user-activity',
    method: 'get',
    params
  })
}

/**
 * 获取危机预警趋势统计
 * @param {Object} params
 * @param {number} [params.days] - 最近天数
 * @returns {Promise} 返回趋势数据
 */
export function getCrisisTrendStatistics(params) {
  return request({
    url: '/api/admin/statistics/crisis-trend',
    method: 'get',
    params
  })
}

// ==================== 用户管理 ====================

/**
 * 获取用户列表
 * @param {Object} params
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @param {string} [params.keyword] - 搜索关键词
 * @param {string} [params.status] - 状态筛选 (active/inactive/risk)
 * @param {string} [params.sortBy] - 排序方式
 * @returns {Promise} 返回用户列表
 */
export function getUserList(params) {
  return request({
    url: '/api/admin/users',
    method: 'get',
    params
  })
}

/**
 * 获取用户详情
 * @param {string} userId - 用户ID
 * @returns {Promise} 返回用户详情
 */
export function getUserDetail(userId) {
  return request({
    url: `/api/admin/users/${userId}`,
    method: 'get'
  })
}

/**
 * 获取用户情绪历史详情
 * @param {string} userId - 用户ID
 * @param {Object} params
 * @param {string} [params.startDate] - 开始日期
 * @param {string} [params.endDate] - 结束日期
 * @param {string} [params.emotion] - 情绪类型筛选
 * @returns {Promise} 返回用户情绪历史
 */
export function getUserEmotionHistory(userId, params) {
  return request({
    url: `/api/admin/users/${userId}/emotion-history`,
    method: 'get',
    params
  })
}

/**
 * 更新用户状态
 * @param {string} userId - 用户ID
 * @param {Object} data
 * @param {string} data.status - 状态 (active/inactive/suspended)
 * @param {string} [data.reason] - 状态变更原因
 * @returns {Promise}
 */
export function updateUserStatus(userId, data) {
  return request({
    url: `/api/admin/users/${userId}/status`,
    method: 'put',
    data
  })
}

/**
 * 删除用户
 * @param {string} userId - 用户ID
 * @returns {Promise}
 */
export function deleteUser(userId) {
  return request({
    url: `/api/admin/users/${userId}`,
    method: 'delete'
  })
}

// ==================== 危机预警管理 ====================

/**
 * 获取危机预警列表
 * @param {Object} params
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @param {string} [params.level] - 风险等级 (critical/high/medium)
 * @param {string} [params.status] - 处理状态 (pending/handling/resolved)
 * @returns {Promise} 返回危机列表
 */
export function getCrisisList(params) {
  return request({
    url: '/api/admin/crisis',
    method: 'get',
    params
  })
}

/**
 * 获取最近的危机事件列表
 * @param {Object} params
 * @param {number} [params.limit] - 返回数量限制（默认10）
 * @param {string} [params.status] - 状态筛选 (pending/handling/resolved)
 * @returns {Promise} 返回最近的危机事件列表
 */
export function getRecentCrisisList(params) {
  return request({
    url: '/api/admin/crisis/recent',
    method: 'get',
    params
  })
}

/**
 * 获取危机详情
 * @param {string} crisisId - 危机ID
 * @returns {Promise} 返回危机详情
 */
export function getCrisisDetail(crisisId) {
  return request({
    url: `/api/admin/crisis/${crisisId}`,
    method: 'get'
  })
}

/**
 * 处理危机事件
 * @param {string} crisisId - 危机ID
 * @param {Object} data
 * @param {string} data.action - 处理措施
 * @param {string} data.result - 处理结果 (resolved/following/escalated/referred)
 * @param {string} [data.notes] - 备注说明
 * @param {string} [data.followUpPlan] - 后续跟进计划
 * @returns {Promise}
 */
export function handleCrisis(crisisId, data) {
  return request({
    url: `/api/admin/crisis/${crisisId}/handle`,
    method: 'post',
    data
  })
}

/**
 * 更新危机状态
 * @param {string} crisisId - 危机ID
 * @param {Object} data
 * @param {string} data.status - 状态 (pending/handling/resolved/closed)
 * @returns {Promise}
 */
export function updateCrisisStatus(crisisId, data) {
  return request({
    url: `/api/admin/crisis/${crisisId}/status`,
    method: 'put',
    data
  })
}

/**
 * 添加危机跟进记录
 * @param {string} crisisId - 危机ID
 * @param {Object} data
 * @param {string} data.content - 跟进内容
 * @param {string} [data.nextFollowUpTime] - 下次跟进时间
 * @returns {Promise}
 */
export function addCrisisFollowUp(crisisId, data) {
  return request({
    url: `/api/admin/crisis/${crisisId}/follow-up`,
    method: 'post',
    data
  })
}

// ==================== 系统设置 ====================

/**
 * 获取系统设置
 * @returns {Promise} 返回系统配置
 */
export function getSystemSettings() {
  return request({
    url: '/api/admin/settings',
    method: 'get'
  })
}

/**
 * 更新系统设置
 * @param {Object} data - 系统配置数据
 * @returns {Promise}
 */
export function updateSystemSettings(data) {
  return request({
    url: '/api/admin/settings',
    method: 'put',
    data
  })
}

/**
 * 获取危机预警阈值配置
 * @returns {Promise} 返回阈值配置
 */
export function getCrisisThresholds() {
  return request({
    url: '/api/admin/settings/crisis-thresholds',
    method: 'get'
  })
}

/**
 * 更新危机预警阈值
 * @param {Object} data
 * @param {number} data.intensityThreshold - 情绪强度阈值
 * @param {number} data.triggerCount - 触发次数
 * @param {number} data.timeWindow - 时间窗口（小时）
 * @param {Array} data.keywords - 关键词列表
 * @returns {Promise}
 */
export function updateCrisisThresholds(data) {
  return request({
    url: '/api/admin/settings/crisis-thresholds',
    method: 'put',
    data
  })
}

// ==================== 数据导出 ====================

/**
 * 导出用户数据
 * @param {Object} params
 * @param {string} [params.format] - 导出格式 (csv/excel/json)
 * @param {string} [params.timeRange] - 时间范围
 * @param {string} [params.startDate] - 开始日期
 * @param {string} [params.endDate] - 结束日期
 * @param {string} [params.statusFilter] - 状态筛选
 * @param {string} [params.riskFilter] - 风险等级筛选
 * @param {number} [params.minRecords] - 最小记录数
 * @param {Array} [params.fields] - 导出字段
 * @param {boolean} [params.includeEmotionHistory] - 包含情绪历史
 * @param {boolean} [params.includeStatistics] - 包含统计数据
 * @param {boolean} [params.anonymize] - 匿名化数据
 * @returns {Promise} 返回文件blob
 */
export function exportUserData(params) {
  return request({
    url: '/api/admin/export/users',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 导出情绪数据
 * @param {Object} params
 * @param {string} [params.format] - 导出格式
 * @param {string} [params.startDate] - 开始日期
 * @param {string} [params.endDate] - 结束日期
 * @returns {Promise} 返回文件blob
 */
export function exportEmotionData(params) {
  return request({
    url: '/api/admin/export/emotions',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 导出危机事件数据
 * @param {Object} params
 * @param {string} [params.format] - 导出格式
 * @param {string} [params.startDate] - 开始日期
 * @param {string} [params.endDate] - 结束日期
 * @returns {Promise} 返回文件blob
 */
export function exportCrisisData(params) {
  return request({
    url: '/api/admin/export/crisis',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 生成用户情绪分析报告
 * @param {string} userId - 用户ID
 * @param {Object} params
 * @param {string} [params.format] - 报告格式 (pdf/docx)
 * @param {string} [params.startDate] - 开始日期
 * @param {string} [params.endDate] - 结束日期
 * @returns {Promise} 返回报告文件blob
 */
export function generateUserReport(userId, params) {
  return request({
    url: `/api/admin/users/${userId}/generate-report`,
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// ==================== 系统日志 ====================

/**
 * 获取操作日志
 * @param {Object} params
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @param {string} [params.adminId] - 管理员ID
 * @param {string} [params.action] - 操作类型
 * @param {string} [params.startDate] - 开始日期
 * @param {string} [params.endDate] - 结束日期
 * @returns {Promise} 返回日志列表
 */
export function getOperationLogs(params) {
  return request({
    url: '/api/admin/logs/operations',
    method: 'get',
    params
  })
}

/**
 * 获取系统异常日志
 * @param {Object} params
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @param {string} [params.level] - 日志级别
 * @returns {Promise} 返回异常日志
 */
export function getErrorLogs(params) {
  return request({
    url: '/api/admin/logs/errors',
    method: 'get',
    params
  })
}

// ==================== 通知管理 ====================

/**
 * 发送系统通知给用户
 * @param {Object} data
 * @param {Array} data.userIds - 用户ID列表（空数组表示全部用户）
 * @param {string} data.title - 通知标题
 * @param {string} data.content - 通知内容
 * @param {string} [data.type] - 通知类型 (info/warning/urgent)
 * @returns {Promise}
 */
export function sendNotificationToUsers(data) {
  return request({
    url: '/api/admin/notifications/send',
    method: 'post',
    data
  })
}

/**
 * 获取通知发送历史
 * @param {Object} params
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @returns {Promise} 返回通知历史
 */
export function getNotificationHistory(params) {
  return request({
    url: '/api/admin/notifications/history',
    method: 'get',
    params
  })
}

export default {
  // 认证
  adminLogin,
  adminLogout,
  getAdminInfo,

  // 数据统计
  getStatisticsOverview,
  getEmotionStatistics,
  getUserActivityStatistics,
  getCrisisTrendStatistics,

  // 用户管理
  getUserList,
  getUserDetail,
  getUserEmotionHistory,
  updateUserStatus,
  deleteUser,

  // 危机预警
  getCrisisList,
  getCrisisDetail,
  handleCrisis,
  updateCrisisStatus,
  addCrisisFollowUp,

  // 系统设置
  getSystemSettings,
  updateSystemSettings,
  getCrisisThresholds,
  updateCrisisThresholds,

  // 数据导出
  exportUserData,
  exportEmotionData,
  exportCrisisData,
  generateUserReport,

  // 系统日志
  getOperationLogs,
  getErrorLogs,

  // 通知管理
  sendNotificationToUsers,
  getNotificationHistory
}
