<template>
  <div class="chat-panel">
    <h4>对话交互</h4>

    <div class="chat-container">
      <div v-if="messages.length === 0" class="empty-hint">
        询问关于整合决策的问题，或要求修改整合方案
      </div>
      <div
        v-for="(msg, i) in messages"
        :key="i"
        :class="['message', msg.role]"
      >
        <div class="role-icon">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
        <div class="content">{{ msg.content }}</div>
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="inputMessage"
        placeholder="输入问题..."
        @keydown.enter="sendMessage"
      />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { sendChat, getChatHistory } from '../api'

export default {
  name: 'ChatPanel',
  setup() {
    const inputMessage = ref('')
    const messages = ref([])
    const sessionId = 'default'

    const sendMessage = async () => {
      if (!inputMessage.value.trim()) return

      const msg = inputMessage.value.trim()
      messages.value.push({ role: 'user', content: msg })
      inputMessage.value = ''

      try {
        const res = await sendChat(msg, sessionId)
        const data = res.data
        messages.value.push({
          role: 'assistant',
          content: data.reply + (data.action_taken ? `\n[操作: ${data.action_taken}]` : '')
        })
      } catch (err) {
        messages.value.push({
          role: 'assistant',
          content: '抱歉，发送失败：' + err.message
        })
      }
    }

    const loadHistory = async () => {
      try {
        const res = await getChatHistory(sessionId)
        messages.value = res.data.messages || []
      } catch (err) {
        console.error('加载历史失败', err)
      }
    }

    onMounted(loadHistory)

    return { inputMessage, messages, sendMessage }
  }
}
</script>

<style scoped>
.chat-panel { display: flex; flex-direction: column; height: 100%; }
.chat-panel h4 { margin-bottom: 12px; }

.chat-container {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 12px;
}

.empty-hint {
  color: #999;
  font-size: 13px;
  text-align: center;
  padding: 40px 0;
}

.message { display: flex; margin-bottom: 12px; }
.message.user { flex-direction: row-reverse; }
.role-icon { font-size: 20px; margin: 0 8px; }
.content {
  max-width: 75%;
  padding: 8px 12px;
  border-radius: 8px;
  background: #f5f5f5;
  font-size: 14px;
  line-height: 1.5;
}
.message.assistant .content { background: #e6f7ff; }

.input-area { display: flex; gap: 8px; }
.input-area input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
}
.input-area button {
  padding: 8px 16px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>