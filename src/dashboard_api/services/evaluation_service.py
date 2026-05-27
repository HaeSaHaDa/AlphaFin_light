"""Evaluation API 서비스."""
from __future__ import annotations

from .trace_service import (
    get_latest_unified_result,
    get_unified_result_by_trace,
    find_evaluation_report,
)


def fetch_latest_evaluation() -> dict | None:
    result = get_latest_unified_result()
    if not result:
        return None
    trace_id = result.get("trace_id", "")
    report = find_evaluation_report(trace_id)
    return _build_evaluation_payload(result, report)


def fetch_evaluation_by_trace(trace_id: str) -> dict | None:
    result = get_unified_result_by_trace(trace_id)
    report = find_evaluation_report(trace_id)
    if not result and not report:
        return None
    return _build_evaluation_payload(result or {}, report)


def _build_evaluation_payload(unified: dict, report: dict | None) -> dict:
    scores = (report or {}).get("scores", {})
    if not scores and unified:
        scores = {}

    return {
        "trace_id": (report or unified).get("trace_id", unified.get("trace_id", "")),
        "query": (report or unified).get("query", unified.get("query", "")),
        "retrieval_score": scores.get("retrieval_score"),
        "reasoning_score": scores.get("reasoning_score"),
        "reflection_score": scores.get("reflection_score"),
        "memory_score": scores.get("memory_score"),
        "stock_chain_score": scores.get("stock_chain_score"),
        "overall_score": scores.get("overall_score"),
        "consistency": (report or {}).get("consistency", {}),
        "hallucination_risk": (report or {}).get("hallucination_risk", {}),
        "evaluated_at": (report or {}).get("evaluated_at", ""),
        "full_report": report,
    }
