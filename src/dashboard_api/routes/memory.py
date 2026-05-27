"""Memory API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.memory_schema import MemoryLayerResponse, MemoryResponse
from ..services.memory_service import (
    fetch_latest_memory,
    fetch_memory_by_layer,
    fetch_memory_by_trace,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/memory", tags=["memory"])


@router.get("/latest", response_model=MemoryResponse)
def get_latest_memory() -> MemoryResponse:
    data = fetch_latest_memory()
    if not data:
        raise HTTPException(status_code=404, detail="Memory 데이터 없음")
    logger.info("GET /api/memory/latest  trace_id=%s", data.get("trace_id"))
    return MemoryResponse(**data)


@router.get("/layer/{layer}", response_model=MemoryLayerResponse)
def get_memory_by_layer(layer: str) -> MemoryLayerResponse:
    data = fetch_memory_by_layer(layer)
    if not data:
        raise HTTPException(status_code=404, detail=f"layer={layer} 없음")
    logger.info("GET /api/memory/layer/%s  count=%d", layer, data.get("memory_count"))
    return MemoryLayerResponse(**data)


@router.get("/{trace_id}", response_model=MemoryResponse)
def get_memory_by_trace(trace_id: str) -> MemoryResponse:
    data = fetch_memory_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/memory/%s", trace_id)
    return MemoryResponse(**data)
