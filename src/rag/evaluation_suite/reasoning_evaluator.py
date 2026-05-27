"""Reasoning 및 Reflection 품질 평가 모듈."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

HALLUCINATION_LEVEL_SCORE = {
    "low": 0.9,
    "medium": 0.5,
    "high": 0.2,
}


def evaluate_reasoning(unified_result: dict, trace: dict | None = None) -> dict:
    """Financial Analysis Reasoning 품질을 평가한다."""
    analysis = unified_result.get("analysis_result", {})
    eval_result = unified_result.get("evaluation_result", {})

    bullish = len(analysis.get("bullish_factors", []))
    bearish = len(analysis.get("bearish_factors", []))
    risks = len(analysis.get("risks", []))

    total_factors = bullish + bearish + risks
    if total_factors > 0:
        balance = 1.0 - abs(bullish - bearish) / total_factors
    else:
        balance = 0.0

    risk_coverage = min(risks / 3.0, 1.0) if risks else 0.0

    aq = eval_result.get("analysis_quality", {})
    structure_score = 1.0 if aq.get("structure_complete") else 0.5

    overlap = eval_result.get("context_usage", {}).get(
        "context_overlap", {},
    ).get("overlap_ratio", 0.0)
    evidence_consistency = max(overlap, 0.3) if aq.get("structure_complete") else overlap

    halluc = eval_result.get("hallucination_risk", {})
    risk_level = halluc.get("risk_level", "medium")
    hallucination_component = HALLUCINATION_LEVEL_SCORE.get(risk_level, 0.5)

    trace_steps = (trace or {}).get("steps", [])
    expected_steps = {
        "retrieval", "character_analysis", "evaluation", "reflection",
    }
    completed = {s.get("step") for s in trace_steps if s.get("status") == "ok"}
    trace_consistency = len(completed & expected_steps) / len(expected_steps)

    factors = {
        "bullish_bearish_balance": round(balance, 4),
        "risk_coverage": round(risk_coverage, 4),
        "evidence_consistency": round(evidence_consistency, 4),
        "hallucination_component": round(hallucination_component, 4),
        "reasoning_trace_consistency": round(trace_consistency, 4),
        "structure_complete": round(structure_score, 4),
    }

    reasoning_score = round(sum(factors.values()) / len(factors), 4)

    result = {
        "reasoning_score": reasoning_score,
        "factors": factors,
        "hallucination_risk_level": risk_level,
    }

    logger.info("Reasoning 평가  score=%.4f  hallucination=%s", reasoning_score, risk_level)
    return result


def evaluate_reflection(unified_result: dict) -> dict:
    """Reflection 품질을 평가한다."""
    reflection = unified_result.get("reflection_result", {})

    missing = reflection.get("missing_risks", [])
    overconf = reflection.get("overconfidence_detected", False)
    gaps = reflection.get("context_gaps", [])
    suggestions = reflection.get("improvement_suggestions", [])
    has_summary = bool(reflection.get("reflection_summary"))

    missing_detection = min(len(missing) / 3.0, 1.0) if missing else 0.3
    overconfidence_detection = 1.0 if overconf else 0.4
    context_gap_detection = min(len(gaps) / 2.0, 1.0) if gaps else 0.3
    usefulness = 0.0
    if has_summary:
        usefulness += 0.4
    if suggestions:
        usefulness += min(len(suggestions) * 0.2, 0.6)
    usefulness = min(usefulness, 1.0)

    factors = {
        "missing_risk_detection": round(missing_detection, 4),
        "overconfidence_detection": round(overconfidence_detection, 4),
        "context_gap_detection": round(context_gap_detection, 4),
        "reflection_usefulness": round(usefulness, 4),
    }

    reflection_score = round(sum(factors.values()) / len(factors), 4)

    result = {
        "reflection_score": reflection_score,
        "factors": factors,
        "missing_risks_count": len(missing),
        "overconfidence_detected": overconf,
    }

    logger.info("Reflection 평가  score=%.4f", reflection_score)
    return result
