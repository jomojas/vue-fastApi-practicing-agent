import os
from openai import OpenAI
from typing import AsyncGenerator


class LLMService:
    def __init__(self):
        # 实际开发中，建议从 core/config.py 读取
        self.client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL")
        )

    # 1. 普通对话 (一次性返回)
    async def get_chat_response(self, message: str, model: str):
        response = self.client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": message}], stream=False
        )
        return response.choices[0].message.content

    # 2. 流式对话 (生成器)
    async def get_chat_stream(
        self, message: str, model: str
    ) -> AsyncGenerator[str, None]:
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            stream=True,  # 开启流式模式
        )

        # 遍历流式返回的每一个区块 (chunk)
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                yield content  # 类似于 Spring 中的流数据推送到前端


# 单例导出
llm_service = LLMService()
