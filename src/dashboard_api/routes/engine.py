"""Engine Run API Route — POST /api/engine/run."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.company_resolver.company_resolver import resolve_company
from src.ingestion_pipeline.ingestion_runner import run_ingestion_for_company

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/engine", tags=["engine"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENGINE_DIR = PROJECT_ROOT / "src" / "rag" / "unified_engine"


class EngineRunRequest(BaseModel):
    query: str
    persona: str = "growth_investor"
    ticker: str | None = None
    skip_ingestion: bool = False


class EngineRunResponse(BaseModel):
    trace_id: str
    status: str = "completed"
    query: str = ""
    ticker: str = ""


def _run_engine(req: EngineRunRequest, ticker: str) -> dict:
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
        return run_unified_pipeline(
            query=req.query,
            persona=req.persona,
            ticker=ticker,
        )
    except Exception as exc:
        logger.exception("Unified Engine 실행 오류  query=%s", req.query)
        raise HTTPException(
            status_code=500,
            detail=f"Engine 실행 오류: {exc}",
        ) from exc


@router.post("/run", response_model=EngineRunResponse)
def run_engine(req: EngineRunRequest) -> EngineRunResponse:
    """회사 식별 → ingestion → Unified Engine 실행."""
    logger.info("POST /api/engine/run  query=%s", req.query)

    resolved = resolve_company(req.query)
    if resolved is None and not req.ticker:
        raise HTTPException(
            status_code=400,
            detail="질문에서 회사를 식별할 수 없습니다. 회사명을 포함해 주세요.",
        )

    ticker = req.ticker or (resolved.ticker if resolved else "")
    if resolved and not req.skip_ingestion:
        run_ingestion_for_company(resolved)

    result = _run_engine(req, ticker)
    trace_id = result.get("trace_id", "")
    if not trace_id:
        raise HTTPException(status_code=500, detail="trace_id 생성 실패")

    logger.info("Engine 완료  trace_id=%s  ticker=%s", trace_id, ticker)
    return EngineRunResponse(
        trace_id=trace_id,
        status="completed",
        query=req.query,
        ticker=ticker,
    )
