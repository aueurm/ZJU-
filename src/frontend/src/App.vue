<template>
  <div class="app-container">
    <header class="app-header">
      <h1>学科知识整合智能体</h1>
    </header>

    <div class="app-main">
      <!-- 左侧：教材管理 -->
      <aside class="sidebar-left">
        <UploadZone @uploaded="onUploaded" />
        <TextbookList
          :textbooks="textbooks"
          :selectedId="selectedTextbook"
          @select="selectTextbook"
        />
      </aside>

      <!-- 中间：知识图谱 -->
      <main class="graph-area">
        <GraphCanvas
          :graphData="currentGraph"
          @nodeClick="onNodeClick"
        />
      </main>

      <!-- 右侧：功能面板 -->
      <aside class="sidebar-right">
        <div class="tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            :class="{ active: activeTab === tab.key }"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="panel-content">
          <MergePanel v-if="activeTab === 'merge'" />
          <RAGPanel v-if="activeTab === 'rag'" />
          <ChatPanel v-if="activeTab === 'chat'" />
          <ReportPanel v-if="activeTab === 'report'" />
        </div>
      </aside>
    </div>

    <!-- 节点详情弹窗 -->
    <NodeDetail
      v-if="selectedNode"
      :node="selectedNode"
      @close="selectedNode = null"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { getTextbookList, getGraph } from './api'

// 导入组件
import UploadZone from './components/UploadZone.vue'
import TextbookList from './components/TextbookList.vue'
import GraphCanvas from './components/GraphCanvas.vue'
import NodeDetail from './components/NodeDetail.vue'
import MergePanel from './components/MergePanel.vue'
import RAGPanel from './components/RAGPanel.vue'
import ChatPanel from './components/ChatPanel.vue'
import ReportPanel from './components/ReportPanel.vue'

export default {
  name: 'App',
  components: {
    UploadZone,
    TextbookList,
    GraphCanvas,
    NodeDetail,
    MergePanel,
    RAGPanel,
    ChatPanel,
    ReportPanel
  },
  setup() {
    // 状态
    const textbooks = ref([])
    const selectedTextbook = ref(null)
    const currentGraph = ref({ nodes: [], edges: [] })
    const selectedNode = ref(null)
    const activeTab = ref('merge')

    // Tab配置
    const tabs = [
      { key: 'merge', label: '整合操作' },
      { key: 'rag', label: 'RAG问答' },
      { key: 'chat', label: '对话交互' },
      { key: 'report', label: '整合报告' }
    ]

    // 加载教材列表
    const loadTextbooks = async () => {
      try {
        const res = await getTextbookList()
        textbooks.value = res.data.textbooks || []
      } catch (err) {
        console.error('加载教材失败', err)
      }
    }

    // 选择教材
    const selectTextbook = async (textbookId) => {
      selectedTextbook.value = textbookId
      try {
        const res = await getGraph(textbookId)
        currentGraph.value = res.data
      } catch (err) {
        console.error('加载图谱失败', err)
      }
    }

    // 上传成功回调
    const onUploaded = () => {
      loadTextbooks()
    }

    // 节点点击回调
    const onNodeClick = (node) => {
      selectedNode.value = node
    }

    // 初始化
    onMounted(() => {
      loadTextbooks()
    })

    return {
      textbooks,
      selectedTextbook,
      currentGraph,
      selectedNode,
      activeTab,
      tabs,
      loadTextbooks,
      selectTextbook,
      onUploaded,
      onNodeClick
    }
  }
}
</script>

<style>
/* 全局样式 */
* { margin: 0; padding: 0; box-sizing: border-box; }

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.app-header {
  padding: 16px 24px;
  background: #1890ff;
  color: white;
}

.app-header h1 { font-size: 20px; font-weight: 600; }

.app-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar-left {
  width: 280px;
  border-right: 1px solid #eee;
  overflow-y: auto;
}

.graph-area {
  flex: 1;
  background: #fafafa;
}

.sidebar-right {
  width: 360px;
  border-left: 1px solid #eee;
  display: flex;
  flex-direction: column;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
}

.tabs button {
  flex: 1;
  padding: 12px 8px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 14px;
  color: #666;
}

.tabs button.active {
  color: #1890ff;
  border-bottom: 2px solid #1890ff;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}
</style>