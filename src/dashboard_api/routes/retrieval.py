"""Retrieval API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.retrieval_schema import RetrievalResponse
from ..services.retrieval_service import fetch_latest_retrieval, fetch_retrieval_by_trace

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/retrieval", tags=["retrieval"])


@router.get("/latest")
def get_latest_retrieval_disabled() -> None:
    from .latest_guard import reject_latest_usage

    reject_latest_usage()


@router.get("/{trace_id}", response_model=RetrievalResponse)
def get_retrieval_by_trace(trace_id: str) -> RetrievalResponse:
    data = fetch_retrieval_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/retrieval/%s", trace_id)
    return RetrievalResponse(**data)
