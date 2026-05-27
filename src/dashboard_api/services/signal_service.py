"""Signal Evaluation API 서비스."""
from __future__ import annotations

from src.signal_evaluation.signal_evaluator import (
    evaluate_signal_for_trace,
    get_or_build_signal,
)
from src.signal_evaluation.signal_history_manager import load_latest_signal
from src.signal_evaluation.signal_summary import build_signal_api_payload

from .trace_service import (
    find_evaluation_report,
    get_latest_unified_result,
    get_unified_result_by_trace,
)


def fetch_latest_signal() -> dict | None:
    unified = get_latest_unified_result()
    if not unified:
        cached = load_latest_signal()
        if cached:
            return build_signal_api_payload(cached)
        return None

    trace_id = unified.get("trace_id", "")
    report = find_evaluation_report(trace_id)
    record = get_or_build_signal(unified, report, trace_id)
    if not record:
        return None
    return build_signal_api_payload(record)


def fetch_signal_by_trace(trace_id: str) -> dict | None:
    unified = get_unified_result_by_trace(trace_id)
    report = find_evaluation_report(trace_id)
    record = get_or_build_signal(unified, report, trace_id)
    if not record and unified:
        record = evaluate_signal_for_trace(unified, report)
    if not record:
        return None
    return build_signal_api_payload(record)
