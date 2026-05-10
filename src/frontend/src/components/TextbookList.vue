<template>
  <div class="textbook-list">
    <h3>已上传教材</h3>
    <div v-if="textbooks.length === 0" class="empty">
      暂无教材，请上传
    </div>
    <div
      v-for="book in textbooks"
      :key="book.textbook_id"
      class="textbook-item"
      :class="{ selected: book.textbook_id === selectedId }"
      @click="$emit('select', book.textbook_id)"
    >
      <div class="book-icon">📚</div>
      <div class="book-info">
        <div class="book-name">{{ book.filename }}</div>
        <div class="book-status">
          <span :class="['status', book.status]">{{ getStatusText(book.status) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TextbookList',
  props: {
    textbooks: { type: Array, default: () => [] },
    selectedId: { type: String, default: null }
  },
  emits: ['select'],
  setup() {
    const getStatusText = (status) => {
      const map = { parsing: '解析中', parsed: '已完成', failed: '失败' }
      return map[status] || status
    }
    return { getStatusText }
  }
}
</script>

<style scoped>
.textbook-list { padding: 16px; }
.textbook-list h3 { font-size: 14px; color: #666; margin-bottom: 12px; }
.empty { color: #999; font-size: 13px; text-align: center; padding: 20px 0; }

.textbook-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border: 1px solid #eee;
  border-radius: 6px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.textbook-item:hover { background: #f5f5f5; }
.textbook-item.selected {
  border-color: #1890ff;
  background: #f0f7ff;
}

.book-icon { font-size: 24px; margin-right: 12px; }
.book-name { font-size: 14px; color: #333; }
.book-status { margin-top: 4px; }
.status {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 3px;
}
.status.parsing { background: #fff7e6; color: #fa8c16; }
.status.parsed { background: #f6ffed; color: #52c41a; }
.status.failed { background: #fff2f0; color: #ff4d4f; }
</style>