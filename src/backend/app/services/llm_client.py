"""
LLM客户端服务
职责：封装LLM API调用，统一管理
"""
import os
import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """LLM统一客户端（支持多种后端）"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = "deepseek-chat"):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_API_BASE", "https://api.deepseek.com/v1")
        self.model = model

        # HTTP客户端
        self.client = httpx.AsyncClient(timeout=60.0)

    async def call(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        """
        调用LLM生成文本
        输入：用户Prompt、可选的系统Prompt、温度参数
        返回：生成的文本
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except httpx.HTTPError as e:
            return f"LLM调用失败: {str(e)}"

    def call_sync(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        """同步版本的LLM调用"""
        import requests

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.HTTPError as e:
            return f"LLM调用失败: {str(e)}"


# 全局LLM客户端实例
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """获取LLM客户端单例"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client