"""Engine Run API Route — POST /api/engine/run."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/engine", tags=["engine"])

PROJECT_ROOT = Path(__file__).resolve().parents[4]
ENGINE_DIR = PROJECT_ROOT / "src" / "rag" / "unified_engine"


class EngineRunRequest(BaseModel):
    query: str
    persona: str = "growth_investor"
    ticker: str = "005930"


class EngineRunResponse(BaseModel):
    trace_id: str
    status: str = "completed"
    query: str = ""


def _run_engine(req: EngineRunRequest) -> dict:
    """Unified Engine을 직접 실행하고 result dict를 반환한다."""
    engine_dir = str(ENGINE_DIR)
    if engine_dir not in sys.path:
        sys.path.insert(0, engine_dir)

    try:
        from engine_runner import run_unified_pipeline  # type: ignore[import]
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"engine_runner import 실패: {exc}",
        ) from exc

    try:
        result = run_unified_pipeline(
            query=req.query,
            persona=req.persona,
            ticker=req.ticker,
        )
    except Exception as exc:
        logger.exception("Unified Engine 실행 오류  query=%s", req.query)
        raise HTTPException(
            status_code=500,
            detail=f"Engine 실행 오류: {exc}",
        ) from exc

    return result


@router.post("/run", response_model=EngineRunResponse)
def run_engine(req: EngineRunRequest) -> EngineRunResponse:
    """Unified Engine을 실행하고 trace_id를 반환한다."""
    logger.info("POST /api/engine/run  query=%s  ticker=%s", req.query, req.ticker)

    result = _run_engine(req)
    trace_id = result.get("trace_id", "")

    if not trace_id:
        raise HTTPException(status_code=500, detail="trace_id 생성 실패")

    logger.info("Engine 완료  trace_id=%s", trace_id)
    return EngineRunResponse(
        trace_id=trace_id,
        status="completed",
        query=req.query,
    )
