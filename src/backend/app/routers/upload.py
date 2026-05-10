"""
教材上传路由
职责：处理教材文件上传、解析、存储
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.models import TextbookInfo, TextbookDetail

router = APIRouter()

# 模拟存储（实际应使用数据库或文件系统）
_textbooks: dict = {}


@router.post("/")
async def upload_textbook(file: UploadFile = File(...)):
    """
    上传教材文件
    接收：PDF/MD/TXT/DOCX文件
    返回：教材ID和解析状态
    """
    # 检查文件格式
    allowed_extensions = [".pdf", ".md", ".txt", ".docx"]
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise HTTPException(status_code=400, detail="不支持的文件格式")

    # 生成教材ID
    textbook_id = f"book_{len(_textbooks) + 1:03d}"

    # 存储教材信息（实际应调用解析服务）
    _textbooks[textbook_id] = {
        "textbook_id": textbook_id,
        "filename": file.filename,
        "title": file.filename.split(".")[0],
        "total_pages": 0,
        "total_chars": 0,
        "status": "parsed"  # 实际应为parsing，解析完成后更新
    }

    return {
        "textbook_id": textbook_id,
        "filename": file.filename,
        "status": "parsed",
        "message": "上传成功，解析完成"
    }


@router.get("/list")
async def get_textbook_list():
    """
    获取已上传教材列表
    返回：所有教材的基本信息
    """
    return {"textbooks": list(_textbooks.values())}


@router.get("/{textbook_id}")
async def get_textbook_detail(textbook_id: str):
    """
    获取单本教材详情
    返回：教材信息和章节结构
    """
    if textbook_id not in _textbooks:
        raise HTTPException(status_code=404, detail="教材不存在")

    return _textbooks[textbook_id]