"""
RAG问答服务
职责：构建向量索引、检索相关chunk、生成回答
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import uuid

from app.services.llm_client import get_llm_client


class RAGService:
    """RAG服务"""

    def __init__(self, persist_dir: str = "./data/embeddings"):
        # 初始化向量数据库
        self.chroma_client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="textbook_chunks",
            metadata={"hnsw:space": "cosine"}
        )

        # 初始化Embedding模型
        self.embedding_model = SentenceTransformer('BAAI/bge-small-zh-v1.5')

    def build_index(self, textbook_id: str, chunks: List[dict]):
        """
        为教材构建向量索引
        输入：教材ID、知识块列表
        """
        for chunk in chunks:
            # 生成向量
            embedding = self.embedding_model.encode(chunk["content"])

            # 添加到向量库
            self.collection.add(
                embeddings=[embedding.tolist()],
                documents=[chunk["content"]],
                metadatas=[{
                    "textbook": chunk.get("textbook", ""),
                    "chapter": chunk.get("chapter", ""),
                    "page": chunk.get("page", 0)
                }],
                ids=[f"{textbook_id}_{chunk['chunk_id']}"]
            )

    def retrieve(self, question: str, top_k: int = 5) -> List[dict]:
        """
        检索相关chunks
        输入：问题、返回数量
        返回：相关chunks列表
        """
        # 问题转向量
        question_embedding = self.embedding_model.encode(question)

        # 向量检索
        results = self.collection.query(
            query_embeddings=[question_embedding.tolist()],
            n_results=top_k
        )

        # 整理返回结果
        chunks = []
        for i in range(len(results["ids"][0])):
            chunks.append({
                "content": results["documents"][0][i],
                "textbook": results["metadatas"][0][i]["textbook"],
                "chapter": results["metadatas"][0][i]["chapter"],
                "page": results["metadatas"][0][i]["page"],
                "relevance_score": float(results["distances"][0][i])
            })

        return chunks

    async def query(self, question: str) -> dict:
        """
        RAG问答
        输入：用户问题
        返回：回答和引用来源
        """
        # 1. 检索相关chunks
        chunks = self.retrieve(question, top_k=5)

        if not chunks:
            return {
                "answer": "当前知识库中未找到相关信息",
                "citations": [],
                "source_chunks": []
            }

        # 2. 构建上下文
        context = "\n\n".join([
            f"【来源：{c['textbook']}, {c['chapter']}, 第{c['page']}页】\n{c['content']}"
            for c in chunks
        ])

        # 3. 构建Prompt
        prompt = f"""你是一个学科知识助手，只能基于提供的教材内容回答问题。

【教材内容】
{context}

【问题】
{question}

【回答要求】
1. 只基于上述教材内容回答，不使用自身知识
2. 每个回答必须附带来源引用，格式：[教材名, 章节, 页码]
3. 如果上下文中找不到答案，回复"当前知识库中未找到相关信息"

请回答："""

        # 4. 调用LLM生成回答
        llm = get_llm_client()
        answer = await llm.call(prompt, temperature=0.3)

        # 5. 构建引用列表
        citations = [{
            "textbook": c["textbook"],
            "chapter": c["chapter"],
            "page": c["page"],
            "relevance_score": c["relevance_score"]
        } for c in chunks]

        return {
            "answer": answer,
            "citations": citations,
            "source_chunks": [c["content"] for c in chunks]
        }

    def get_status(self) -> dict:
        """获取索引状态"""
        return {
            "indexed_textbooks": len(set(
                id.split("_")[0] for id in self.collection.get()["ids"]
            )),
            "total_chunks": self.collection.count(),
            "status": "ready"
        }