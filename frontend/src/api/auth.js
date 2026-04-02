import request from './request'

/**
 * 用户认证相关API
 * 对应后端路由: /api/auth/*
 */

/**
 * 用户登录
 * @param {Object} data - 登录信息
 * @param {string} data.username - 用户名或邮箱
 * @param {string} data.password - 密码
 * @returns {Promise} 返回token和用户信息
 */
export function login(data) {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data
  })
}

/**
 * 用户注册
 * @param {Object} data - 注册信息
 * @param {string} data.username - 用户名
 * @param {string} data.email - 邮箱
 * @param {string} data.password - 密码
 * @param {string} data.confirmPassword - 确认密码
 * @param {string} [data.phone] - 手机号（可选）
 * @param {string} [data.school] - 学校（可选）
 * @returns {Promise} 返回注册结果
 */
export function register(data) {
  return request({
    url: '/api/auth/register',
    method: 'post',
    data
  })
}

/**
 * 用户退出登录
 * @returns {Promise}
 */
export function logout() {
  return request({
    url: '/api/auth/logout',
    method: 'post'
  })
}

/**
 * 获取当前用户信息
 * @returns {Promise} 返回用户信息
 */
export function getUserInfo() {
  return request({
    url: '/api/auth/user',
    method: 'get'
  })
}

/**
 * 更新用户基本信息
 * @param {Object} data - 更新的用户信息
 * @param {string} [data.username] - 昵称
 * @param {string} [data.email] - 邮箱
 * @param {string} [data.phone] - 手机号
 * @param {string} [data.school] - 学校
 * @param {string} [data.avatar] - 头像
 * @returns {Promise}
 */
export function updateUserInfo(data) {
  return request({
    url: '/api/auth/user',
    method: 'put',
    data
  })
}

/**
 * 修改密码
 * @param {Object} data - 密码信息
 * @param {string} data.currentPassword - 当前密码
 * @param {string} data.newPassword - 新密码
 * @returns {Promise}
 */
export function changePassword(data) {
  return request({
    url: '/api/auth/change-password',
    method: 'post',
    data
  })
}

/**
 * 发送重置密码验证码（邮箱）
 * @param {Object} data
 * @param {string} data.email - 邮箱地址
 * @returns {Promise}
 */
export function sendResetPasswordCode(data) {
  return request({
    url: '/api/auth/reset-password/send-code',
    method: 'post',
    data
  })
}

/**
 * 验证重置密码验证码
 * @param {Object} data
 * @param {string} data.email - 邮箱地址
 * @param {string} data.code - 验证码
 * @returns {Promise} 返回重置token
 */
export function verifyResetPasswordCode(data) {
  return request({
    url: '/api/auth/reset-password/verify-code',
    method: 'post',
    data
  })
}

/**
 * 重置密码
 * @param {Object} data
 * @param {string} data.resetToken - 重置令牌
 * @param {string} data.newPassword - 新密码
 * @returns {Promise}
 */
export function resetPassword(data) {
  return request({
    url: '/api/auth/reset-password',
    method: 'post',
    data
  })
}

/**
 * 刷新访问令牌
 * @param {Object} data
 * @param {string} data.refreshToken - 刷新令牌
 * @returns {Promise} 返回新的access token
 */
export function refreshToken(data) {
  return request({
    url: '/api/auth/refresh-token',
    method: 'post',
    data
  })
}

/**
 * 验证邮箱
 * @param {Object} data
 * @param {string} data.token - 验证令牌（从邮件链接获取）
 * @returns {Promise}
 */
export function verifyEmail(data) {
  return request({
    url: '/api/auth/verify-email',
    method: 'post',
    data
  })
}

export default {
  login,
  register,
  logout,
  getUserInfo,
  updateUserInfo,
  changePassword,
  sendResetPasswordCode,
  verifyResetPasswordCode,
  resetPassword,
  refreshToken,
  verifyEmail
}
