"""Reflection API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.reflection_schema import ReflectionResponse
from ..services.reflection_service import fetch_latest_reflection, fetch_reflection_by_trace

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/reflection", tags=["reflection"])


@router.get("/latest", response_model=ReflectionResponse)
def get_latest_reflection() -> ReflectionResponse:
    data = fetch_latest_reflection()
    if not data:
        raise HTTPException(status_code=404, detail="Reflection 데이터 없음")
    logger.info("GET /api/reflection/latest  trace_id=%s", data.get("trace_id"))
    return ReflectionResponse(**data)


@router.get("/{trace_id}", response_model=ReflectionResponse)
def get_reflection_by_trace(trace_id: str) -> ReflectionResponse:
    data = fetch_reflection_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/reflection/%s", trace_id)
    return ReflectionResponse(**data)
