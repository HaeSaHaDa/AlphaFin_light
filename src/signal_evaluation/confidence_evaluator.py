"""분석 신뢰도(Confidence) 평가 모듈."""
from __future__ import annotations


def evaluate_confidence(
    confidence: float,
    direction_correct: bool,
) -> dict:
    """신뢰도 대비 방향 예측 결과를 평가한다."""
    high = confidence >= 0.75
    if high and direction_correct:
        outcome = "high_confidence_success"
        label = "높은 신뢰도 · 방향 일치"
    elif high and not direction_correct:
        outcome = "high_confidence_miss"
        label = "높은 신뢰도 · 방향 불일치"
    elif not high and direction_correct:
        outcome = "low_confidence_success"
        label = "보통 신뢰도 · 방향 일치"
    else:
        outcome = "low_confidence_miss"
        label = "보통 신뢰도 · 방향 불일치"

    return {
        "confidence": confidence,
        "direction_correct": direction_correct,
        "outcome": outcome,
        "label": label,
        "is_high_confidence": high,
    }


def summarize_confidence_evaluations(evaluations: list[dict]) -> dict:
    """여러 평가의 신뢰도 요약."""
    if not evaluations:
        return {"avg_confidence": 0.0, "high_confidence_hit_rate": 0.0}

    avg = sum(e["confidence"] for e in evaluations) / len(evaluations)
    high = [e for e in evaluations if e.get("is_high_confidence")]
    high_hits = sum(1 for e in high if e.get("direction_correct"))
    hit_rate = (high_hits / len(high) * 100) if high else 0.0

    return {
        "avg_confidence": round(avg, 3),
        "high_confidence_hit_rate": round(hit_rate, 1),
        "high_confidence_count": len(high),
    }
