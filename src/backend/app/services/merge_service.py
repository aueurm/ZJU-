"""
跨教材整合服务
职责：计算知识点相似度、生成整合决策
"""
import numpy as np
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from app.models import MergeDecision, KnowledgeNode


class MergeService:
    """整合服务"""

    def __init__(self):
        # 初始化Embedding模型用于相似度计算
        self.embedding_model = SentenceTransformer('BAAI/bge-small-zh-v1.5')

        # 相似度阈值配置
        self.HIGH_THRESHOLD = 0.85   # 高置信度，直接合并
        self.MID_THRESHOLD = 0.70     # 中置信度，需要LLM二次判断
        self.LOW_THRESHOLD = 0.50     # 低置信度，保留各自版本

    def compute_similarity(self, node1: KnowledgeNode, node2: KnowledgeNode) -> float:
        """
        计算两个知识点的语义相似度
        输入：两个知识点节点
        返回：相似度分数（0-1）
        """
        # 将知识点名称和定义拼接
        text1 = f"{node1.name} {node1.definition}"
        text2 = f"{node2.name} {node2.definition}"

        # 生成向量
        emb1 = self.embedding_model.encode(text1)
        emb2 = self.embedding_model.encode(text2)

        # 计算余弦相似度
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(similarity)

    def merge_graphs(self, graphs: List[dict]) -> Tuple[List[dict], MergeDecision]:
        """
        合并多个教材图谱
        输入：多个图谱数据列表
        返回：(合并后图谱, 整合决策列表)
        """
        decisions = []
        all_nodes = []
        all_edges = []

        # 收集所有节点
        for graph in graphs:
            all_nodes.extend(graph.get("nodes", []))

        # 构建节点映射（新ID -> 合并后节点）
        node_mapping = {}

        # 计算相似度矩阵
        for i in range(len(all_nodes)):
            for j in range(i + 1, len(all_nodes)):
                similarity = self.compute_similarity(all_nodes[i], all_nodes[j])

                if similarity >= self.HIGH_THRESHOLD:
                    # 高置信度，直接合并
                    decision = self._create_merge_decision(
                        [all_nodes[i], all_nodes[j]],
                        similarity
                    )
                    decisions.append(decision)

                    # 更新映射
                    merged_id = decision.result_node
                    node_mapping[all_nodes[i]["id"]] = merged_id
                    node_mapping[all_nodes[j]["id"]] = merged_id

                elif similarity >= self.MID_THRESHOLD:
                    # 中置信度，标记为待LLM判断
                    decisions.append(MergeDecision(
                        decision_id=f"merge_{len(decisions)+1:03d}",
                        action="pending_llm",
                        affected_nodes=[all_nodes[i]["id"], all_nodes[j]["id"]],
                        reason="中置信度，需LLM二次判断",
                        confidence=similarity
                    ))

        # 构建合并后的图谱
        merged_nodes = self._build_merged_nodes(all_nodes, node_mapping)
        merged_edges = self._build_merged_edges(
            [e for g in graphs for e in g.get("edges", [])],
            node_mapping
        )

        return {"nodes": merged_nodes, "edges": merged_edges}, decisions

    def _create_merge_decision(self, nodes: List[KnowledgeNode], confidence: float) -> MergeDecision:
        """创建合并决策"""
        # 选择描述最完整的节点作为主版本
        best_node = max(nodes, key=lambda n: len(n.definition))

        return MergeDecision(
            decision_id=f"merge_{np.random.randint(1000):03d}",
            action="merge",
            affected_nodes=[n["id"] for n in nodes],
            result_node=f"merged_{best_node['id']}",
            reason=f"三本教材都讲解了'{best_node.name}'的概念，保留该版本因其描述最系统完整",
            confidence=confidence
        )

    def _build_merged_nodes(self, all_nodes: List[dict], node_mapping: dict) -> List[dict]:
        """构建合并后的节点列表"""
        merged = []
        seen = set()

        for node in all_nodes:
            new_id = node_mapping.get(node["id"], node["id"])

            if new_id not in seen:
                merged.append({
                    **node,
                    "id": new_id,
                    "freq": len([n for n in all_nodes if node_mapping.get(n["id"]) == new_id])
                })
                seen.add(new_id)
            else:
                # 累加频次
                for m in merged:
                    if m["id"] == new_id:
                        m["freq"] = m.get("freq", 1) + 1
                        break

        return merged

    def _build_merged_edges(self, all_edges: List[dict], node_mapping: dict) -> List[dict]:
        """构建合并后的边列表"""
        merged = []
        seen_edges = set()

        for edge in all_edges:
            # 映射节点ID
            new_source = node_mapping.get(edge["source"], edge["source"])
            new_target = node_mapping.get(edge["target"], edge["target"])

            edge_key = (new_source, new_target)
            if edge_key not in seen_edges:
                merged.append({
                    **edge,
                    "source": new_source,
                    "target": new_target
                })
                seen_edges.add(edge_key)

        return merged