<template>
  <div class="chat-tab" ref="chatTab">
    <div class="chat-container">
      <!-- 欢迎消息（首次进入） -->
      <div v-if="messages.length === 0" class="welcome-section">
        <div class="welcome-icon">🌱</div>
        <h2 class="welcome-title">嗨，我是小安</h2>
        <p class="welcome-text">
          焦虑、难过、生气的时候，我都在。<br>
          说说吧，我在听。
        </p>
      </div>

      <!-- 消息列表 -->
      <div
        v-for="(message, index) in messages"
        :key="message.id"
        :class="['message-item', message.role === 'user' ? 'message-user' : 'message-ai']"
      >
        {{ message.content }}
        <span class="timestamp">{{ message.time }}</span>
      </div>

      <!-- 图片选择器触发按钮 -->
      <div v-if="showImageButton && !showImageSelector && !emotionResult && !assessmentCompleted" class="action-buttons">
        <button class="action-btn primary" @click="showImageSelector = true">
          📸 开始选择图片识别情绪
        </button>
      </div>

      <!-- 图片选择器 -->
      <EmotionImageSelector
        v-if="showImageSelector"
        @confirm="handleImageSelection"
      />

      <!-- 身体不适询问 -->
      <div v-if="showDiscomfortQuestion" class="discomfort-question">
        <div class="question-card">
          <h3 class="question-title">在情绪的影响下，你的身体是否感受到了不适？</h3>
          <p class="question-subtitle">身体的感受能帮助我更好地理解你的情绪</p>
          <div class="question-buttons">
            <button class="question-btn yes-btn" @click="handleDiscomfortYes">
              有，我想选择
            </button>
            <button class="question-btn no-btn" @click="handleDiscomfortNo">
              没有
            </button>
          </div>
        </div>
      </div>

      <!-- 体感选择器 -->
      <BodySelector
        v-if="showBodySelector"
        @confirm="handleBodySelection"
        @skip="handleSkipBodySelection"
      />

      <!-- 情绪分析结果 -->
      <div v-if="emotionResult" class="result-card">
        <div class="result-header">
          <div class="result-icon">{{ emotionResult.emoji }}</div>
          <div class="result-info">
            <h3 class="result-title">{{ emotionResult.label }}</h3>
            <p class="result-confidence">可信度: {{ (emotionResult.confidence * 100).toFixed(0) }}%</p>
          </div>
        </div>
        <p class="result-desc">{{ emotionResult.description }}</p>
      </div>

      <!-- 情绪强度滑块 -->
      <EmotionIntensitySlider
        v-if="showIntensitySlider"
        v-model="intensity"
        :min="0"
        :max="10"
        label="情绪强度评分"
        class="intensity-slider"
        @confirm="handleIntensityConfirm"
      />

      <!-- 技能确认 -->
      <SkillConfirmation
        v-if="showSkillConfirmation"
        :visible="showSkillConfirmation"
        :skillName="skillConfirmationData.skillName"
        :introduction="skillConfirmationData.introduction"
        :options="skillConfirmationData.options"
        @confirm="handleSkillConfirmation"
      />

      <!-- 步骤引导 -->
      <StepGuidance
        v-if="showStepGuidance"
        :visible="showStepGuidance"
        :stepNumber="stepGuidanceData.stepNumber"
        :totalSteps="stepGuidanceData.totalSteps"
        :content="stepGuidanceData.content"
        :isLastStep="stepGuidanceData.isLastStep"
        @complete="handleStepComplete"
      />
    </div>

    <!-- 危机预警弹窗 -->
    <CrisisWarningModal
      :visible="showCrisisModal"
      @close="handleCloseCrisisModal"
      @call-hotline="handleCallHotline"
    />
  </div>
</template>

<script>
import EmotionImageSelector from '@/components/EmotionImageSelector.vue'
import BodySelector from '@/components/BodySelector.vue'
import EmotionIntensitySlider from '@/components/EmotionIntensitySlider.vue'
import CrisisWarningModal from '@/components/CrisisWarningModal.vue'
import SkillConfirmation from '@/components/SkillConfirmation.vue'
import StepGuidance from '@/components/StepGuidance.vue'
import { analyzeEmotion, sendChatMessage } from '@/api/emotion.js'

export default {
  name: 'ChatTab',
  components: {
    EmotionImageSelector,
    BodySelector,
    EmotionIntensitySlider,
    CrisisWarningModal,
    SkillConfirmation,
    StepGuidance
  },
  props: {
    // 接收消息列表
    messages: {
      type: Array,
      default: () => []
    },
    // 接收会话ID
    sessionId: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      intensity: 5,  // 情绪强度 0-10
      showImageSelector: false, // 是否显示图片选择器
      showDiscomfortQuestion: false, // 是否显示身体不适询问
      showBodySelector: false, // 是否显示体感选择器
      showIntensitySlider: false, // 是否显示情绪强度滑块
      selectedImageData: null, // 暂存选择的图片数据
      selectedBodyParts: [], // 选择的身体部位
      emotionResult: null, // 情绪分析结果
      analyzing: false, // 是否正在分析
      showImageButton: false, // 是否显示图片选择按钮
      showCrisisModal: false, // 是否显示危机预警弹窗
      assessmentCompleted: false, // 情绪评估是否已完成
      hasPromptedAssessment: false, // 是否已经提示过进行评估

      // 技能确认相关
      showSkillConfirmation: false,
      skillConfirmationData: {
        skillName: '',
        introduction: '',
        options: []
      },

      // 步骤引导相关
      showStepGuidance: false,
      stepGuidanceData: {
        stepNumber: 1,
        totalSteps: 1,
        content: '',
        isLastStep: false
      }
    }
  },
  computed: {
    // 判断是否正在进行情绪评估
    isAssessmentInProgress() {
      return this.showImageSelector ||
             this.showDiscomfortQuestion ||
             this.showBodySelector ||
             (this.emotionResult !== null && !this.assessmentCompleted)
    }
  },
  watch: {
    // 监听消息变化，自动滚动到底部
    messages: {
      handler() {
        this.$nextTick(() => {
          this.scrollToBottom()
        })

        // 前端不再主动触发评估，完全由后端的 requires_input 字段驱动
      },
      deep: true
    },
    // 监听评估状态变化，通知父组件
    isAssessmentInProgress: {
      handler(newValue) {
        this.$emit('assessment-status-change', newValue)
      },
      immediate: true
    }
  },
  methods: {
    async handleImageSelection(data) {
      console.log('用户选择的图片:', data)

      this.showImageSelector = false

      // 提取所有图片URL
      const imageUrls = data.selectedImages.map(img => img.url)

      await this.sendChatMessageWithState(
        '用户已选择情绪图片',
        'image_selection',
        {
          selected_images: data.selectedImages,
          image_urls: imageUrls
        }
      )
    },

    handleDiscomfortYes() {
      console.log('用户选择：有身体不适')

      // 关闭询问对话框，显示身体选择器
      this.showDiscomfortQuestion = false
      this.showBodySelector = true

      // 发送AI消息：引导选择身体部位
      this.$emit('add-message', {
        role: 'assistant',
        content: '好的，请告诉我你的身体哪些地方感到不舒服，这能帮助我更准确地理解你的感受。'
      })
    },

    handleDiscomfortNo() {
      console.log('用户选择：没有身体不适')

      this.showDiscomfortQuestion = false
      this.selectedBodyParts = []

      this.sendChatMessageWithState('我没有身体不适的感觉', 'body_selection', {
        selected_parts: []
      })
    },

    async handleBodySelection(bodyData) {
      console.log('用户选择的身体部位:', bodyData)

      this.showBodySelector = false

      await this.sendChatMessageWithState(
        '用户已选择身体部位',
        'body_selection',
        { selected_parts: bodyData.selectedParts }
      )
    },

    async handleSkipBodySelection() {
      console.log('用户跳过了身体部位选择')

      this.showBodySelector = false

      await this.sendChatMessageWithState(
        '用户跳过身体部位选择',
        'body_selection',
        { selected_parts: [] }
      )
    },

    async analyzeEmotionWithBodyData() {
      this.analyzing = true

      // 发送AI消息：正在分析
      this.$emit('add-message', {
        role: 'assistant',
        content: '正在分析你的情绪...'
      })

      try {
        // 调用真实API分析情绪
        const response = await analyzeEmotion({
          selectedImages: this.selectedImageData.selectedImages,
          intensity: this.intensity
        })

        console.log('✅ 情绪分析结果:', response)

        // 保存分析结果
        this.emotionResult = {
          type: response.emotion.emotionType,
          label: response.emotion.emotionLabel,
          confidence: response.emotion.confidence,
          emoji: response.emotion.emoji,
          description: response.emotion.description
        }

        // 生成包含身体部位的消息 - 更有共情的表达
        let message = ''

        // 根据情绪强度和类型生成更有共情的描述
        if (this.intensity >= 7) {
          message = `我感受到你现在的情绪比较强烈，识别出的情绪是${this.emotionResult.label}。`
        } else if (this.intensity >= 4) {
          message = `我理解了，你现在的情绪是${this.emotionResult.label}，强度处于中等水平。`
        } else {
          message = `我理解了，你现在的情绪强度比较温和，识别出的情绪是${this.emotionResult.label}。`
        }

        if (this.selectedBodyParts.length > 0) {
          message += `我也注意到你的身体有不适感，这些身心反应都是正常的。`
        }

        // 添加情绪描述，但避免重复
        if (this.emotionResult.description && !message.includes(this.emotionResult.description)) {
          message += this.emotionResult.description
        }

        // 发送AI消息：分析结果
        this.$emit('add-message', {
          role: 'assistant',
          content: message
        })

        // 检查是否需要危机预警（基于强度和情绪类型）
        const hasHighIntensity = this.intensity >= 8
        const isNegativeEmotion = ['anxiety', 'sadness', 'fear'].includes(response.emotion.emotionType)

        if (hasHighIntensity && isNegativeEmotion) {
          this.showCrisisModal = true
          console.warn('检测到危机情况，已触发危机预警弹窗')
        }

        // 不在这里推荐DBT技能，等待用户确认情绪强度后再推荐
        // await this.recommendDBTSkills(response.emotion.emotionType, this.intensity)

      } catch (error) {
        console.error('❌ 情绪分析失败:', error)

        // 发送错误消息
        this.$emit('add-message', {
          role: 'assistant',
          content: '抱歉，情绪分析遇到了一些问题。你可以试着用文字告诉我你的感受。'
        })
      } finally {
        this.analyzing = false
      }
    },

    async handleIntensityConfirm(value) {
      console.log('用户确认情绪强度:', value)
      this.intensity = value

      this.showIntensitySlider = false

      await this.sendChatMessageWithState(
        '用户已确认情绪强度',
        'intensity_rating',
        { intensity: value }
      )

      this.assessmentCompleted = true
    },

    getEmotionLabel(emotionType) {
      const labelMap = {
        'anxiety': '焦虑',
        'sadness': '难过',
        'joy': '开心',
        'anger': '生气',
        'calm': '平静',
        'fear': '害怕'
      }
      return labelMap[emotionType] || '未知'
    },

    getEmotionEmoji(emotionType) {
      const emojiMap = {
        'anxiety': '😰',
        'sadness': '😢',
        'joy': '😊',
        'anger': '😠',
        'fear': '😨',
        'neutral': '😐'
      }
      return emojiMap[emotionType] || '🤔'
    },

    async recommendDBTSkills(emotionType, intensity) {
      // 根据情绪类型和强度选择最合适的一个DBT技能
      const skillRecommendations = {
        'anxiety': {
          high: { skill: 'TIPP技能', intro: '当焦虑很强烈的时候，TIPP技能可以帮助你快速降低情绪强度。', steps: ['温度：用冷水洗脸或含冰块，激活身体的潜水反射', '强烈运动：做30秒到1分钟的剧烈运动，比如原地跑步或开合跳', '调整呼吸：深呼吸，让呼气比吸气长', '渐进式肌肉放松：从头到脚依次紧张再放松各个肌肉群'] },
          medium: { skill: '正念呼吸', intro: '正念呼吸可以帮助你把注意力从焦虑的想法中拉回来，专注于当下。', steps: ['找一个舒适的姿势坐下或躺下', '把注意力放在呼吸上，感受空气进出鼻腔', '当思绪飘走时，温柔地把注意力带回呼吸', '持续3-5分钟，慢慢延长时间'] },
          low: { skill: '接地技术', intro: '接地技术可以帮助你稳定情绪，感受当下的安全。', steps: ['用5-4-3-2-1法：说出5样你看到的东西', '说出4样你能触摸到的东西', '说出3样你听到的声音', '说出2样你闻到的气味', '说出1样你尝到的味道'] }
        },
        'anger': {
          high: { skill: 'TIPP技能', intro: '当愤怒很强烈的时候，TIPP技能可以帮助你快速冷静下来。', steps: ['温度：用冷水洗脸或含冰块，激活身体的潜水反射', '强烈运动：做30秒到1分钟的剧烈运动，释放愤怒的能量', '调整呼吸：深呼吸，让呼气比吸气长', '渐进式肌肉放松：从头到脚依次紧张再放松各个肌肉群'] },
          medium: { skill: 'STOP技能', intro: 'STOP技能可以帮助你在愤怒升级前暂停下来，做出更好的选择。', steps: ['停下来：意识到自己在生气，暂停当前的行动', '后退一步：从情境中抽离，给自己一点空间', '观察：注意自己的想法、感受和身体反应', '继续前进：选择一个有效的应对方式'] },
          low: { skill: '相反行动', intro: '当愤怒不太强烈时，相反行动可以帮助你改变情绪。', steps: ['识别愤怒带来的冲动，比如想要攻击或指责', '做相反的行为：温和地说话，放松身体', '用友善的态度对待让你生气的人或事', '持续这个行为直到情绪开始改变'] }
        },
        'sadness': {
          high: { skill: '自我安抚', intro: '当难过很强烈的时候，自我安抚可以帮助你照顾好自己。', steps: ['视觉：看一些美好的图片或风景', '听觉：听舒缓的音乐或自然的声音', '嗅觉：闻喜欢的香味，比如花香或精油', '味觉：吃一些喜欢的食物，慢慢品尝', '触觉：抱一个柔软的抱枕，或者泡个热水澡'] },
          medium: { skill: '驾驭情绪之波', intro: '驾驭情绪之波可以帮助你接纳难过，让它自然流动。', steps: ['承认并接纳这份难过的情绪', '不要试图压制或逃避它', '想象情绪像海浪一样，会升起也会落下', '观察情绪的变化，不做评判', '提醒自己：这个情绪会过去的'] },
          low: { skill: '积极体验', intro: '当难过不太强烈时，积极体验可以帮助你提升情绪。', steps: ['做一件让你感到愉快的事情', '全身心投入，专注于当下的体验', '注意这个活动带来的积极感受', '记录下这些美好的时刻'] }
        },
        'fear': {
          high: { skill: 'TIPP技能', intro: '当恐惧很强烈的时候，TIPP技能可以帮助你快速平静下来。', steps: ['温度：用冷水洗脸或含冰块，激活身体的潜水反射', '强烈运动：做30秒到1分钟的剧烈运动，释放紧张', '调整呼吸：深呼吸，让呼气比吸气长', '渐进式肌肉放松：从头到脚依次紧张再放松各个肌肉群'] },
          medium: { skill: '接地技术', intro: '接地技术可以帮助你从恐惧中回到当下，感受安全。', steps: ['用5-4-3-2-1法：说出5样你看到的东西', '说出4样你能触摸到的东西', '说出3样你听到的声音', '说出2样你闻到的气味', '说出1样你尝到的味道'] },
          low: { skill: '检查事实', intro: '检查事实可以帮助你理性地看待恐惧，减少不必要的担心。', steps: ['写下让你害怕的事情', '问自己：这个担心有多少是基于事实的？', '寻找证据：支持和反对这个担心的证据', '重新评估：这件事真的有那么可怕吗？', '制定应对计划：如果真的发生了，我可以怎么做？'] }
        },
        'joy': {
          high: { skill: '感恩练习', intro: '感恩练习可以帮助你珍惜和延长这份快乐。', steps: ['写下3件让你感到快乐或感恩的事情', '详细描述为什么这些事情让你感到快乐', '回想这些美好时刻的细节', '对自己说：我值得拥有这份快乐'] },
          medium: { skill: '积极情绪清单', intro: '积极情绪清单可以帮助你识别和培养更多的快乐。', steps: ['列出让你感到快乐的活动', '计划在未来一周做其中的几件事', '做的时候全身心投入', '记录下这些体验带来的感受'] },
          low: { skill: '正念呼吸', intro: '正念呼吸可以帮助你保持平静和专注。', steps: ['找一个舒适的姿势坐下或躺下', '把注意力放在呼吸上，感受空气进出鼻腔', '当思绪飘走时，温柔地把注意力带回呼吸', '持续3-5分钟，慢慢延长时间'] }
        },
        'calm': {
          high: { skill: '正念呼吸', intro: '正念呼吸可以帮助你保持这份平静。', steps: ['找一个舒适的姿势坐下或躺下', '把注意力放在呼吸上，感受空气进出鼻腔', '当思绪飘走时，温柔地把注意力带回呼吸', '持续3-5分钟，慢慢延长时间'] },
          medium: { skill: '一心一意', intro: '一心一意可以帮助你专注于当下，提升生活质量。', steps: ['选择一个日常活动，比如吃饭或走路', '全身心投入这个活动，不做其他事情', '注意这个活动的每一个细节', '当思绪飘走时，温柔地把注意力带回来'] },
          low: { skill: '感恩练习', intro: '感恩练习可以帮助你培养积极的心态。', steps: ['写下3件让你感到感恩的事情', '详细描述为什么这些事情让你感恩', '回想这些美好时刻的细节', '对自己说：我很幸运拥有这些'] }
        }
      }

      // 根据强度确定级别
      let intensityLevel = 'low'
      if (intensity >= 7) {
        intensityLevel = 'high'
      } else if (intensity >= 4) {
        intensityLevel = 'medium'
      }

      // 获取推荐的技能
      const recommendedSkill = skillRecommendations[emotionType]?.[intensityLevel] || skillRecommendations['calm']['medium']

      // 生成温暖且自然的引导消息
      let guidanceMessage = ''

      if (intensity >= 7) {
        guidanceMessage = `我能感受到你现在的情绪比较强烈。别担心，我会陪着你。让我们一起尝试一个DBT技能来帮助你调节情绪。`
      } else if (intensity >= 4) {
        guidanceMessage = `我理解你现在的感受。让我来帮你找一个合适的方法来应对这个情绪。`
      } else {
        guidanceMessage = `很好，你的情绪状态还不错。我们可以学习一个技能来保持或提升这种状态。`
      }

      // 延迟一下，让用户有时间消化情绪分析结果
      await new Promise(resolve => setTimeout(resolve, 1500))

      // 发送引导消息
      this.$emit('add-message', {
        role: 'assistant',
        content: guidanceMessage
      })

      // 再延迟一下
      await new Promise(resolve => setTimeout(resolve, 1000))

      // 介绍技能
      this.$emit('add-message', {
        role: 'assistant',
        content: `根据你的情况，我推荐你尝试${recommendedSkill.skill}。${recommendedSkill.intro}`
      })

      // 再延迟一下
      await new Promise(resolve => setTimeout(resolve, 1500))

      // 逐步引导
      this.$emit('add-message', {
        role: 'assistant',
        content: `让我来一步步引导你。准备好了吗？`
      })

      // 再延迟一下
      await new Promise(resolve => setTimeout(resolve, 1500))

      // 发送第一步
      this.$emit('add-message', {
        role: 'assistant',
        content: `第一步：${recommendedSkill.steps[0]}`
      })

      // 标记评估已完成
      this.assessmentCompleted = true

      // 再延迟一下，然后折叠情绪结果卡片
      await new Promise(resolve => setTimeout(resolve, 2000))

      // 折叠情绪结果，允许继续对话
      this.emotionResult = null

      // 发送继续引导的提示
      await new Promise(resolve => setTimeout(resolve, 1000))
      this.$emit('add-message', {
        role: 'assistant',
        content: `试试看，完成后告诉我，我会继续引导你下一步。`
      })
    },

    getEmotionDescription(emotionType) {
      const descMap = {
        'anxiety': '这是一种很常见的情绪反应，让我们一起来处理它。',
        'sadness': '允许自己感受这份情绪是很重要的。',
        'joy': '保持这份积极的状态。',
        'anger': '让我们一起找到合适的方式来表达这份情绪。',
        'fear': '这是人类的正常保护机制，我们可以一起面对。',
        'neutral': '你现在的情绪比较平静。'
      }
      return descMap[emotionType] || '我理解你现在的感受。'
    },

    scrollToBottom() {
      const chatTab = this.$refs.chatTab
      if (chatTab) {
        chatTab.scrollTop = chatTab.scrollHeight
      }
    },

    handleCloseCrisisModal() {
      this.showCrisisModal = false
    },

    handleCallHotline() {
      console.log('用户拨打了危机热线')
    },

    async handleSkillConfirmation(data) {
      console.log('用户技能确认选择:', data)
      this.showSkillConfirmation = false

      try {
        const response = await sendChatMessage({
          session_id: this.sessionId,
          message: data.choice === '愿意' ? '我愿意尝试这个技能' : '我再想想',
          message_type: 'skill_confirmation',
          metadata: { choice: data.choice }
        })

        if (response.reply) {
          this.$emit('add-message', {
            role: 'assistant',
            content: response.reply
          })
        }

        if (response.requires_input) {
          this.handleRequiresInput(response.requires_input)
        }
      } catch (error) {
        console.error('发送技能确认失败:', error)
        this.$emit('add-message', {
          role: 'assistant',
          content: '好的，我们继续。'
        })
      }
    },

    async handleStepComplete() {
      console.log('用户完成步骤')
      this.showStepGuidance = false

      try {
        const response = await sendChatMessage({
          session_id: this.sessionId,
          message: '我已完成当前步骤',
          message_type: 'step_completion',
          metadata: {}
        })

        if (response.reply) {
          this.$emit('add-message', {
            role: 'assistant',
            content: response.reply
          })
        }

        if (response.requires_input) {
          this.handleRequiresInput(response.requires_input)
        }
      } catch (error) {
        console.error('发送步骤完成失败:', error)
        this.$emit('add-message', {
          role: 'assistant',
          content: '很好，让我们继续。'
        })
      }
    },

// 处理后端要求的输入
    handleRequiresInput(requiresInput) {
      console.log('后端要求输入:', requiresInput)

      if (requiresInput.type === 'emotion_images') {
        this.showImageSelector = true
      } else if (requiresInput.type === 'body_selector') {
        this.showBodySelector = true
      } else if (requiresInput.type === 'intensity_slider') {
        this.showIntensitySlider = true
      } else if (requiresInput.type === 'skill_confirmation') {
        this.showSkillConfirmation = true
        this.skillConfirmationData = {
          skillName: requiresInput.skill_name || requiresInput.skillName || '',
          introduction: requiresInput.introduction || '',
          options: requiresInput.options || ['愿意', '再想想']
        }
      } else if (requiresInput.type === 'step_completion') {
        this.showStepGuidance = true
        this.stepGuidanceData = {
          stepNumber: requiresInput.step_number || 1,
          totalSteps: requiresInput.total_steps || 1,
          content: requiresInput.content || requiresInput.prompt || '',
          isLastStep: requiresInput.is_last_step || false
        }
      }
    },

    async sendChatMessageWithState(message, messageType, metadata = {}) {
      try {
        const response = await sendChatMessage({
          session_id: this.sessionId,
          message: message,
          message_type: messageType,
          metadata: metadata
        })

        if (response.reply) {
          this.$emit('add-message', {
            role: 'assistant',
            content: response.reply
          })
        }

        if (response.requires_input) {
          this.handleRequiresInput(response.requires_input)
        }

        return response
      } catch (error) {
        console.error('发送消息失败:', error)
        this.$emit('add-message', {
          role: 'assistant',
          content: '我了解了，让我们继续。'
        })
        throw error
      }
    },
  },
  mounted() {
    // 组件挂载后滚动到底部
    this.scrollToBottom()
  }
}
</script>

<style scoped>
.chat-tab {
  height: 100%;
  overflow-y: auto;
  background: transparent;
  scroll-behavior: smooth;
}

/* ========== 对话容器 ========== */
.chat-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 48px 24px 120px;
}

/* ========== 缩小选择器尺寸 ========== */
.chat-container :deep(.emotion-selector) {
  max-width: 500px;
  margin: 20px auto;
  padding: 16px;
  transform: scale(0.85);
  transform-origin: top center;
}

.chat-container :deep(.emotion-selector .image-grid) {
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.chat-container :deep(.emotion-selector .image-item) {
  aspect-ratio: 3/2;
}

.chat-container :deep(.body-selector) {
  max-width: 400px;
  margin: 20px auto;
  padding: 16px;
  transform: scale(0.75);
  transform-origin: top center;
}

.chat-container :deep(.body-selector .body-svg) {
  max-width: 200px;
}

/* ========== 身体不适询问 ========== */
.discomfort-question {
  margin: 20px auto;
  padding: 20px;
  animation: fadeIn 0.5s ease;
}

.question-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
}

.question-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12px;
}

.question-subtitle {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 28px;
  line-height: 1.6;
}

.question-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.question-btn {
  flex: 1;
  max-width: 180px;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.yes-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.yes-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.no-btn {
  background: #f0f0f0;
  color: #666;
}

.no-btn:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

/* ========== 欢迎消息 ========== */
.welcome-section {
  text-align: center;
  padding: 80px 20px;
  animation: fadeIn 0.8s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.welcome-icon {
  font-size: 80px;
  margin-bottom: 24px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  color: #2E7D32;
  margin-bottom: 16px;
}

.welcome-text {
  font-size: 18px;
  line-height: 1.8;
  color: #666;
}

/* ========== 消息样式 ========== */
.message-item {
  font-size: 17px;
  line-height: 1.8;
  margin-bottom: 24px;
  padding: 8px 0;
  animation: fadeInMessage 0.5s ease;
}

@keyframes fadeInMessage {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* AI消息 - 靠左,深蓝色 */
.message-ai {
  color: #0D47A1;
  font-weight: 500;
  text-align: left;
  margin-left: 20px;
  margin-right: 100px;
}

/* 用户消息 - 靠右,深紫色 */
.message-user {
  color: #6A1B9A;
  font-weight: 500;
  text-align: right;
  margin-left: 100px;
  margin-right: 20px;
}

.timestamp {
  color: #81C784;
  font-size: 12px;
  font-weight: 400;
  margin-top: 6px;
  display: block;
  opacity: 0.8;
}

/* ========== 操作按钮 ========== */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin: 32px 20px;
}

.action-btn {
  padding: 14px 32px;
  border: none;
  border-radius: 24px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(76, 175, 80, 0.5);
}

/* ========== 情绪分析结果卡片 ========== */
.result-card {
  margin: 24px 20px;
  padding: 24px;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.8),
    rgba(255, 255, 255, 0.6)
  );
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 2px solid rgba(102, 187, 106, 0.3);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(46, 125, 50, 0.2);
  animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.result-icon {
  font-size: 48px;
}

.result-info {
  flex: 1;
}

.result-title {
  font-size: 22px;
  font-weight: 700;
  color: #2E7D32;
  margin-bottom: 4px;
}

.result-confidence {
  font-size: 14px;
  color: #66BB6A;
}

.result-desc {
  font-size: 15px;
  line-height: 1.6;
  color: #555;
}

/* ========== 滑块 ========== */
.intensity-slider {
  margin: 24px 20px;
}

/* 滚动条样式 */
.chat-tab::-webkit-scrollbar {
  width: 6px;
}

.chat-tab::-webkit-scrollbar-track {
  background: transparent;
}

.chat-tab::-webkit-scrollbar-thumb {
  background: rgba(76, 175, 80, 0.3);
  border-radius: 3px;
}

.chat-tab::-webkit-scrollbar-thumb:hover {
  background: rgba(76, 175, 80, 0.5);
}
</style>
