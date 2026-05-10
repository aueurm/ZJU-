<template>
  <div class="report-panel">
    <h4>整合报告</h4>

    <div class="stats">
      <div class="stat-item">
        <div class="label">原始教材</div>
        <div class="value">{{ stats.original_count }} 本</div>
      </div>
      <div class="stat-item">
        <div class="label">原始字数</div>
        <div class="value">{{ stats.original_chars | formatNumber }} 字</div>
      </div>
      <div class="stat-item">
        <div class="label">压缩比</div>
        <div class="value" :class="{ warning: stats.compression_ratio > 0.3 }">
          {{ (stats.compression_ratio * 100).toFixed(1) }}%
        </div>
      </div>
    </div>

    <div class="decisions-summary">
      <h5>决策摘要</h5>
      <div class="summary-grid">
        <div class="summary-item merge">合并: {{ decisionsSummary.merge }}</div>
        <div class="summary-item keep">保留: {{ decisionsSummary.keep }}</div>
        <div class="summary-item remove">删除: {{ decisionsSummary.remove }}</div>
      </div>
    </div>

    <div class="graph-stats">
      <h5>图谱统计</h5>
      <div>整合前节点: {{ stats.original_nodes }}</div>
      <div>整合后节点: {{ stats.merged_nodes }}</div>
      <div>关系边数: {{ stats.edge_count }}</div>
    </div>

    <button class="btn-export" @click="exportReport">导出报告</button>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'ReportPanel',
  setup() {
    const stats = ref({
      original_count: 7,
      original_chars: 1000000,
      compression_ratio: 0,
      original_nodes: 0,
      merged_nodes: 0,
      edge_count: 0
    })

    const decisionsSummary = ref({ merge: 0, keep: 0, remove: 0 })

    const exportReport = () => {
      // 生成Markdown报告
      const content = `# 整合报告\n\n## 整合概览\n\n| 指标 | 数值 |\n|------|------|\n| 原始教材 | ${stats.value.original_count}本 |\n| 原始字数 | ${stats.value.original_chars} |\n| 压缩比 | ${(stats.value.compression_ratio * 100).toFixed(1)}% |\n\n`
      const blob = new Blob([content], { type: 'text/markdown' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = '整合报告.md'
      a.click()
    }

    onMounted(() => {
      // 加载实际统计数据
    })

    return { stats, decisionsSummary, exportReport }
  }
}
</script>

<style scoped>
.report-panel h4 { margin-bottom: 16px; }

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.stat-item {
  text-align: center;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 6px;
}
.stat-item .label { font-size: 12px; color: #666; }
.stat-item .value { font-size: 18px; font-weight: 600; margin-top: 4px; }
.stat-item .value.warning { color: #ff4d4f; }

.decisions-summary { margin-bottom: 20px; }
.decisions-summary h5 { font-size: 14px; margin-bottom: 8px; }
.summary-grid { display: flex; gap: 8px; }
.summary-item {
  flex: 1;
  text-align: center;
  padding: 8px;
  border-radius: 4px;
  font-size: 13px;
}
.summary-item.merge { background: #f6ffed; color: #52c41a; }
.summary-item.keep { background: #e6f7ff; color: #1890ff; }
.summary-item.remove { background: #fff2f0; color: #ff4d4f; }

.graph-stats { margin-bottom: 20px; }
.graph-stats h5 { font-size: 14px; margin-bottom: 8px; }
.graph-stats div { font-size: 13px; color: #666; margin-bottom: 4px; }

.btn-export {
  width: 100%;
  padding: 10px;
  background: #52c41a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>