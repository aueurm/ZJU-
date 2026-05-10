"""
跨教材整合路由
职责：执行跨教材整合、获取决策、确认修改
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models import MergeRequest, MergeResult, MergeDecision

router = APIRouter()

# 模拟存储整合决策
_merge_decisions: List[MergeDecision] = []


@router.post("/")
async def merge_textbooks(request: MergeRequest):
    """
    执行跨教材整合
    输入：需要整合的教材ID列表
    返回：整合决策列表和压缩比
    """
    # TODO: 调用整合服务执行实际整合逻辑
    return MergeResult(
        decisions=_merge_decisions,
        compression_ratio=0.0,
        original_chars=0,
        merged_chars=0
    )


@router.get("/decisions")
async def get_merge_decisions():
    """
    获取当前整合决策列表
    返回：所有待确认的整合决策
    """
    return {"decisions": _merge_decisions}


@router.post("/confirm")
async def confirm_merge():
    """
    确认并执行整合决策
    返回：执行后的整合图谱
    """
    global _merge_decisions
    _merge_decisions = []  # 清空已确认的决策
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