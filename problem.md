# 项目问题检查报告

## 检查日期
2026/05/10

## 更新说明
- 确认 `GraphCanvas.vue` 节点着色问题已修复
- 确认 `chat.py` 已实现对话功能
- 确认 `extractor_service.py` 使用正确的 `chat_sync` 接口
- 确认 `MergePanel.vue` 函数命名正确
- 确认 `graph.py` /merged 端点已修复
- 确认 `rag.py` /index 端点已修复
- 问题范围缩小为1个前端数据展示问题

---

## 当前问题清单

### 问题1：ReportPanel.vue 统计数据依赖后端接口

**文件**：`src/frontend/src/components/ReportPanel.vue:81-116`

**现状**：前端统计数据依赖于 `getMergeStats()` 接口返回真实数据。如果后端 `_last_merge_stats` 未更新，则显示为空。

**说明**：该组件已正确调用后端接口（`getMergeStats()`, `getMergeDecisions()`, `getMergedGraph()`），问题取决于后端 merge.py 的 `/stats` 端点是否返回准确数据。merge.py 第60-68行已正确计算并保存统计信息。

**影响**：当前端调用时如后端无数据则显示为空，但这属于正常行为（无数据时不应显示假数据）。

---

## 已确认正常的功能

| 模块 | 文件 | 状态 |
|------|------|------|
| 教材上传管道 | `upload.py` | ✅ 完整 |
| 跨教材整合 | `merge.py` | ✅ 完整 |
| RAG问答 | `rag.py` (/query, /status, /index) | ✅ 完整 |
| 对话交互 | `chat.py` | ✅ 完整 |
| 知识提取 | `extractor_service.py` | ✅ 使用 `chat_sync` |
| LLM客户端 | `llm_client.py` | ✅ 接口完整 |
| 图谱存储共享 | `graph.py` | ✅ store_graph 正常 |
| 节点着色逻辑 | `GraphCanvas.vue` | ✅ sourceCount 被正确使用 |
| 函数命名 | `MergePanel.vue` | ✅ 正确 |
| 前端API | `api/index.js` | ✅ 所有端点匹配 |
| RAG索引构建 | `rag.py` /index | ✅ 已修复 |

---

## 问题汇总

| 优先级 | 问题 | 文件 | 影响 |
|--------|------|------|------|
| P1 | ReportPanel 统计依赖后端数据 | ReportPanel.vue | 无数据时显示为空 |

---

## 修复优先级

1. **P1 建议关注**：ReportPanel 统计数据显示依赖后端 merge.py 的 `/stats` 接口返回真实数据。当前代码逻辑正确，数据取决于整合操作是否执行。