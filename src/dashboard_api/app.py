"""AlphaFin LTE Dashboard Backend API."""
from __future__ import annotations

import logging
import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .routes import (
    retrieval,
    reflection,
    memory,
    stock_chain,
    trace,
    evaluation,
    engine,
    signal,
    company,
    ingestion,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """FastAPI 앱을 생성하고 Route를 등록한다."""
    app = FastAPI(
        title="AlphaFin LTE Dashboard API",
        description="Financial AI Engine 상태 조회 API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        elapsed = round((time.time() - start) * 1000, 2)
        logger.info(
            "%s %s  status=%d  %sms",
            request.method, request.url.path, response.status_code, elapsed,
        )
        return response

    @app.get("/")
    def root() -> dict:
        return {
            "service": "AlphaFin LTE Dashboard API",
            "docs": "/docs",
            "health": "/health",
        }

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "port": os.getenv("PORT", "8000")}

    register_routes(app)
    return app


def register_routes(app: FastAPI) -> None:
    """API Router를 등록한다."""
    app.include_router(retrieval.router)
    app.include_router(reflection.router)
    app.include_router(memory.router)
    app.include_router(stock_chain.router)
    app.include_router(trace.router)
    app.include_router(evaluation.router)
    app.include_router(engine.router)
    app.include_router(signal.router)
    app.include_router(company.router)
    app.include_router(ingestion.router)
    logger.info("API Route 등록 완료")


app = create_app()


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "src.dashboard_api.app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
