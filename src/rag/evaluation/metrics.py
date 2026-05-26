"""Evaluation 메트릭 계산 모듈."""
from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

HALLUCINATION_KEYWORDS = [
    "확실히", "반드시", "틀림없이", "100%", "절대적으로",
    "무조건", "당연히", "의심할 여지없이",
]


def calculate_average_similarity(scores: list[float]) -> float:
    """similarity score 목록의 평균을 계산한다."""
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 6)


def calculate_score_stats(scores: list[float]) -> dict:
    """similarity score 통계를 계산한다."""
    if not scores:
        return {"min": 0.0, "max": 0.0, "avg": 0.0, "count": 0}
    return {
        "min": round(min(scores), 6),
        "max": round(max(scores), 6),
        "avg": calculate_average_similarity(scores),
        "count": len(scores),
    }


def check_context_text_in_analysis(
    analysis_text: str,
    context_texts: list[str],
    min_overlap_chars: int = 10,
) -> dict:
    """분석 결과 텍스트가 Context 내용을 참조하는지 검증한다.

    Args:
        analysis_text: 분석 결과 전체 텍스트 (summary + factors 결합).
        context_texts: Chunk 원문 텍스트 목록.
        min_overlap_chars: 겹침 판단 최소 문자 수.

    Returns:
        {"overlap_count", "total_chunks", "overlap_ratio"}
    """
    if not analysis_text or not context_texts:
        return {"overlap_count": 0, "total_chunks": 0, "overlap_ratio": 0.0}

    overlap_count = 0
    for ctx_text in context_texts:
        words = re.findall(r"[\w가-힣]+", ctx_text)
        key_phrases = [w for w in words if len(w) >= min_overlap_chars]

        for phrase in key_phrases[:20]:
            if phrase in analysis_text:
                overlap_count += 1
                break

    total = len(context_texts)
    ratio = round(overlap_count / total, 4) if total > 0 else 0.0

    return {
        "overlap_count": overlap_count,
        "total_chunks": total,
        "overlap_ratio": ratio,
    }


def detect_possible_hallucination(
    analysis_result: dict,
    context: str,
    retrieval_scores: list[float],
) -> dict:
    """hallucination 가능성을 추정한다.

    Args:
        analysis_result: 분석 결과 dict.
        context: RAG Context 문자열.
        retrieval_scores: Retrieval similarity score 목록.

    Returns:
        {
            "risk_level": "low" | "medium" | "high",
            "reasons": [...],
            "assertive_phrases": [...],
        }
    """
    reasons: list[str] = []
    assertive: list[str] = []

    all_text = " ".join([
        analysis_result.get("summary", ""),
        *analysis_result.get("bullish_factors", []),
        *analysis_result.get("bearish_factors", []),
        *analysis_result.get("risks", []),
    ])

    for kw in HALLUCINATION_KEYWORDS:
        if kw in all_text:
            assertive.append(kw)
    if assertive:
        reasons.append(f"단정 표현 사용: {assertive}")

    refs = analysis_result.get("referenced_chunks", [])
    if not refs:
        reasons.append("referenced_chunks 없음")

    avg_score = calculate_average_similarity(retrieval_scores)
    if avg_score < 0.2:
        reasons.append(f"평균 retrieval score 낮음: {avg_score:.4f}")

    has_bullish = len(analysis_result.get("bullish_factors", [])) > 0
    has_bearish = len(analysis_result.get("bearish_factors", [])) > 0
    has_risks = len(analysis_result.get("risks", [])) > 0
    has_summary = bool(analysis_result.get("summary"))
    if not (has_bullish and has_bearish and has_risks and has_summary):
        reasons.append("분석 구조 불완전")

    if len(reasons) == 0:
        risk_level = "low"
    elif len(reasons) <= 1:
        risk_level = "medium"
    else:
        risk_level = "high"

    logger.info(
        "hallucination 추정  risk=%s  reasons=%d",
        risk_level, len(reasons),
    )
    return {
        "risk_level": risk_level,
        "reasons": reasons,
        "assertive_phrases": assertive,
    }
