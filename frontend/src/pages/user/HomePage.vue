<template>
  <div class="home-container">
    <!-- 顶部Tab导航 -->
    <nav class="tab-navigation">
      <div
        class="tab-item"
        :class="{ active: currentTab === 'chat' }"
        @click="switchTab('chat')"
      >
        💬 对话
      </div>
      <div
        class="tab-item"
        :class="{ active: currentTab === 'diary' }"
        @click="switchTab('diary')"
      >
        📖 日记
      </div>
      <div
        class="tab-item"
        :class="{ active: currentTab === 'profile' }"
        @click="switchTab('profile')"
      >
        🌱 我
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="main-content">
      <ChatTab
        ref="chatTab"
        v-show="currentTab === 'chat'"
        :class="{ active: currentTab === 'chat' }"
        :messages="messages"
        :session-id="sessionId"
        @add-message="handleAddMessage"
      />
      <DiaryTab
        v-show="currentTab === 'diary'"
        :class="{ active: currentTab === 'diary' }"
      />
      <ProfileTab
        v-show="currentTab === 'profile'"
        :class="{ active: currentTab === 'profile' }"
      />
    </main>

    <!-- 底部输入框(仅对话页显示) -->
    <div v-show="currentTab === 'chat'" class="chat-input-container">
      <div class="chat-input-wrapper">
        <input
          v-model="inputMessage"
          type="text"
          class="chat-input"
          placeholder="输入你的想法..."
          @keyup.enter="sendMessage"
        />
        <div class="send-button" @click="sendMessage">➤</div>
      </div>
    </div>
  </div>
</template>

<script>
import ChatTab from './ChatTab.vue'
import DiaryTab from './DiaryTab.vue'
import ProfileTab from './ProfileTab.vue'
import { sendChatMessage } from '@/api/emotion'

export default {
  name: 'HomePage',
  components: {
    ChatTab,
    DiaryTab,
    ProfileTab
  },
  data() {
    return {
      currentTab: 'chat',  // 默认显示对话tab
      inputMessage: '',
      messages: [],  // 消息列表
      messageIdCounter: 0,  // 消息ID计数器
      sessionId: null,  // 会话ID
      isAITyping: false  // AI是否正在输入
    }
  },
  methods: {
    switchTab(tab) {
      this.currentTab = tab
    },

    async sendMessage() {
      if (!this.inputMessage.trim() || this.isAITyping) return

      const userMessage = this.inputMessage.trim()

      // 添加用户消息
      this.addMessage({
        role: 'user',
        content: userMessage
      })

      // 清空输入框
      this.inputMessage = ''

      // 调用后端AI聊天API
      this.isAITyping = true

      try {
        const response = await sendChatMessage({
          message: userMessage,
          message_type: 'text',
          session_id: this.sessionId
        })

        console.log('✅ AI回复:', response)

        // 保存会话ID
        if (response.session_id) {
          this.sessionId = response.session_id
        }

        // 添加AI回复
        this.addMessage({
          role: 'assistant',
          content: response.reply
        })

        // 处理后端要求的输入（如情绪评估）
        if (response.requires_input) {
          this.$refs.chatTab.handleRequiresInput(response.requires_input)
        }

      } catch (error) {
        console.error('❌ AI对话失败:', error)

        // 发送错误提示
        this.addMessage({
          role: 'assistant',
          content: '抱歉，我现在遇到了一些问题。请稍后再试，或者你可以继续跟我说说你的感受。'
        })
      } finally {
        this.isAITyping = false
      }
    },

    handleAddMessage(messageData) {
      // 处理来自ChatTab的消息（如情绪分析结果）
      this.addMessage(messageData)
    },

    addMessage(messageData) {
      const newMessage = {
        id: ++this.messageIdCounter,
        role: messageData.role,
        content: messageData.content,
        time: this.getCurrentTime()
      }
      this.messages.push(newMessage)
    },

    getCurrentTime() {
      const now = new Date()
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      return `${hours}:${minutes}`
    }
  }
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: transparent;
}

/* ========== 顶部导航 ========== */
.tab-navigation {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border-bottom: 2px solid rgba(129, 199, 132, 0.2);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 48px;
  z-index: 1000;
}

.tab-item {
  position: relative;
  padding: 10px 20px;
  font-size: 16px;
  color: #66BB6A;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.tab-item:hover {
  color: #43A047;
  transform: translateY(-2px);
}

.tab-item.active {
  color: #2E7D32;
  font-weight: 600;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 70%;
  height: 4px;
  background: linear-gradient(90deg,
    rgba(46, 125, 50, 0),
    rgba(46, 125, 50, 1),
    rgba(46, 125, 50, 0)
  );
  border-radius: 2px;
  box-shadow: 0 2px 12px rgba(46, 125, 50, 0.6);
  animation: tabIndicator 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes tabIndicator {
  from {
    width: 0%;
    opacity: 0;
  }
  to {
    width: 70%;
    opacity: 1;
  }
}

/* ========== 主内容区 ========== */
.main-content {
  padding-top: 64px;
  padding-bottom: 0;
  min-height: 100vh;
  position: relative;
}

.main-content > * {
  animation: contentFadeIn 0.6s ease;
}

@keyframes contentFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== 底部输入栏 ========== */
.chat-input-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: linear-gradient(180deg,
    rgba(255, 255, 255, 0.7),
    rgba(255, 255, 255, 0.85)
  );
  backdrop-filter: blur(35px) saturate(180%);
  -webkit-backdrop-filter: blur(35px) saturate(180%);
  border-top: 2px solid rgba(129, 199, 132, 0.3);
  box-shadow: 0 -12px 40px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 1);
  z-index: 100;
}

.chat-input-wrapper {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  gap: 16px;
  align-items: center;
}

.chat-input {
  flex: 1;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 2px solid rgba(102, 187, 106, 0.3);
  border-radius: 28px;
  padding: 14px 24px;
  font-size: 15px;
  color: #1B5E20;
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15), inset 0 2px 0 rgba(255, 255, 255, 1);
  transition: all 0.3s ease;
  outline: none;
}

.chat-input::placeholder {
  color: #81C784;
}

.chat-input:focus {
  border-color: rgba(76, 175, 80, 0.6);
  box-shadow: 0 6px 24px rgba(76, 175, 80, 0.25), 0 0 0 4px rgba(129, 199, 132, 0.1), inset 0 2px 0 rgba(255, 255, 255, 1);
}

.send-button {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg,
    rgba(102, 187, 106, 1),
    rgba(129, 199, 132, 1)
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.5), inset 0 2px 0 rgba(255, 255, 255, 0.7);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: white;
  font-size: 24px;
}

.send-button:hover {
  transform: scale(1.1) rotate(15deg);
  box-shadow: 0 8px 28px rgba(76, 175, 80, 0.6), inset 0 2px 0 rgba(255, 255, 255, 0.8);
}

.send-button:active {
  transform: scale(0.95);
}
</style>
