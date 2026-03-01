from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    model: str = "deepseek-ai/DeepSeek-OCR"


class ChatResponse(BaseModel):
    answer: str
    usage: Optional[int] = 0
