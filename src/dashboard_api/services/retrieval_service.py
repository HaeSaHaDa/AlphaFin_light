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


def _enrich_chunks(chunks: list[dict]) -> list[dict]:
    ranked = sorted(chunks, key=lambda c: c.get("score", 0), reverse=True)
    enriched: list[dict] = []
    for i, chunk in enumerate(ranked, start=1):
        doc_type = chunk.get("document_type", "unknown")
        chunk_id = chunk.get("chunk_id", "")
        ticker = chunk.get("ticker", "")
        enriched.append({
            **chunk,
            "rank": i,
            "source_file": f"data/processed/{doc_type}/chunk_{chunk_id}.json",
            "chunk_preview": (
                f"[{doc_type}] chunk #{chunk_id}"
                + (f" · {ticker}" if ticker else "")
            ),
            "related_entity": ticker or "",
        })
    return enriched


def _build_retrieval_payload(unified: dict) -> dict:
    analysis = unified.get("analysis_result", {})
    eval_result = unified.get("evaluation_result", {})
    chunks = _enrich_chunks(analysis.get("referenced_chunks", []))

    return {
        "trace_id": unified.get("trace_id", ""),
        "query": unified.get("query", ""),
        "ticker": unified.get("ticker", "") or "",
        "chunk_count": len(chunks) or unified.get("retrieval_chunk_count", 0),
        "chunks": chunks,
        "retrieval_quality": eval_result.get("retrieval_quality", {}),
        "context_usage": eval_result.get("context_usage", {}),
        "unified_context_length": unified.get("unified_context_length", 0),
        "retrieval_timestamp": unified.get("completed_at", ""),
        "analysis": {
            "summary": analysis.get("summary", ""),
            "bullish_factors": analysis.get("bullish_factors", []),
            "bearish_factors": analysis.get("bearish_factors", []),
            "risks": analysis.get("risks", []),
            "model": analysis.get("model", ""),
        },
        "context_layers": {
            "retrieval": {
                "chunk_count": len(chunks),
                "context_length": unified.get("unified_context_length", 0),
            },
            "memory": unified.get("memory_updates", {}),
            "reflection": unified.get("reflection_result", {}),
            "stock_chain": unified.get("stock_chain", {}),
            "temporal": unified.get("temporal_result", {}),
        },
    }
