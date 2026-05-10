"""
RAG精准问答路由
职责：建立索引、问答查询、状态查询
"""
from fastapi import APIRouter
from app.models import RAGQuery, RAGResponse, RAGStatus, Citation

router = APIRouter()


@router.post("/index")
async def build_rag_index():
    """
    为已上传教材建立向量索引
    返回：索引构建状态
    """
    # TODO: 调用RAG服务构建向量索引
    return RAGStatus(
        indexed_textbooks=0,
        total_chunks=0,
        status="ready"
    )


@router.post("/query")
async def rag_query(query: RAGQuery):
    """
    RAG精准问答
    输入：用户问题
    返回：回答和引用来源
    """
    # TODO: 调用RAG服务进行问答
    # 1. 问题转Embedding
    # 2. 向量检索top-5相关chunks
    # 3. 构建Prompt调用LLM
    # 4. 返回带引用的回答

    return RAGResponse(
        answer="这是示例回答，实际需要调用RAG服务生成",
        citations=[
            Citation(
                textbook="示例教材",
                chapter="第一章",
                page=1,
                relevance_score=0.95
            )
        ],
        source_chunks=["这是示例原文内容..."]
    )


@router.get("/status")
async def get_rag_status():
    """
    查询RAG索引状态
    返回：已索引教材数、知识块总数
    """
    return RAGStatus(
        indexed_textbooks=0,
        total_chunks=0,
        status="ready"
    )