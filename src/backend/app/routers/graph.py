"""
知识图谱路由
职责：获取教材图谱、节点详情、整合图谱
"""
from fastapi import APIRouter, HTTPException
from app.models import GraphData, KnowledgeNode, KnowledgeEdge

router = APIRouter()

# 模拟图谱数据存储
_graphs: dict = {}


@router.get("/{textbook_id}")
async def get_textbook_graph(textbook_id: str):
    """
    获取单本教材知识图谱
    返回：该教材的节点和边列表
    """
    # 如果没有数据，返回空图谱
    if textbook_id not in _graphs:
        return GraphData(nodes=[], edges=[])
    return _graphs[textbook_id]


@router.get("/merged")
async def get_merged_graph():
    """
    获取跨教材整合后的知识图谱
    返回：所有教材整合后的图谱数据
    """
    return GraphData(nodes=[], edges=[])


@router.get("/node/{node_id}")
async def get_node_detail(node_id: str):
    """
    获取知识点详情
    返回：节点的完整信息
    """
    # 遍历所有图谱查找节点
    for graph_data in _graphs.values():
        for node in graph_data.nodes:
            if node.id == node_id:
                return node
    raise HTTPException(status_code=404, detail="知识点不存在")


def store_graph(textbook_id: str, graph: GraphData):
    """保存图谱数据（供其他模块调用）"""
    _graphs[textbook_id] = graph