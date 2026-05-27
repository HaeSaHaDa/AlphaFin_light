"""Memory Importance 계산 모듈."""
from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
LAYERED_MODULE = PROJECT_ROOT / "src" / "rag" / "layered_memory"
sys.path.insert(0, str(LAYERED_MODULE))

from memory_classifier import calculate_importance_score as _base_importance_score  # noqa: E402

HIGH_IMPORTANCE_KEYWORDS = [
    "NVIDIA", "엔비디아", "실적 발표", "금리", "HBM", "공급 부족",
    "AI 서버", "AI 메모리", "반도체", "DRAM", "시장 성장",
    "투자 확대", "정책 변화",
]

LOW_IMPORTANCE_KEYWORDS = [
    "루머", "일회성", "속보", "단기", "소문", "찌라시",
]

LONG_TERM_INDUSTRY_KEYWORDS = [
    "사이클", "장기", "구조적", "산업 재편", "패러다임",
]

PERSONA_WEIGHT = {
    "growth_investor": 0.05,
    "value_investor": 0.04,
    "risk_averse_analyst": 0.06,
    "aggressive_trader": 0.03,
    "default": 0.02,
}


def _memory_text(memory: dict) -> str:
    return " ".join([
        memory.get("summary", ""),
        memory.get("query", ""),
        memory.get("event_name", ""),
        memory.get("event_summary", ""),
        memory.get("reflection_summary", ""),
        " ".join(memory.get("bullish_factors", [])),
        " ".join(memory.get("bearish_factors", [])),
        " ".join(memory.get("risks", [])),
        " ".join(memory.get("missing_risks", [])),
    ])


def calculate_reuse_score(memory: dict, reuse_count: int = 0) -> float:
    """Retrieval 재사용 빈도 기반 점수 (0.0 ~ 0.2)."""
    count = reuse_count or memory.get("reuse_count", 0)
    score = min(count * 0.04, 0.2)
    logger.debug("reuse_score=%.4f  count=%d", score, count)
    return round(score, 4)


def calculate_event_impact(memory: dict, graphs: list[dict] | None = None) -> float:
    """Event Graph propagation 범위 기반 점수 (0.0 ~ 0.25)."""
    if not graphs:
        return 0.0

    text = _memory_text(memory)
    text_words = set(re.findall(r"[\w가-힣]+", text.lower()))

    max_relations = 0
    for graph in graphs:
        matched = 0
        for rel in graph.get("relations", []):
            rel_text = f"{rel.get('source', '')} {rel.get('target', '')}".lower()
            rel_words = set(re.findall(r"[\w가-힣]+", rel_text))
            if text_words & rel_words:
                matched += 1
        max_relations = max(max_relations, matched)

    score = min(max_relations * 0.05, 0.25)
    logger.debug("event_impact=%.4f  relations=%d", score, max_relations)
    return round(score, 4)


def calculate_reflection_boost(
    memory: dict,
    reflections: list[dict] | None = None,
) -> tuple[float, int]:
    """Reflection 언급 빈도 기반 보정 (0.0 ~ 0.15)."""
    if not reflections:
        return 0.0, 0

    mem_words = set(re.findall(r"[\w가-힣]+", _memory_text(memory).lower()))
    mentions = 0

    for ref in reflections:
        ref_text = " ".join([
            ref.get("reflection_summary", ""),
            ref.get("query", ""),
            " ".join(ref.get("missing_risks", [])),
            " ".join(ref.get("improvement_suggestions", [])),
        ]).lower()
        ref_words = set(re.findall(r"[\w가-힣]+", ref_text))
        overlap = len(mem_words & ref_words)
        if overlap >= 2:
            mentions += 1

    boost = min(mentions * 0.05, 0.15)
    logger.debug("reflection_boost=%.4f  mentions=%d", boost, mentions)
    return round(boost, 4), mentions


def calculate_importance_factors(
    memory: dict,
    reflections: list[dict] | None = None,
    graphs: list[dict] | None = None,
    reuse_count: int = 0,
) -> dict:
    """Importance factor 상세를 계산한다."""
    text = _memory_text(memory)

    market_impact = min(
        sum(1 for kw in HIGH_IMPORTANCE_KEYWORDS if kw in text) * 0.08, 0.4,
    )
    low_penalty = min(
        sum(1 for kw in LOW_IMPORTANCE_KEYWORDS if kw in text) * 0.1, 0.3,
    )
    long_term = min(
        sum(1 for kw in LONG_TERM_INDUSTRY_KEYWORDS if kw in text) * 0.05, 0.15,
    )

    base_score = _base_importance_score(memory)
    reuse_score = calculate_reuse_score(memory, reuse_count)
    event_impact = calculate_event_impact(memory, graphs)
    reflection_boost, reflection_mentions = calculate_reflection_boost(
        memory, reflections,
    )

    persona = memory.get("persona", "default")
    character_weight = PERSONA_WEIGHT.get(persona, PERSONA_WEIGHT["default"])

    factors = {
        "base_score": round(base_score, 4),
        "market_impact": round(market_impact, 4),
        "low_importance_penalty": round(low_penalty, 4),
        "long_term_industry": round(long_term, 4),
        "reuse_score": reuse_score,
        "event_impact": event_impact,
        "reflection_boost": reflection_boost,
        "character_weight": round(character_weight, 4),
    }

    raw = (
        base_score
        + market_impact
        + reuse_score
        + event_impact
        + reflection_boost
        + long_term
        + character_weight
        - low_penalty
    )
    factors["raw_total"] = round(raw, 4)
    factors["reflection_mentions"] = reflection_mentions

    return factors


def calculate_importance(
    memory: dict,
    reflections: list[dict] | None = None,
    graphs: list[dict] | None = None,
    reuse_count: int = 0,
) -> dict:
    """Memory의 종합 importance를 계산한다.

    Returns:
        {
            "memory_id", "importance_score", "importance_factors",
            "importance_reasons", "reuse_count", "reflection_mentions"
        }
    """
    factors = calculate_importance_factors(
        memory, reflections, graphs, reuse_count,
    )

    score = round(min(max(factors["raw_total"], 0.0), 1.0), 4)
    reasons = _build_importance_reasons(memory, factors)

    memory_id = memory.get("memory_id") or _generate_memory_id(memory)

    result = {
        "memory_id": memory_id,
        "importance_score": score,
        "importance_factors": factors,
        "importance_reasons": reasons,
        "reuse_count": reuse_count or memory.get("reuse_count", 0),
        "reflection_mentions": factors.get("reflection_mentions", 0),
    }

    logger.info(
        "calculate_importance  id=%s  score=%.4f  reasons=%d",
        memory_id[:20], score, len(reasons),
    )
    return result


def _build_importance_reasons(memory: dict, factors: dict) -> list[str]:
    reasons: list[str] = []
    text = _memory_text(memory)

    if factors.get("market_impact", 0) >= 0.16:
        reasons.append("높은 시장 영향 키워드 포함")
    if factors.get("event_impact", 0) > 0:
        reasons.append("Event Graph 연관 관계 존재")
    if factors.get("reflection_boost", 0) > 0:
        reasons.append("Reflection에서 언급됨")
    if factors.get("reuse_score", 0) >= 0.08:
        reasons.append("Retrieval 재사용 빈도 높음")
    if factors.get("long_term_industry", 0) > 0:
        reasons.append("장기 산업 영향 가능성")
    if factors.get("low_importance_penalty", 0) > 0:
        reasons.append("낮은 중요도 키워드(루머/일회성) 포함")

    for kw in HIGH_IMPORTANCE_KEYWORDS:
        if kw in text and kw not in str(reasons):
            if len(reasons) < 5:
                reasons.append(f"핵심 키워드: {kw}")

    return reasons[:6]


def _generate_memory_id(memory: dict) -> str:
    query = memory.get("query", "unknown")[:20]
    ts = memory.get("timestamp", "notime")
    persona = memory.get("persona", "default")
    mem_type = memory.get("memory_type", "memory")
    safe_query = re.sub(r"[^\w가-힣]", "_", query)
    return f"{mem_type}_{persona}_{safe_query}_{ts}".replace(" ", "_")
