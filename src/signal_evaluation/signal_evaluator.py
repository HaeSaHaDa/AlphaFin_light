"""Signal Evaluation Engine — 통합 평가 오케스트레이션."""
from __future__ import annotations

import logging

from .confidence_evaluator import evaluate_confidence, summarize_confidence_evaluations
from .direction_accuracy import (
    calc_direction_accuracy,
    calc_hit_ratio,
    is_direction_correct,
)
from .signal_generator import generate_signal
from .signal_history_manager import (
    get_demo_timeline,
    get_market_outcome,
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
    """Unified Engine 결과로 Signal을 생성하고 시장 결과와 비교 평가한다."""
    trace_id = unified.get("trace_id", "")
    analysis = unified.get("analysis_result") or {}
    overall = None
    if eval_report:
        overall = (eval_report.get("scores") or {}).get("overall_score")

    signal_data = generate_signal(analysis, overall_score=overall)
    market = get_market_outcome(trace_id, signal_data["signal"])
    price_pct = market["price_change_pct"]
    direction_correct = is_direction_correct(signal_data["signal"], price_pct)
    conf_eval = evaluate_confidence(signal_data["confidence"], direction_correct)

    timeline = get_demo_timeline()
    history_records = []
    for entry in timeline:
        ok = is_direction_correct(entry["signal"], entry.get("price_change_pct", 0))
        history_records.append({
            **entry,
            "direction_correct": ok,
            "confidence": signal_data["confidence"],
        })

    record = {
        "trace_id": trace_id,
        "query": unified.get("query", ""),
        "ticker": unified.get("ticker", ""),
        "signal": signal_data,
        "market_outcome": {
            **market,
            "price_change_pct": price_pct,
            "direction_correct": direction_correct,
        },
        "confidence_evaluation": conf_eval,
        "timeline": timeline,
        "history": history_records,
        "metrics": {
            "direction_accuracy": calc_direction_accuracy(history_records),
            "hit_ratio_pct": calc_hit_ratio(history_records),
            "total_signals": len(history_records),
            "correct_count": sum(1 for h in history_records if h.get("direction_correct")),
        },
        "confidence_summary": summarize_confidence_evaluations(
            [evaluate_confidence(signal_data["confidence"], h["direction_correct"]) for h in history_records]
        ),
    }

    if save:
        save_signal_record(record)

    logger.info(
        "Signal 평가 완료  trace_id=%s  signal=%s  correct=%s",
        trace_id, signal_data["signal"], direction_correct,
    )
    return record


def get_or_build_signal(
    unified: dict | None,
    eval_report: dict | None,
    trace_id: str,
) -> dict | None:
    """저장된 Signal이 있으면 로드, 없으면 생성."""
    cached = load_signal_record(trace_id)
    if cached:
        return cached
    if unified:
        return evaluate_signal_for_trace(unified, eval_report)
    return None
