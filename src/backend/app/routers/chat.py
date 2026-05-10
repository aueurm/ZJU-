"""
对话交互路由
职责：处理用户对话、修改整合决策
"""
from fastapi import APIRouter
from typing import Dict, List
from app.models import ChatRequest, ChatResponse, ChatMessage

router = APIRouter()

# 模拟存储对话历史（按session_id分组）
_chat_histories: Dict[str, List[ChatMessage]] = {}


@router.post("/")
async def chat(request: ChatRequest):
    """
    发送对话消息
    输入：用户消息和会话ID
    返回：系统回复和执行的操作
    """
    session_id = request.session_id or "default"

    # 初始化会话历史
    if session_id not in _chat_histories:
        _chat_histories[session_id] = []

    # 添加用户消息
    _chat_histories[session_id].append(
        ChatMessage(role="user", content=request.message)
    )

    # TODO: 调用对话服务处理消息
    # 1. 解析用户意图
    # 2. 如需修改决策，调用整合服务
    # 3. 生成回复

    reply = "这是示例回复，实际需要调用对话服务生成"
    action_taken = None  # 如修改了整合决策，说明操作

    # 添加助手回复
    _chat_histories[session_id].append(
        ChatMessage(role="assistant", content=reply)
    )

    return ChatResponse(reply=reply, action_taken=action_taken)


@router.get("/history")
async def get_chat_history(session_id: str = "default"):
    """
    获取对话历史
    返回：该会话的所有消息列表
    """
    return {
        "session_id": session_id,
        "messages": _chat_histories.get(session_id, [])
    }