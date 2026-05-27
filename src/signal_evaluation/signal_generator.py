"""AI 시장 관점(Signal) 생성 모듈."""
from __future__ import annotations

SIGNAL_LABELS = {
    "bullish": "긍정",
    "neutral": "중립",
    "bearish": "부정",
}


def generate_signal(
    analysis_result: dict,
    overall_score: float | None = None,
) -> dict:
    """분석 결과에서 bullish/neutral/bearish Signal을 생성한다."""
    bullish = analysis_result.get("bullish_factors") or []
    bearish = analysis_result.get("bearish_factors") or []
    risks = analysis_result.get("risks") or []

    bull_n = len(bullish)
    bear_n = len(bearish)
    diff = bull_n - bear_n

    if diff >= 2:
        signal = "bullish"
    elif diff <= -2:
        signal = "bearish"
    else:
        signal = "neutral"

    base_conf = 0.55 + min(abs(diff) * 0.08, 0.25)
    if overall_score is not None:
        base_conf = base_conf * 0.5 + float(overall_score) * 0.5
    confidence = round(min(max(base_conf, 0.4), 0.95), 2)

    reasons: list[str] = []
    reasons.extend(bullish[:3])
    if signal == "bearish":
        reasons = list(bearish[:3])
    elif signal == "neutral":
        reasons = (bullish[:1] + bearish[:1] + risks[:1])[:3]

    return {
        "signal": signal,
        "display_label": SIGNAL_LABELS[signal],
        "confidence": confidence,
        "reason": reasons,
        "bullish_count": bull_n,
        "bearish_count": bear_n,
    }
