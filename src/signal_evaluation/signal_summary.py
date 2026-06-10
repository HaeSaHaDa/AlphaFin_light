"""Signal Evaluation API 요약 페이로드."""
from __future__ import annotations


def build_signal_api_payload(record: dict) -> dict:
    """Dashboard API 응답용 dict."""
    signal = record.get("signal") or {}
    market = record.get("market_outcome") or {}
    metrics = record.get("metrics") or {}

    return {
        "trace_id": record.get("trace_id", ""),
        "query": record.get("query", ""),
        "ticker": record.get("ticker", ""),
        "current_signal": {
            "signal": signal.get("signal", "neutral"),
            "display_label": signal.get("display_label", "중립"),
            "confidence": signal.get("confidence", 0.5),
            "reason": signal.get("reason", []),
        },
        "market_comparison": {
            "price_change_pct": market.get("price_change_pct", 0),
            "period_label": market.get("period_label", ""),
            "direction_correct": market.get("direction_correct", False),
            "actual_direction": market.get("actual_direction", ""),
        },
        "confidence_evaluation": record.get("confidence_evaluation", {}),
        "metrics": {
            "direction_accuracy": metrics.get("direction_accuracy", 0),
            "hit_ratio_pct": metrics.get("hit_ratio_pct", 0),
            "total_signals": metrics.get("total_signals", 0),
            "correct_count": metrics.get("correct_count", 0),
        },
        "timeline": record.get("timeline", []),
        "history": record.get("history", []),
        "confidence_summary": record.get("confidence_summary", {}),
        "summary_text": _build_summary_text(record),
    }


def _build_summary_text(record: dict) -> str:
    signal = record.get("signal") or {}
    label = signal.get("display_label", "중립")
    return (
        f"현재 AI 시장 관점: {label} · "
        "실제 시장 결과가 연동되지 않아 수익률 및 적중률 평가는 제공하지 않습니다."
    )
