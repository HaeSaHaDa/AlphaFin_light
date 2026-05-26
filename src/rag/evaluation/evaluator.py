"""RAG 금융 분석 결과 평가 모듈."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from metrics import (  # noqa: E402
    calculate_score_stats,
    check_context_text_in_analysis,
    detect_possible_hallucination,
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation"


def evaluate_retrieval_quality(chunks: list[dict]) -> dict:
    """Retrieval 결과의 품질을 평가한다.

    Args:
        chunks: Retrieval 결과 목록 (score 포함).

    Returns:
        {
            "chunk_count", "score_stats",
            "doc_type_distribution", "has_relevant"
        }
    """
    scores = [c.get("score", 0.0) for c in chunks]
    stats = calculate_score_stats(scores)

    type_dist: dict[str, int] = {}
    for c in chunks:
        dt = c.get("document_type", "unknown")
        type_dist[dt] = type_dist.get(dt, 0) + 1

    has_relevant = stats["max"] >= 0.3

    result = {
        "chunk_count": len(chunks),
        "score_stats": stats,
        "doc_type_distribution": type_dist,
        "has_relevant": has_relevant,
    }

    logger.info(
        "Retrieval 품질  chunks=%d  max=%.4f  avg=%.4f  relevant=%s",
        len(chunks), stats["max"], stats["avg"], has_relevant,
    )
    return result


def evaluate_context_usage(
    analysis_result: dict,
    context_chunks: list[dict],
) -> dict:
    """분석 결과가 Context를 실제로 사용했는지 평가한다.

    Args:
        analysis_result: analyze_financial_query 결과.
        context_chunks: Retrieval로 얻은 Chunk 목록.

    Returns:
        {"referenced_count", "context_overlap", "usage_rating"}
    """
    refs = analysis_result.get("referenced_chunks", [])

    all_analysis_text = " ".join([
        analysis_result.get("summary", ""),
        *analysis_result.get("bullish_factors", []),
        *analysis_result.get("bearish_factors", []),
        *analysis_result.get("risks", []),
    ])

    chunk_texts = [c.get("chunk_text", "") for c in context_chunks]
    overlap = check_context_text_in_analysis(all_analysis_text, chunk_texts)

    if overlap["overlap_ratio"] >= 0.5:
        usage_rating = "good"
    elif overlap["overlap_ratio"] >= 0.2:
        usage_rating = "partial"
    else:
        usage_rating = "weak"

    result = {
        "referenced_count": len(refs),
        "context_overlap": overlap,
        "usage_rating": usage_rating,
    }

    logger.info(
        "Context 사용  refs=%d  overlap=%.2f  rating=%s",
        len(refs), overlap["overlap_ratio"], usage_rating,
    )
    return result


def evaluate_analysis_result(
    analysis_result: dict,
    context_chunks: list[dict],
    context_text: str,
) -> dict:
    """분석 결과 전체를 종합 평가한다.

    Args:
        analysis_result: analyze_financial_query 결과.
        context_chunks: Retrieval 결과 Chunk 목록.
        context_text: prompt_context 문자열.

    Returns:
        {
            "query", "retrieval_quality", "context_usage",
            "analysis_quality", "hallucination_risk", "scores"
        }
    """
    query = analysis_result.get("query", "")
    scores = [c.get("score", 0.0) for c in context_chunks]

    retrieval_q = evaluate_retrieval_quality(context_chunks)
    context_u = evaluate_context_usage(analysis_result, context_chunks)

    analysis_q = {
        "has_bullish": len(analysis_result.get("bullish_factors", [])) > 0,
        "has_bearish": len(analysis_result.get("bearish_factors", [])) > 0,
        "has_risks": len(analysis_result.get("risks", [])) > 0,
        "has_summary": bool(analysis_result.get("summary")),
        "bullish_count": len(analysis_result.get("bullish_factors", [])),
        "bearish_count": len(analysis_result.get("bearish_factors", [])),
        "risks_count": len(analysis_result.get("risks", [])),
    }
    analysis_q["structure_complete"] = all([
        analysis_q["has_bullish"],
        analysis_q["has_bearish"],
        analysis_q["has_risks"],
        analysis_q["has_summary"],
    ])

    hallucination = detect_possible_hallucination(
        analysis_result, context_text, scores,
    )

    evaluation = {
        "query": query,
        "retrieval_quality": retrieval_q,
        "context_usage": context_u,
        "analysis_quality": analysis_q,
        "hallucination_risk": hallucination,
        "scores": {
            "retrieval_scores": [round(s, 6) for s in scores],
            "score_stats": retrieval_q["score_stats"],
        },
    }

    logger.info(
        "종합 평가  query='%s'  retrieval=%s  context=%s  hallucination=%s",
        query[:30],
        "OK" if retrieval_q["has_relevant"] else "WEAK",
        context_u["usage_rating"],
        hallucination["risk_level"],
    )
    return evaluation


def save_evaluation_json(
    evaluation: dict,
    output_dir: Path | str | None = None,
    filename: str = "evaluation.json",
) -> Path | None:
    """평가 결과를 JSON으로 저장한다."""
    out = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(evaluation, f, ensure_ascii=False, indent=2)

    logger.info("Evaluation JSON 저장  %s", filepath)
    return filepath
