from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 必须在导入 routes 和 services 之前加载环境变量
load_dotenv()

from app.routes import chat  # 导入路由模块


app = FastAPI(
    title="Jomo LLM API", description="基于 FastAPI 的大模型后端服务", version="1.0.0"
)

# 跨域配置 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许前端 Vue 访问
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册组件 (类似于 Spring Boot 的 Controller 注册)
app.include_router(chat.router)


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
