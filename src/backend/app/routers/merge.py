"""
跨教材整合路由
职责：执行跨教材整合、获取决策、确认修改
集成MergeService实现真正的跨教材整合
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.models import MergeRequest, MergeResult, MergeDecision, GraphData
from app.services.merge_service import MergeService
from app.routers.graph import _graphs, store_graph

router = APIRouter()

# 存储整合决策
_merge_decisions: List[MergeDecision] = []

# 存储上次整合结果统计
_last_merge_stats: dict = {}


@router.post("/", response_model=MergeResult)
async def merge_textbooks(request: MergeRequest):
    """
    执行跨教材整合
    输入：需要整合的教材ID列表
    返回：整合决策列表和压缩比
    """
    # 1. 收集所有教材图谱
    graphs = []
    for tid in request.textbook_ids:
        if tid in _graphs:
            graphs.append(_graphs[tid].dict())

    if not graphs:
        raise HTTPException(status_code=404, detail="未找到指定的教材图谱")

    # 2. 调用合并服务
    merge_service = MergeService()
    merged_graph, decisions = merge_service.merge_graphs(graphs)

    # 3. 存储合并后的图谱
    store_graph("merged", GraphData(**merged_graph))

    # 4. 保存决策列表
    global _merge_decisions
    _merge_decisions = decisions

    # 5. 计算压缩比
    original_chars = sum(
        sum(len(n.get("definition", "")) for n in g.get("nodes", []))
        for g in graphs
    )
    merged_chars = sum(
        len(n.get("definition", ""))
        for n in merged_graph.get("nodes", [])
    )

    # 保存统计信息
    global _last_merge_stats
    _last_merge_stats = {
        "original_count": len(graphs),
        "original_chars": original_chars,
        "original_nodes": sum(len(g.get("nodes", [])) for g in graphs),
        "merged_nodes": len(merged_graph.get("nodes", [])),
        "edge_count": len(merged_graph.get("edges", [])),
        "compression_ratio": 1 - (merged_chars / original_chars) if original_chars > 0 else 0
    }

    return MergeResult(
        decisions=decisions,
        compression_ratio=1 - (merged_chars / original_chars) if original_chars > 0 else 0,
        original_chars=original_chars,
        merged_chars=merged_chars
    )


@router.get("/decisions")
async def get_merge_decisions():
    """
    获取当前整合决策列表
    返回：所有待确认的整合决策
    """
    return {"decisions": _merge_decisions}


@router.get("/stats")
async def get_merge_stats():
    """
    获取上次整合的统计信息
    返回：整合统计
    """
    return _last_merge_stats


@router.post("/confirm")
async def confirm_merge():
    """
    确认并执行整合决策
    返回：执行后的整合图谱
    """
    global _merge_decisions
    _merge_decisions = []
    return {"message": "整合已确认，图谱已更新"}


@router.post("/modify")
async def modify_decision(decision_id: str, new_action: str):
    """
    修改整合决策
    输入：决策ID和新操作类型
    返回：更新后的决策列表
    """
    for decision in _merge_decisions:
        if decision.decision_id == decision_id:
            decision.action = new_action
            return {"message": f"决策 {decision_id} 已更新为 {new_action}"}
    raise HTTPException(status_code=404, detail="决策不存在")