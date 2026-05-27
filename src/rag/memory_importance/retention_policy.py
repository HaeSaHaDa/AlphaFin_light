"""Memory Retention 정책 모듈."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

PROMOTE_THRESHOLD = 0.55
DECAY_THRESHOLD = 0.25
HIGH_RETENTION_THRESHOLD = 0.7

LAYER_ORDER = ["short_term", "mid_term", "long_term"]


def should_promote_memory(memory: dict) -> bool:
    """Memory를 상위 Layer로 승격할지 판단한다.

    조건:
    - importance_score >= PROMOTE_THRESHOLD
    - 현재 short_term 또는 mid_term
    - 낮은 중요도 키워드 패널티가 크지 않음
    """
    score = memory.get("importance_score", 0.0)
    layer = memory.get("memory_layer", "short_term")

    if score < PROMOTE_THRESHOLD:
        return False

    if layer == "long_term":
        return False

    factors = memory.get("importance_factors", {})
    penalty = factors.get("low_importance_penalty", 0.0)
    if penalty >= 0.2:
        return False

    logger.info(
        "should_promote=True  id=%s  score=%.4f  layer=%s",
        str(memory.get("memory_id", ""))[:20], score, layer,
    )
    return True


def should_decay_memory(memory: dict) -> bool:
    """Memory를 decay(만료/삭제 후보)할지 판단한다.

    조건:
    - importance_score < DECAY_THRESHOLD
    - short_term Layer
    """
    score = memory.get("importance_score", 0.0)
    layer = memory.get("memory_layer", "short_term")

    if layer != "short_term":
        return False

    if score >= DECAY_THRESHOLD:
        return False

    logger.info(
        "should_decay=True  id=%s  score=%.4f  layer=%s",
        str(memory.get("memory_id", ""))[:20], score, layer,
    )
    return True


def get_promote_target_layer(current_layer: str) -> str | None:
    """승격 대상 Layer를 반환한다."""
    if current_layer == "short_term":
        return "mid_term"
    if current_layer == "mid_term":
        return "long_term"
    return None


def get_retention_action(memory: dict) -> str:
    """Retention 액션을 반환한다: promote | decay | keep | high_retention."""
    score = memory.get("importance_score", 0.0)

    if score >= HIGH_RETENTION_THRESHOLD:
        return "high_retention"
    if should_promote_memory(memory):
        return "promote"
    if should_decay_memory(memory):
        return "decay"
    return "keep"
