"""Trace API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..services.trace_service import (
    get_latest_trace,
    get_trace_by_id,
    get_latest_unified_result,
    get_unified_result_by_trace,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/trace", tags=["trace"])


@router.get("/latest")
def get_latest_trace_disabled() -> None:
    from .latest_guard import reject_latest_usage

    reject_latest_usage()


@router.get("/{trace_id}")
def get_trace_by_id_api(trace_id: str) -> dict:
    trace = get_trace_by_id(trace_id)
    if trace:
        logger.info(
            "GET /api/trace/%s  steps=%d", trace_id, len(trace.get("steps", [])),
        )
        return trace

    unified = get_unified_result_by_trace(trace_id)
    if unified:
        logger.info("GET /api/trace/%s  (trace file 없음, unified summary)", trace_id)
        return {
            "trace_id": trace_id,
            "query": unified.get("query", ""),
            "steps": [],
            "retrieval_summary": {
                "chunk_count": unified.get("retrieval_chunk_count", 0),
            },
        }

    raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
