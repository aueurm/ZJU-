<template>
  <div class="rag-panel">
    <h4>RAG精准问答</h4>

    <div class="status-bar">
      已索引 {{ status.indexed_textbooks }} 本教材，共 {{ status.total_chunks }} 个知识块
      <button @click="buildIndex" :disabled="status.status === 'indexing'">
        {{ status.status === 'indexing' ? '索引中...' : '重建索引' }}
      </button>
    </div>

    <div class="chat-container">
      <div
        v-for="(msg, i) in messages"
        :key="i"
        :class="['message', msg.role]"
      >
        <div class="role-icon">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
        <div class="content">
          <div class="text">{{ msg.content }}</div>
          <div v-if="msg.citations" class="citations">
            <div v-for="c in msg.citations" :key="c.page" class="citation">
              [{{ c.textbook }}, {{ c.chapter }}, 第{{ c.page }}页]
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="input-area">
      <textarea
        v-model="question"
        placeholder="输入问题，按Enter发送..."
        @keydown.enter.prevent="sendQuery"
        rows="3"
      ></textarea>
      <button @click="sendQuery" :disabled="!question.trim()">发送</button>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ragQuery, buildRagIndex, getRagStatus } from '../api'

export default {
  name: 'RAGPanel',
  setup() {
    const question = ref('')
    const messages = ref([])
    const status = reactive({ indexed_textbooks: 0, total_chunks: 0, status: 'ready' })

    const sendQuery = async () => {
      if (!question.value.trim()) return

      const q = question.value.trim()
      messages.value.push({ role: 'user', content: q })
      question.value = ''

      try {
        const res = await ragQuery(q)
        const data = res.data
        messages.value.push({
          role: 'assistant',
          content: data.answer,
          citations: data.citations
        })
      } catch (err) {
        messages.value.push({
          role: 'assistant',
          content: '抱歉，查询失败：' + err.message
        })
      }
    }

    const buildIndex = async () => {
      status.status = 'indexing'
      try {
        await buildRagIndex()
        loadStatus()
      } catch (err) {
        console.error('索引构建失败', err)
      }
      status.status = 'ready'
    }

    const loadStatus = async () => {
      try {
        const res = await getRagStatus()
        Object.assign(status, res.data)
      } catch (err) {
        console.error('获取状态失败', err)
      }
    }

    onMounted(loadStatus)

    return { question, messages, status, sendQuery, buildIndex }
  }
}
</script>

<style scoped>
.rag-panel { display: flex; flex-direction: column; height: 100%; }
.rag-panel h4 { margin-bottom: 12px; }

.status-bar {
  font-size: 12px;
  color: #666;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.status-bar button {
  font-size: 12px;
  padding: 4px 8px;
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 12px;
}

.message { display: flex; margin-bottom: 12px; }
.message.user { flex-direction: row-reverse; }
.role-icon { font-size: 20px; margin: 0 8px; }
.content { max-width: 80%; }
.text { padding: 8px 12px; border-radius: 8px; background: #f5f5f5; font-size: 14px; }
.message.assistant .text { background: #e6f7ff; }
.citations { margin-top: 6px; }
.citation {
  font-size: 11px;
  color: #1890ff;
  padding: 2px 0;
}

.input-area { display: flex; gap: 8px; }
.input-area textarea {
  flex: 1;
  padding: 8px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  resize: none;
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
.input-area button:disabled { background: #d9d9d9; }
</style>