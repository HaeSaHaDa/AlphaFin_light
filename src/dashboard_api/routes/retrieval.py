"""Retrieval API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.retrieval_schema import RetrievalResponse
from ..services.retrieval_service import fetch_latest_retrieval, fetch_retrieval_by_trace

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/retrieval", tags=["retrieval"])


@router.get("/latest", response_model=RetrievalResponse)
def get_latest_retrieval() -> RetrievalResponse:
    data = fetch_latest_retrieval()
    if not data:
        raise HTTPException(status_code=404, detail="Retrieval 데이터 없음")
    logger.info("GET /api/retrieval/latest  trace_id=%s", data.get("trace_id"))
    return RetrievalResponse(**data)


@router.get("/{trace_id}", response_model=RetrievalResponse)
def get_retrieval_by_trace(trace_id: str) -> RetrievalResponse:
    data = fetch_retrieval_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/retrieval/%s", trace_id)
    return RetrievalResponse(**data)
