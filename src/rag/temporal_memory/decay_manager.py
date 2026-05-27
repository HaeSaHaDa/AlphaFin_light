"""Temporal Memory Decay 관리 모듈."""
from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
IMPORTANCE_MODULE = PROJECT_ROOT / "src" / "rag" / "memory_importance"
sys.path.insert(0, str(IMPORTANCE_MODULE))

from retention_policy import should_decay_memory, DECAY_THRESHOLD  # noqa: E402

DECAY_FACTOR = 0.2
NO_REUSE_DAYS = 14
LOW_REFLECTION_MENTIONS = 0


def _calculate_age_days(ts_str: str) -> int | None:
    if not ts_str:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            ts = datetime.strptime(ts_str, fmt)
            return (datetime.now() - ts).days
        except ValueError:
            continue
    return None


def calculate_decay(memory: dict, evolution: dict | None = None) -> dict:
    """Decay 후 importance 감소량을 계산한다."""
    current = memory.get("importance_score", 0.0)
    evolution = evolution or {}

    penalty = DECAY_FACTOR
    if not evolution.get("has_reoccurrence", False):
        penalty += 0.1
    if memory.get("reflection_mentions", 0) <= LOW_REFLECTION_MENTIONS:
        penalty += 0.05

    age_days = _calculate_age_days(memory.get("timestamp", ""))
    if age_days is not None and age_days > NO_REUSE_DAYS:
        penalty += 0.05

    new_score = round(max(current - penalty, 0.0), 4)

    result = {
        "previous_score": current,
        "decayed_score": new_score,
        "decay_amount": round(current - new_score, 4),
        "decay_factors": {
            "no_reoccurrence": not evolution.get("has_reoccurrence", False),
            "low_reflection": memory.get("reflection_mentions", 0) <= LOW_REFLECTION_MENTIONS,
            "low_reuse": memory.get("reuse_count", 0) == 0,
        },
    }

    logger.info(
        "calculate_decay  id=%s  %.4f → %.4f",
        str(memory.get("memory_id", ""))[:20], current, new_score,
    )
    return result


def should_decay(
    memory: dict,
    evolution: dict | None = None,
) -> bool:
    """Temporal 기준으로 decay 여부를 판단한다."""
    evolution = evolution or {}
    score = memory.get("importance_score", 0.0)

    if should_decay_memory(memory):
        return True

    if score < DECAY_THRESHOLD and memory.get("memory_layer") == "short_term":
        return True

    if (
        not evolution.get("has_reoccurrence", True)
        and memory.get("reuse_count", 0) == 0
        and score < 0.35
    ):
        return True

    return False


def apply_temporal_importance_update(
    memory: dict,
    evolution: dict,
) -> dict:
    """반복 등장·진화 단계에 따라 importance를 보정한다."""
    updated = dict(memory)
    score = updated.get("importance_score", 0.0)

    boost = 0.0
    if evolution.get("has_reoccurrence"):
        boost += min(evolution.get("reoccurrence_count", 0) * 0.03, 0.12)
    if evolution.get("long_term_signal"):
        boost += 0.08
    if evolution.get("evolution_stage") == "structural_shift":
        boost += 0.1

    updated["importance_score"] = round(min(score + boost, 1.0), 4)
    updated["temporal_boost"] = round(boost, 4)
    updated["evolution_stage"] = evolution.get("evolution_stage", "")

    logger.info(
        "apply_temporal_importance_update  score=%.4f  boost=%.4f",
        updated["importance_score"], boost,
    )
    return updated
