"""Trace API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..services.trace_service import get_latest_trace, get_trace_by_id, get_latest_unified_result

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/trace", tags=["trace"])


@router.get("/latest")
def get_latest_trace_api() -> dict:
    trace = get_latest_trace()
    result = get_latest_unified_result()
    if not trace and not result:
        raise HTTPException(status_code=404, detail="Trace 데이터 없음")

    payload = {
        "trace": trace or {},
        "unified_result_summary": {
            "trace_id": (result or {}).get("trace_id", ""),
            "query": (result or {}).get("query", ""),
            "completed_at": (result or {}).get("completed_at", ""),
        },
        "pipeline_flow": [
            "retrieval", "context_assembly", "character_analysis",
            "evaluation", "reflection", "memory_save", "importance_update",
            "temporal_tracking", "event_graph", "stock_chain", "result_save",
        ],
    }
    logger.info("GET /api/trace/latest")
    return payload


@router.get("/{trace_id}")
def get_trace_by_id_api(trace_id: str) -> dict:
    trace = get_trace_by_id(trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/trace/%s  steps=%d", trace_id, len(trace.get("steps", [])))
    return trace
