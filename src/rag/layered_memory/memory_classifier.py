"""Memory Layer 분류 및 importance score 계산 모듈."""
from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

LAYERS = ["short_term", "mid_term", "long_term"]

SHORT_TERM_DAYS = 7
MID_TERM_DAYS = 90

SHORT_TERM_KEYWORDS = [
    "발표", "급등", "급락", "속보", "긴급", "오늘",
    "어제", "이번 주", "최근", "돌파", "폭등", "폭락",
]

LONG_TERM_KEYWORDS = [
    "사이클", "장기", "구조적", "패러다임", "전환",
    "거시", "글로벌 추세", "산업 재편", "장기 성장",
]

HIGH_IMPACT_KEYWORDS = [
    "HBM", "AI", "반도체", "DRAM", "NAND",
    "수요 증가", "공급 부족", "시장 성장",
    "실적 개선", "가격 상승",
]


def classify_memory_layer(memory: dict) -> str:
    """Memory를 시간 및 키워드 기반으로 Layer 분류한다.

    Args:
        memory: Memory dict (timestamp, summary 등 포함).

    Returns:
        "short_term" | "mid_term" | "long_term"
    """
    ts_str = memory.get("timestamp", "")
    age_days = _calculate_age_days(ts_str)

    text = " ".join([
        memory.get("summary", ""),
        memory.get("query", ""),
        memory.get("event_name", ""),
        memory.get("event_summary", ""),
    ])

    short_hits = sum(1 for kw in SHORT_TERM_KEYWORDS if kw in text)
    long_hits = sum(1 for kw in LONG_TERM_KEYWORDS if kw in text)

    if age_days is not None and age_days <= SHORT_TERM_DAYS:
        layer = "short_term"
    elif age_days is not None and age_days > MID_TERM_DAYS:
        layer = "long_term"
    elif long_hits >= 2:
        layer = "long_term"
    elif short_hits >= 2:
        layer = "short_term"
    else:
        layer = "mid_term"

    logger.info(
        "Memory 분류  layer=%s  age=%s  short_kw=%d  long_kw=%d",
        layer,
        f"{age_days}d" if age_days is not None else "?",
        short_hits, long_hits,
    )
    return layer


def calculate_importance_score(memory: dict) -> float:
    """Memory의 importance score를 계산한다.

    기준:
    - 반복 등장 빈도 (키워드 매칭)
    - 시장 영향 범위 (HIGH_IMPACT_KEYWORDS)
    - 이벤트 지속 기간 (age)
    - 분석 구조 완전성

    Returns:
        0.0 ~ 1.0 범위의 importance score.
    """
    score = 0.0

    text = " ".join([
        memory.get("summary", ""),
        memory.get("query", ""),
        memory.get("event_name", ""),
        memory.get("event_summary", ""),
        " ".join(memory.get("bullish_factors", [])),
        " ".join(memory.get("bearish_factors", [])),
        " ".join(memory.get("risks", [])),
    ])

    impact_hits = sum(1 for kw in HIGH_IMPACT_KEYWORDS if kw in text)
    score += min(impact_hits * 0.1, 0.4)

    has_bullish = len(memory.get("bullish_factors", [])) > 0
    has_bearish = len(memory.get("bearish_factors", [])) > 0
    has_risks = len(memory.get("risks", [])) > 0
    has_summary = bool(memory.get("summary"))
    completeness = sum([has_bullish, has_bearish, has_risks, has_summary])
    score += completeness * 0.075

    refs = memory.get("referenced_chunks", [])
    score += min(len(refs) * 0.04, 0.2)

    age_days = _calculate_age_days(memory.get("timestamp", ""))
    if age_days is not None:
        if age_days <= 7:
            score += 0.1
        elif age_days <= 30:
            score += 0.05

    score = round(min(max(score, 0.0), 1.0), 4)

    logger.info(
        "importance_score=%.4f  impact=%d  comp=%d  refs=%d",
        score, impact_hits, completeness, len(refs),
    )
    return score


def is_expired(memory: dict, layer: str) -> bool:
    """Memory가 해당 Layer에서 만료되었는지 확인한다.

    Short-term: 7일 초과 시 만료
    Mid-term: 90일 초과 시 만료
    Long-term: 만료 없음
    """
    if layer == "long_term":
        return False

    age_days = _calculate_age_days(memory.get("timestamp", ""))
    if age_days is None:
        return False

    if layer == "short_term":
        return age_days > SHORT_TERM_DAYS
    if layer == "mid_term":
        return age_days > MID_TERM_DAYS

    return False


def _calculate_age_days(ts_str: str) -> int | None:
    """timestamp 문자열로부터 경과 일수를 계산한다."""
    if not ts_str:
        return None

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            ts = datetime.strptime(ts_str, fmt)
            delta = datetime.now() - ts
            return delta.days
        except ValueError:
            continue

    return None
