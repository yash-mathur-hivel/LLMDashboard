from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import proxy, logs, analytics, mcp

app = FastAPI(title="LLM Dashboard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proxy.router)
app.include_router(logs.router)
app.include_router(analytics.router)
app.include_router(mcp.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
