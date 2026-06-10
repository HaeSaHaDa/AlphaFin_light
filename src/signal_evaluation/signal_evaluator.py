"""Signal Evaluation Engine — 통합 평가 오케스트레이션."""
from __future__ import annotations

import logging

from .signal_generator import generate_signal
from .signal_history_manager import (
    load_signal_record,
    save_signal_record,
)

logger = logging.getLogger(__name__)


def evaluate_signal_for_trace(
    unified: dict,
    eval_report: dict | None = None,
    *,
    save: bool = True,
) -> dict:
    """Unified Engine 결과에서 현재 Signal 관점만 생성한다."""
    trace_id = unified.get("trace_id", "")
    analysis = unified.get("analysis_result") or {}
    overall = None
    if eval_report:
        overall = (eval_report.get("scores") or {}).get("overall_score")

    signal_data = generate_signal(analysis, overall_score=overall)
    record = {
        "trace_id": trace_id,
        "query": unified.get("query", ""),
        "ticker": unified.get("ticker", ""),
        "signal": signal_data,
        "market_outcome": {
            "price_change_pct": 0.0,
            "period_label": "실제 시장 결과 미연동",
            "actual_direction": "unavailable",
            "direction_correct": False,
        },
        "confidence_evaluation": {},
        "timeline": [],
        "history": [],
        "metrics": {
            "direction_accuracy": 0.0,
            "hit_ratio_pct": 0.0,
            "total_signals": 0,
            "correct_count": 0,
        },
        "confidence_summary": {},
    }

    if save:
        save_signal_record(record)

    logger.info(
        "Signal 관점 생성 완료  trace_id=%s  signal=%s  market_outcome=unavailable",
        trace_id, signal_data["signal"],
    )
    return record


def get_or_build_signal(
    unified: dict | None,
    eval_report: dict | None,
    trace_id: str,
) -> dict | None:
    """저장된 Signal이 있으면 로드, 없으면 생성."""
    cached = load_signal_record(trace_id)
    market = (cached or {}).get("market_outcome") or {}
    if cached and market.get("actual_direction") == "unavailable":
        return cached
    if unified:
        return evaluate_signal_for_trace(unified, eval_report)
    return None
