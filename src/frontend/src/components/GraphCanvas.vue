<template>
  <div class="graph-canvas" ref="container">
    <div v-if="!hasData" class="empty-graph">
      请选择教材查看知识图谱
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import G6 from '@antv/g6'

export default {
  name: 'GraphCanvas',
  props: {
    graphData: { type: Object, default: () => ({ nodes: [], edges: [] }) }
  },
  emits: ['nodeClick'],
  setup(props, { emit }) {
    const container = ref(null)
    let graph = null

    const hasData = ref(false)

    // 初始化图谱
    const initGraph = () => {
      if (!container.value) return

      graph = new G6.Graph({
        container: container.value,
        width: container.value.clientWidth,
        height: container.value.clientHeight,
        // 配置布局
        layout: {
          type: 'force',
          preventOverlap: true,
          nodeSize: 30
        },
        // 节点配置
        defaultNode: {
          size: 30,
          style: {
            fill: '#1890ff',
            stroke: '#40a9ff',
            cursor: 'pointer'
          },
          labelCfg: {
            style: { fill: '#333', fontSize: 12 }
          }
        },
        // 边配置
        defaultEdge: {
          style: {
            stroke: '#e0e0e0',
            lineWidth: 1
          }
        },
        // 交互行为
        modes: {
          default: ['drag-canvas', 'zoom-canvas', 'drag-node']
        }
      })

      // 节点点击事件
      graph.on('node:click', (e) => {
        const node = e.item.getModel()
        emit('nodeClick', node)
      })
    }

    // 更新图谱数据
    const updateGraph = () => {
      if (!graph) return

      const { nodes, edges } = props.graphData
      hasData.value = nodes.length > 0

      // 映射边数据
      const edgeData = edges.map(e => ({
        source: e.source,
        target: e.target,
        label: e.relation_type
      }))

      graph.data({ nodes, edges: edgeData })
      graph.render()

      // 根据教材数量设置节点颜色
      const countMap = {}
      nodes.forEach(n => {
        countMap[n.source] = (countMap[n.source] || 0) + 1
      })

      const colors = ['#1890ff', '#52c41a', '#fa8c16', '#f5222d', '#722ed1', '#13c2c2']
      let colorIndex = 0
      nodes.forEach(n => {
        graph.updateItem(n.id, {
          style: {
            fill: colors[colorIndex % colors.length]
          }
        })
        colorIndex++
      })
    }

    // 监听数据变化
    watch(() => props.graphData, updateGraph, { deep: true })

    // 窗口大小变化
    const handleResize = () => {
      if (graph && container.value) {
        graph.changeSize(container.value.clientWidth, container.value.clientHeight)
      }
    }

    onMounted(() => {
      initGraph()
      updateGraph()
      window.addEventListener('resize', handleResize)
    })

    onUnmounted(() => {
      if (graph) graph.destroy()
      window.removeEventListener('resize', handleResize)
    })

    return { container, hasData }
  }
}
</script>

<style scoped>
.graph-canvas {
  width: 100%;
  height: 100%;
  position: relative;
}

.empty-graph {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  font-size: 16px;
}
</style>