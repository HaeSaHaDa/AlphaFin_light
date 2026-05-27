"""Retrieval API 서비스."""
from __future__ import annotations

import logging

from .trace_service import get_latest_unified_result, get_unified_result_by_trace

logger = logging.getLogger(__name__)


def fetch_latest_retrieval() -> dict | None:
    result = get_latest_unified_result()
    if not result:
        return None
    return _build_retrieval_payload(result)


def fetch_retrieval_by_trace(trace_id: str) -> dict | None:
    result = get_unified_result_by_trace(trace_id)
    if not result:
        return None
    return _build_retrieval_payload(result)


def _build_retrieval_payload(unified: dict) -> dict:
    analysis = unified.get("analysis_result", {})
    eval_result = unified.get("evaluation_result", {})
    chunks = analysis.get("referenced_chunks", [])

    return {
        "trace_id": unified.get("trace_id", ""),
        "query": unified.get("query", ""),
        "ticker": unified.get("ticker", ""),
        "chunk_count": len(chunks) or unified.get("retrieval_chunk_count", 0),
        "chunks": chunks,
        "retrieval_quality": eval_result.get("retrieval_quality", {}),
        "context_usage": eval_result.get("context_usage", {}),
        "unified_context_length": unified.get("unified_context_length", 0),
    }
