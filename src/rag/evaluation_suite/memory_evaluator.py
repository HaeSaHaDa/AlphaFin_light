"""Memory 품질 평가 모듈."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def evaluate_memory(unified_result: dict) -> dict:
    """Memory Layer 및 Temporal Memory 품질을 평가한다."""
    memory_updates = unified_result.get("memory_updates", {})
    temporal = unified_result.get("temporal_result", {})
    importance = memory_updates.get("importance", {})
    layered = memory_updates.get("layered_memory", {})

    imp_score = importance.get("importance_score", 0.0)
    importance_consistency = min(imp_score, 1.0) if imp_score > 0 else 0.0

    action = temporal.get("action", "keep")
    evolution = temporal.get("evolution", {})
    temporal_valid = 1.0 if action in ("promote", "keep", "high_retention") else 0.5
    if action == "decay" and imp_score < 0.3:
        temporal_valid = 0.8

    promotion_validity = 1.0 if action == "promote" and imp_score >= 0.5 else 0.6
    if action != "promote":
        promotion_validity = 0.7

    decay_validity = 0.7
    if importance.get("retention_action") == "decay":
        decay_validity = 1.0 if imp_score < 0.25 else 0.4
    elif importance.get("retention_action") in ("keep", "high_retention", "promote"):
        decay_validity = 0.8

    has_memory = bool(memory_updates.get("analysis_memory"))
    reuse_consistency = 0.8 if has_memory and layered.get("memory_count", 0) > 0 else 0.4

    if evolution.get("evolution_chains"):
        temporal_consistency = min(0.5 + len(evolution["evolution_chains"]) * 0.15, 1.0)
    else:
        temporal_consistency = 0.5

    factors = {
        "importance_consistency": round(importance_consistency, 4),
        "temporal_consistency": round(temporal_consistency, 4),
        "promotion_validity": round(promotion_validity, 4),
        "decay_validity": round(decay_validity, 4),
        "retrieval_reuse_consistency": round(reuse_consistency, 4),
        "temporal_action_valid": round(temporal_valid, 4),
    }

    memory_score = round(sum(factors.values()) / len(factors), 4)

    result = {
        "memory_score": memory_score,
        "factors": factors,
        "temporal_action": action,
        "importance_score": imp_score,
        "memory_layer": layered.get("layer", ""),
    }

    logger.info("Memory 평가  score=%.4f  action=%s", memory_score, action)
    return result
