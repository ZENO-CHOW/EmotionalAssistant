import request from './request'

/**
 * 情绪识别和日记相关API
 * 对应后端路由: /api/emotion/*
 */

// ==================== 情绪识别相关 ====================

/**
 * 获取情绪图片列表
 * @param {Object} params
 * @param {string} [params.category] - 图片分类 (positive/negative/neutral)
 * @param {number} [params.limit] - 返回数量
 * @returns {Promise} 返回图片列表
 */
export function getEmotionImages(params) {
  return request({
    url: '/api/emotion/images',
    method: 'get',
    params
  })
}

/**
 * 分析用户选择的图片，识别情绪
 * @param {Object} data
 * @param {string} data.userId - 用户ID
 * @param {Array} data.selectedImages - 选中的图片 [{imageId, selectionTime}]
 * @param {number} data.intensity - 情绪强度 (0-10)
 * @returns {Promise} 返回情绪分析结果
 */
export function analyzeEmotion(data) {
  return request({
    url: '/api/emotion/analyze',
    method: 'post',
    data
  })
}

/**
 * 获取情绪历史记录（简要列表）
 * @param {Object} params
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @param {string} [params.startDate] - 开始日期
 * @param {string} [params.endDate] - 结束日期
 * @returns {Promise} 返回情绪历史列表
 */
export function getEmotionHistory(params) {
  return request({
    url: '/api/emotion/history',
    method: 'get',
    params
  })
}

/**
 * 获取用户情绪统计数据
 * @param {Object} params
 * @param {string} [params.timeRange] - 时间范围 (week/month/quarter/year)
 * @returns {Promise} 返回统计数据
 */
export function getEmotionStatistics(params) {
  return request({
    url: '/api/emotion/statistics',
    method: 'get',
    params
  })
}

/**
 * 获取情绪趋势数据
 * @param {Object} params
 * @param {number} [params.days] - 最近天数 (默认30天)
 * @returns {Promise} 返回趋势数据
 */
export function getEmotionTrend(params) {
  return request({
    url: '/api/emotion/trend',
    method: 'get',
    params
  })
}

// ==================== 日记相关 ====================

/**
 * 创建情绪日记
 * @param {Object} data
 * @param {string} data.emotion - 情绪类型 (joy/calm/sadness/anxiety/anger/fear)
 * @param {string} data.emotionLabel - 情绪标签（中文）
 * @param {string} data.emoji - 情绪emoji
 * @param {number} data.intensity - 强度 (0-10)
 * @param {string} data.content - 日记内容
 * @param {Array} [data.triggers] - 触发因素
 * @param {Object} [data.bodyParts] - 身体部位感受
 * @param {Array} [data.selectedImages] - 选择的图片ID
 * @returns {Promise} 返回创建的日记
 */
export function createDiary(data) {
  return request({
    url: '/api/diary',
    method: 'post',
    data
  })
}

/**
 * 更新情绪日记
 * @param {string} diaryId - 日记ID
 * @param {Object} data - 更新的内容
 * @returns {Promise}
 */
export function updateDiary(diaryId, data) {
  return request({
    url: `/api/diary/${diaryId}`,
    method: 'put',
    data
  })
}

/**
 * 删除情绪日记
 * @param {string} diaryId - 日记ID
 * @returns {Promise}
 */
export function deleteDiary(diaryId) {
  return request({
    url: `/api/diary/${diaryId}`,
    method: 'delete'
  })
}

/**
 * 获取日记列表
 * @param {Object} params
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @param {string} [params.startDate] - 开始日期
 * @param {string} [params.endDate] - 结束日期
 * @param {string} [params.emotion] - 情绪类型筛选
 * @returns {Promise} 返回日记列表
 */
export function getDiaryList(params) {
  return request({
    url: '/api/diary/list',
    method: 'get',
    params
  })
}

/**
 * 获取日记详情
 * @param {string} diaryId - 日记ID
 * @returns {Promise} 返回日记详情
 */
export function getDiaryDetail(diaryId) {
  return request({
    url: `/api/diary/${diaryId}`,
    method: 'get'
  })
}

/**
 * 获取今日日记
 * @returns {Promise} 返回今日的日记（如果存在）
 */
export function getTodayDiary() {
  return request({
    url: '/api/diary/today',
    method: 'get'
  })
}

/**
 * 导出用户日记数据
 * @param {Object} params
 * @param {string} [params.format] - 导出格式 (csv/json/pdf)
 * @param {string} [params.startDate] - 开始日期
 * @param {string} [params.endDate] - 结束日期
 * @returns {Promise} 返回文件blob
 */
export function exportDiaryData(params) {
  return request({
    url: '/api/diary/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// ==================== DBT技能学习相关 ====================

/**
 * 获取DBT技能列表
 * @returns {Promise} 返回技能列表
 */
export function getDBTSkills() {
  return request({
    url: '/api/dbt/skills',
    method: 'get'
  })
}

/**
 * 获取用户DBT技能学习进度
 * @returns {Promise} 返回学习进度
 */
export function getDBTProgress() {
  return request({
    url: '/api/dbt/progress',
    method: 'get'
  })
}

/**
 * 更新DBT技能学习进度
 * @param {Object} data
 * @param {string} data.skillId - 技能ID
 * @param {number} data.progress - 进度 (0-100)
 * @returns {Promise}
 */
export function updateDBTProgress(data) {
  return request({
    url: '/api/dbt/progress',
    method: 'post',
    data
  })
}

/**
 * 获取DBT技能练习记录
 * @param {Object} params
 * @param {string} [params.skillId] - 技能ID
 * @returns {Promise} 返回练习记录
 */
export function getDBTPracticeRecords(params) {
  return request({
    url: '/api/dbt/practice-records',
    method: 'get',
    params
  })
}

/**
 * 创建DBT技能练习记录
 * @param {Object} data
 * @param {string} data.skillId - 技能ID
 * @param {number} data.duration - 练习时长（分钟）
 * @param {string} [data.notes] - 练习笔记
 * @returns {Promise}
 */
export function createDBTPracticeRecord(data) {
  return request({
    url: '/api/dbt/practice-records',
    method: 'post',
    data
  })
}

// ==================== 聊天对话相关 ====================

/**
 * 发送聊天消息
 * @param {Object} data
 * @param {string} data.message - 消息内容
 * @param {string} [data.session_id] - 会话ID
 * @param {string} [data.message_type] - 消息类型 (text/image_selection/body_selection/intensity_rating)
 * @param {Object} [data.metadata] - 附加数据
 * @returns {Promise} 返回AI回复和requires_input信息
 */
export function sendChatMessage(data) {
  return request({
    url: '/api/chat/message',
    method: 'post',
    data
  })
}

/**
 * 获取聊天历史
 * @param {Object} params
 * @param {string} [params.sessionId] - 会话ID
 * @param {number} [params.limit] - 返回数量
 * @returns {Promise} 返回聊天历史
 */
export function getChatHistory(params) {
  return request({
    url: '/api/chat/history',
    method: 'get',
    params
  })
}

/**
 * 清空聊天历史
 * @param {Object} data
 * @param {string} [data.sessionId] - 会话ID
 * @returns {Promise}
 */
export function clearChatHistory(data) {
  return request({
    url: '/api/chat/clear',
    method: 'post',
    data
  })
}

export default {
  // 情绪识别
  getEmotionImages,
  analyzeEmotion,
  getEmotionHistory,
  getEmotionStatistics,
  getEmotionTrend,

  // 日记管理
  createDiary,
  updateDiary,
  deleteDiary,
  getDiaryList,
  getDiaryDetail,
  getTodayDiary,
  exportDiaryData,

  // DBT技能
  getDBTSkills,
  getDBTProgress,
  updateDBTProgress,
  getDBTPracticeRecords,
  createDBTPracticeRecord,

  // 聊天对话
  sendChatMessage,
  getChatHistory,
  clearChatHistory
}
