"""방향 예측 정확도 · Hit Ratio 계산."""
from __future__ import annotations


def is_direction_correct(signal: str, price_change_pct: float) -> bool:
    """Signal 방향과 실제 가격 변화가 일치하는지 판단한다."""
    threshold = 1.0
    if signal == "bullish":
        return price_change_pct > threshold
    if signal == "bearish":
        return price_change_pct < -threshold
    return abs(price_change_pct) <= threshold


def calc_direction_accuracy(records: list[dict]) -> float:
    """방향 예측 정확도 (0~1)."""
    if not records:
        return 0.0
    correct = sum(1 for r in records if r.get("direction_correct"))
    return round(correct / len(records), 4)


def calc_hit_ratio(records: list[dict]) -> float:
    """예측 적중률 (퍼센트)."""
    if not records:
        return 0.0
    correct = sum(1 for r in records if r.get("direction_correct"))
    return round(correct / len(records) * 100, 1)
