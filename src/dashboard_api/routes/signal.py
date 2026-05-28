"""Signal Evaluation API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.signal_schema import SignalResponse
from ..services.signal_service import fetch_latest_signal, fetch_signal_by_trace

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/signal", tags=["signal"])


@router.get("/latest")
def get_latest_signal_disabled() -> None:
    from .latest_guard import reject_latest_usage

    reject_latest_usage()


@router.get("/{trace_id}", response_model=SignalResponse)
def get_signal_by_trace(trace_id: str) -> SignalResponse:
    data = fetch_signal_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/signal/%s", trace_id)
    return SignalResponse(**data)
