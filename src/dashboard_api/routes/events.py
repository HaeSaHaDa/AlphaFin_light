"""Canonical market events API routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Query

from ..schemas.events_schema import (
    EventEvidenceResponse,
    EventsTickerResponse,
    EventsTraceResponse,
)
from ..services.events_service import (
    fetch_event_evidence,
    fetch_events_by_ticker,
    fetch_events_by_trace,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("/ticker/{ticker}", response_model=EventsTickerResponse)
def get_events_by_ticker(ticker: str) -> EventsTickerResponse:
    data = fetch_events_by_ticker(ticker)
    logger.info("GET /api/events/ticker/%s  count=%d", ticker, data.get("event_count", 0))
    return EventsTickerResponse(**data)


@router.get("/{event_id}/evidence", response_model=EventEvidenceResponse)
def get_event_evidence(event_id: str) -> EventEvidenceResponse:
    if not event_id.startswith("evt_"):
        raise HTTPException(status_code=400, detail="event_id는 evt_ 로 시작해야 합니다")
    data = fetch_event_evidence(event_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"event_id={event_id} evidence 없음")
    logger.info("GET /api/events/%s/evidence  count=%d", event_id, data.get("evidence_count", 0))
    return EventEvidenceResponse(**data)


@router.get("/{trace_id}", response_model=EventsTraceResponse)
def get_events_by_trace(
    trace_id: str,
    ticker: str = Query("", description="selectedTicker 필터"),
) -> EventsTraceResponse:
    if trace_id.startswith("evt_"):
        raise HTTPException(status_code=400, detail="trace_id 엔드포인트에는 trace_id를 사용하세요")
    data = fetch_events_by_trace(trace_id, ticker=ticker or None)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info(
        "GET /api/events/%s  events=%d  ticker=%s",
        trace_id,
        data.get("event_count", 0),
        data.get("ticker"),
    )
    return EventsTraceResponse(**data)
