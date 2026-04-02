<template>
  <div v-if="visible" class="export-modal-overlay" @click.self="close">
    <div class="export-modal">
      <div class="modal-header">
        <h2 class="modal-title">📊 数据导出配置</h2>
        <button class="close-btn" @click="close">✕</button>
      </div>

      <div class="modal-body">
        <!-- 导出格式 -->
        <div class="form-section">
          <h3 class="section-title">导出格式</h3>
          <div class="format-options">
            <label
              v-for="format in formats"
              :key="format.value"
              class="format-option"
              :class="{ active: exportConfig.format === format.value }"
            >
              <input
                type="radio"
                :value="format.value"
                v-model="exportConfig.format"
                hidden
              />
              <span class="format-icon">{{ format.icon }}</span>
              <div class="format-info">
                <div class="format-name">{{ format.name }}</div>
                <div class="format-desc">{{ format.desc }}</div>
              </div>
            </label>
          </div>
        </div>

        <!-- 时间范围 -->
        <div class="form-section">
          <h3 class="section-title">时间范围</h3>
          <div class="time-range-options">
            <label
              v-for="range in timeRanges"
              :key="range.value"
              class="time-option"
            >
              <input
                type="radio"
                :value="range.value"
                v-model="exportConfig.timeRange"
              />
              <span>{{ range.label }}</span>
            </label>
          </div>

          <!-- 自定义日期范围 -->
          <div v-if="exportConfig.timeRange === 'custom'" class="custom-date-range">
            <div class="date-input-group">
              <label>开始日期</label>
              <input
                type="date"
                v-model="exportConfig.startDate"
                class="date-input"
              />
            </div>
            <div class="date-input-group">
              <label>结束日期</label>
              <input
                type="date"
                v-model="exportConfig.endDate"
                class="date-input"
              />
            </div>
          </div>
        </div>

        <!-- 筛选条件 -->
        <div class="form-section">
          <h3 class="section-title">筛选条件</h3>
          <div class="filter-grid">
            <div class="filter-item">
              <label class="filter-label">用户状态</label>
              <select v-model="exportConfig.statusFilter" class="filter-select">
                <option value="">全部</option>
                <option value="active">活跃</option>
                <option value="inactive">非活跃</option>
              </select>
            </div>

            <div class="filter-item">
              <label class="filter-label">风险等级</label>
              <select v-model="exportConfig.riskFilter" class="filter-select">
                <option value="">全部</option>
                <option value="high">高危</option>
                <option value="medium">中危</option>
                <option value="low">低危</option>
              </select>
            </div>

            <div class="filter-item">
              <label class="filter-label">最小记录数</label>
              <input
                type="number"
                v-model.number="exportConfig.minRecords"
                class="filter-input"
                placeholder="0"
                min="0"
              />
            </div>
          </div>
        </div>

        <!-- 导出字段 -->
        <div class="form-section">
          <h3 class="section-title">导出字段</h3>
          <div class="fields-grid">
            <label
              v-for="field in availableFields"
              :key="field.value"
              class="field-checkbox"
            >
              <input
                type="checkbox"
                :value="field.value"
                v-model="exportConfig.fields"
              />
              <span>{{ field.label }}</span>
            </label>
          </div>
        </div>

        <!-- 高级选项 -->
        <div class="form-section">
          <h3 class="section-title">高级选项</h3>
          <div class="advanced-options">
            <label class="option-checkbox">
              <input
                type="checkbox"
                v-model="exportConfig.includeEmotionHistory"
              />
              <div class="option-info">
                <div class="option-name">包含情绪历史记录</div>
                <div class="option-desc">导出每个用户的详细情绪记录数据</div>
              </div>
            </label>

            <label class="option-checkbox">
              <input
                type="checkbox"
                v-model="exportConfig.includeStatistics"
              />
              <div class="option-info">
                <div class="option-name">包含统计分析</div>
                <div class="option-desc">添加情绪分布、趋势等统计数据</div>
              </div>
            </label>

            <label class="option-checkbox">
              <input
                type="checkbox"
                v-model="exportConfig.anonymize"
              />
              <div class="option-info">
                <div class="option-name">匿名化数据</div>
                <div class="option-desc">隐藏敏感信息（姓名、邮箱等）</div>
              </div>
            </label>
          </div>
        </div>

        <!-- 预计数据量 -->
        <div class="export-preview">
          <div class="preview-icon">📈</div>
          <div class="preview-info">
            <div class="preview-label">预计导出</div>
            <div class="preview-value">{{ estimatedRecords }} 条用户记录</div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="cancel-btn" @click="close">取消</button>
        <button class="export-btn" @click="handleExport" :disabled="isExporting">
          {{ isExporting ? '导出中...' : '开始导出' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExportDataModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    totalRecords: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      isExporting: false,
      exportConfig: {
        format: 'csv',
        timeRange: 'all',
        startDate: '',
        endDate: '',
        statusFilter: '',
        riskFilter: '',
        minRecords: 0,
        fields: ['id', 'name', 'email', 'registerTime', 'emotionCount', 'riskLevel', 'status'],
        includeEmotionHistory: false,
        includeStatistics: false,
        anonymize: false
      },
      formats: [
        {
          value: 'csv',
          name: 'CSV',
          icon: '📄',
          desc: '通用格式，兼容Excel'
        },
        {
          value: 'excel',
          name: 'Excel',
          icon: '📊',
          desc: '完整格式化表格'
        },
        {
          value: 'json',
          name: 'JSON',
          icon: '🔗',
          desc: '程序化数据处理'
        }
      ],
      timeRanges: [
        { value: 'all', label: '全部时间' },
        { value: 'today', label: '今天' },
        { value: 'week', label: '最近7天' },
        { value: 'month', label: '最近30天' },
        { value: 'quarter', label: '最近3个月' },
        { value: 'year', label: '最近一年' },
        { value: 'custom', label: '自定义范围' }
      ],
      availableFields: [
        { value: 'id', label: '用户ID' },
        { value: 'name', label: '姓名' },
        { value: 'email', label: '邮箱' },
        { value: 'phone', label: '手机号' },
        { value: 'school', label: '学校' },
        { value: 'registerTime', label: '注册时间' },
        { value: 'lastActive', label: '最后活跃' },
        { value: 'emotionCount', label: '情绪记录数' },
        { value: 'riskLevel', label: '风险等级' },
        { value: 'status', label: '账户状态' }
      ]
    }
  },
  computed: {
    estimatedRecords() {
      // 简单估算，实际应该根据筛选条件从后端获取
      return this.totalRecords
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },

    async handleExport() {
      this.isExporting = true

      try {
        // 🔧 开发模式：生成mock数据导出
        await new Promise(resolve => setTimeout(resolve, 1500))

        const mockData = this.generateMockExportData()
        this.downloadFile(mockData)

        alert('数据导出成功！')
        this.close()
      } catch (error) {
        console.error('导出失败:', error)
        alert('导出失败，请稍后重试')
      } finally {
        this.isExporting = false
      }
    },

    generateMockExportData() {
      // 生成mock数据用于导出
      const mockUsers = []

      for (let i = 1; i <= this.estimatedRecords; i++) {
        const user = {
          id: 10000 + i,
          name: this.exportConfig.anonymize ? `用户${i}` : `张三${i}`,
          email: this.exportConfig.anonymize ? `user${i}@***` : `user${i}@example.com`,
          phone: this.exportConfig.anonymize ? '138****5678' : '13800000000',
          school: '某某大学',
          registerTime: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          lastActive: `${i}小时前`,
          emotionCount: Math.floor(Math.random() * 100),
          riskLevel: ['low', 'medium', 'high'][Math.floor(Math.random() * 3)],
          status: ['active', 'inactive'][Math.floor(Math.random() * 2)]
        }

        // 只包含选中的字段
        const filteredUser = {}
        this.exportConfig.fields.forEach(field => {
          if (user[field] !== undefined) {
            filteredUser[field] = user[field]
          }
        })

        mockUsers.push(filteredUser)
      }

      return mockUsers
    },

    downloadFile(data) {
      const format = this.exportConfig.format

      if (format === 'csv') {
        this.downloadCSV(data)
      } else if (format === 'excel') {
        this.downloadExcel(data)
      } else if (format === 'json') {
        this.downloadJSON(data)
      }
    },

    downloadCSV(data) {
      if (data.length === 0) return

      // 生成CSV
      const headers = Object.keys(data[0])
      const rows = data.map(item =>
        headers.map(header => `"${item[header] || ''}"`).join(',')
      )

      const csv = [
        headers.join(','),
        ...rows
      ].join('\n')

      const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' })
      this.triggerDownload(blob, `用户数据_${this.getTimestamp()}.csv`)
    },

    downloadExcel(data) {
      // 简化版：使用CSV格式但命名为xlsx
      // 实际应该使用xlsx库生成真正的Excel文件
      this.downloadCSV(data)
      alert('注意：当前为演示模式，实际应使用xlsx库生成真正的Excel文件')
    },

    downloadJSON(data) {
      const json = JSON.stringify(data, null, 2)
      const blob = new Blob([json], { type: 'application/json;charset=utf-8;' })
      this.triggerDownload(blob, `用户数据_${this.getTimestamp()}.json`)
    },

    triggerDownload(blob, filename) {
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },

    getTimestamp() {
      return new Date().toISOString().split('T')[0]
    }
  },
  watch: {
    visible(newVal) {
      if (newVal) {
        // 重置结束日期为今天
        this.exportConfig.endDate = new Date().toISOString().split('T')[0]
      }
    }
  }
}
</script>

<style scoped>
.export-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.export-modal {
  background: white;
  border-radius: 20px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 24px 32px;
  border-bottom: 2px solid rgba(59, 130, 246, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e3a8a;
  margin: 0;
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(148, 163, 184, 0.1);
  border-radius: 50%;
  font-size: 20px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(148, 163, 184, 0.2);
  transform: rotate(90deg);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

/* ========== 表单区块 ========== */
.form-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1e40af;
  margin-bottom: 16px;
}

/* ========== 格式选择 ========== */
.format-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.format-option {
  padding: 16px;
  border: 2px solid rgba(59, 130, 246, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.format-option:hover {
  border-color: rgba(59, 130, 246, 0.4);
  background: rgba(59, 130, 246, 0.05);
}

.format-option.active {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.format-icon {
  font-size: 32px;
}

.format-name {
  font-size: 14px;
  font-weight: 700;
  color: #1e40af;
}

.format-desc {
  font-size: 12px;
  color: #64748b;
}

/* ========== 时间范围 ========== */
.time-range-options {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.time-option {
  padding: 8px 16px;
  border: 2px solid rgba(59, 130, 246, 0.2);
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.time-option:has(input:checked) {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
}

.custom-date-range {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 16px;
}

.date-input-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 6px;
}

.date-input {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid rgba(59, 130, 246, 0.2);
  border-radius: 8px;
  font-size: 14px;
}

/* ========== 筛选条件 ========== */
.filter-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.filter-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 6px;
}

.filter-select,
.filter-input {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid rgba(59, 130, 246, 0.2);
  border-radius: 8px;
  font-size: 14px;
}

/* ========== 导出字段 ========== */
.fields-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.field-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 2px solid rgba(59, 130, 246, 0.1);
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.field-checkbox:hover {
  background: rgba(59, 130, 246, 0.05);
}

.field-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* ========== 高级选项 ========== */
.advanced-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.option-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border: 2px solid rgba(59, 130, 246, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-checkbox:hover {
  background: rgba(59, 130, 246, 0.05);
}

.option-checkbox input[type="checkbox"] {
  width: 20px;
  height: 20px;
  margin-top: 2px;
  cursor: pointer;
}

.option-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e40af;
  margin-bottom: 4px;
}

.option-desc {
  font-size: 13px;
  color: #64748b;
}

/* ========== 预览 ========== */
.export-preview {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 197, 253, 0.1));
  border: 2px solid rgba(59, 130, 246, 0.2);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}

.preview-icon {
  font-size: 40px;
}

.preview-label {
  font-size: 13px;
  color: #64748b;
}

.preview-value {
  font-size: 20px;
  font-weight: 700;
  color: #1e40af;
}

/* ========== 底部 ========== */
.modal-footer {
  padding: 20px 32px;
  border-top: 2px solid rgba(59, 130, 246, 0.1);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  padding: 12px 24px;
  background: rgba(148, 163, 184, 0.1);
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  background: rgba(148, 163, 184, 0.2);
}

.export-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.export-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

.export-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* ========== 滚动条 ========== */
.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: rgba(148, 163, 184, 0.1);
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.3);
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: rgba(59, 130, 246, 0.5);
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .format-options,
  .filter-grid,
  .fields-grid {
    grid-template-columns: 1fr;
  }

  .custom-date-range {
    grid-template-columns: 1fr;
  }
}
</style>
