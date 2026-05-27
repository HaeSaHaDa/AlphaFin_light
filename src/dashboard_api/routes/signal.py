"""Signal Evaluation API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.signal_schema import SignalResponse
from ..services.signal_service import fetch_latest_signal, fetch_signal_by_trace

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/signal", tags=["signal"])


@router.get("/latest", response_model=SignalResponse)
def get_latest_signal() -> SignalResponse:
    data = fetch_latest_signal()
    if not data:
        raise HTTPException(status_code=404, detail="Signal 데이터 없음")
    logger.info(
        "GET /api/signal/latest  signal=%s",
        data.get("current_signal", {}).get("signal"),
    )
    return SignalResponse(**data)


@router.get("/{trace_id}", response_model=SignalResponse)
def get_signal_by_trace(trace_id: str) -> SignalResponse:
    data = fetch_signal_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/signal/%s", trace_id)
    return SignalResponse(**data)
