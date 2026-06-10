"""Memory API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.memory_schema import MemoryLayerResponse, MemoryResponse
from ..schemas.events_schema import MemoryEventsResponse
from ..services.events_service import fetch_memory_events
from ..services.memory_service import (
    fetch_latest_memory,
    fetch_memory_by_layer,
    fetch_memory_by_trace,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/memory", tags=["memory"])


@router.get("/latest")
def get_latest_memory_disabled() -> None:
    from .latest_guard import reject_latest_usage

    reject_latest_usage()


@router.get("/layer/{layer}", response_model=MemoryLayerResponse)
def get_memory_by_layer(layer: str) -> MemoryLayerResponse:
    data = fetch_memory_by_layer(layer)
    if not data:
        raise HTTPException(status_code=404, detail=f"layer={layer} 없음")
    logger.info("GET /api/memory/layer/%s  count=%d", layer, data.get("memory_count"))
    return MemoryLayerResponse(**data)


@router.get("/events/{trace_id}", response_model=MemoryEventsResponse)
def get_memory_events(trace_id: str) -> MemoryEventsResponse:
    data = fetch_memory_events(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info(
        "GET /api/memory/events/%s  events=%d",
        trace_id,
        data.get("event_count", 0),
    )
    return MemoryEventsResponse(**data)


@router.get("/{trace_id}", response_model=MemoryResponse)
def get_memory_by_trace(trace_id: str) -> MemoryResponse:
    data = fetch_memory_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/memory/%s", trace_id)
    return MemoryResponse(**data)
