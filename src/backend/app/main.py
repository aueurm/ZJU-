"""
FastAPI 应用入口
职责：初始化应用、配置中间件、注册路由
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, graph, merge, rag, chat

# 创建FastAPI应用实例
app = FastAPI(
    title="学科知识整合智能体",
    description="将多本教材整合压缩到30%",
    version="1.0.0"
)

# 配置CORS跨域 - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册各功能模块路由
app.include_router(upload.router, prefix="/api/upload", tags=["教材上传"])
app.include_router(graph.router, prefix="/api/graph", tags=["知识图谱"])
app.include_router(merge.router, prefix="/api/merge", tags=["跨教材整合"])
app.include_router(rag.router, prefix="/api/rag", tags=["RAG问答"])
app.include_router(chat.router, prefix="/api/chat", tags=["对话交互"])


@app.get("/")
async def root():
    """根路径 - 健康检查"""
    return {"message": "学科知识整合智能体服务运行中", "status": "ok"}