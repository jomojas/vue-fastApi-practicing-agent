from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest
from app.services.llm_service import llm_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/completions")
async def chat_completions(request: ChatRequest):
    """普通非流式接口"""
    try:
        content = await llm_service.get_chat_response(request.message, request.model)
        return {"answer": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """流式接口 - 像打字机一样逐字返回"""
    try:
        # 获取 Python 生成器
        gen = llm_service.get_chat_stream(request.message, request.model)
        # 返回流式响应，media_type 必须是 text/event-stream (SSE技术，前端开门，后端向前端不断传输内容)
        return StreamingResponse(gen, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
