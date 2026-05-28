"""trace_id 기반 Dashboard API 응답 조립."""
from __future__ import annotations

from src.dashboard_api.services.evaluation_service import _build_evaluation_payload
from src.dashboard_api.services.memory_service import fetch_memory_by_trace
from src.dashboard_api.services.reflection_service import _build_reflection_payload
from src.dashboard_api.services.retrieval_service import _build_retrieval_payload
from src.dashboard_api.services.signal_service import fetch_signal_by_trace

from .trace_manager import (
    get_evaluation_report,
    get_stock_chain,
    get_trace,
    get_unified_result,
)


def build_dashboard_bundle(trace_id: str) -> dict | None:
    unified = get_unified_result(trace_id)
    if not unified:
        return None

    retrieval = _build_retrieval_payload(unified)
    reflection = _build_reflection_payload(unified)
    memory = fetch_memory_by_trace(trace_id)
    report = get_evaluation_report(trace_id)
    evaluation = _build_evaluation_payload(unified, report)
    signal = fetch_signal_by_trace(trace_id)

    chain_data = get_stock_chain(trace_id)
    trace_raw = get_trace(trace_id)
    stock_chain = {
        "trace_id": trace_id,
        "query": unified.get("query", ""),
        "ticker": unified.get("ticker", ""),
        "summary": unified.get("stock_chain", {}),
        "chain": chain_data or {},
    }

    trace_payload = {
        "trace": trace_raw or {
            "trace_id": trace_id,
            "query": unified.get("query", ""),
            "ticker": unified.get("ticker", ""),
            "steps": [],
        },
        "unified_result_summary": {
            "trace_id": trace_id,
            "query": unified.get("query", ""),
            "ticker": unified.get("ticker", ""),
            "completed_at": unified.get("completed_at", ""),
        },
        "pipeline_flow": [
            "retrieval", "context_assembly", "character_analysis",
            "evaluation", "reflection", "memory_save", "importance_update",
            "temporal_tracking", "event_graph", "stock_chain", "result_save",
        ],
    }

    return {
        "trace_id": trace_id,
        "ticker": unified.get("ticker", ""),
        "query": unified.get("query", ""),
        "retrieval": retrieval,
        "reflection": reflection,
        "memory": memory,
        "stock_chain": stock_chain,
        "trace": trace_payload,
        "evaluation": evaluation,
        "signal": signal,
    }
