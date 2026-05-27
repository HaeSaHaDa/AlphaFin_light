"""Reflection API 서비스."""
from __future__ import annotations

from .trace_service import get_latest_unified_result, get_unified_result_by_trace


def fetch_latest_reflection() -> dict | None:
    result = get_latest_unified_result()
    if not result:
        return None
    return _build_reflection_payload(result)


def fetch_reflection_by_trace(trace_id: str) -> dict | None:
    result = get_unified_result_by_trace(trace_id)
    if not result:
        return None
    return _build_reflection_payload(result)


def _build_reflection_payload(unified: dict) -> dict:
    reflection = unified.get("reflection_result", {})
    return {
        "trace_id": unified.get("trace_id", ""),
        "query": unified.get("query", ""),
        "persona": unified.get("persona", ""),
        "reflection_summary": reflection.get("reflection_summary", ""),
        "missing_risks": reflection.get("missing_risks", []),
        "overconfidence_detected": reflection.get("overconfidence_detected", False),
        "overconfidence_reasons": reflection.get("overconfidence_reasons", []),
        "context_gaps": reflection.get("context_gaps", []),
        "improvement_suggestions": reflection.get("improvement_suggestions", []),
        "timestamp": reflection.get("timestamp", ""),
    }
