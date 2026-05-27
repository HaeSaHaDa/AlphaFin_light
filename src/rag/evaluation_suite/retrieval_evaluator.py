"""Retrieval 품질 평가 모듈."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def evaluate_retrieval(unified_result: dict) -> dict:
    """Unified Result에서 Retrieval 품질을 평가한다."""
    analysis = unified_result.get("analysis_result", {})
    eval_result = unified_result.get("evaluation_result", {})
    rq = eval_result.get("retrieval_quality", {})

    refs = analysis.get("referenced_chunks", [])
    scores = [c.get("score", 0.0) for c in refs]
    chunk_count = len(refs) or unified_result.get("retrieval_chunk_count", 0)

    relevance = 0.0
    if rq.get("has_relevant") or (scores and max(scores) >= 0.3):
        relevance = min(max(scores) if scores else 0.4, 1.0)

    doc_types = set(c.get("document_type", "") for c in refs)
    diversity = min(len(doc_types) / 2.0, 1.0) if doc_types else 0.0

    avg_sim = rq.get("score_stats", {}).get("avg", 0.0)
    if not avg_sim and scores:
        avg_sim = sum(scores) / len(scores)
    semantic_similarity = min(avg_sim / 0.5, 1.0) if avg_sim else 0.0

    context_coverage = min(chunk_count / 5.0, 1.0)

    ref_count = eval_result.get("context_usage", {}).get("referenced_count", len(refs))
    reuse_quality = min(ref_count / max(chunk_count, 1), 1.0)

    factors = {
        "relevance": round(relevance, 4),
        "chunk_diversity": round(diversity, 4),
        "semantic_similarity": round(semantic_similarity, 4),
        "context_coverage": round(context_coverage, 4),
        "retrieval_reuse_quality": round(reuse_quality, 4),
    }

    retrieval_score = round(
        sum(factors.values()) / len(factors), 4,
    )

    result = {
        "retrieval_score": retrieval_score,
        "factors": factors,
        "chunk_count": chunk_count,
        "max_similarity": round(max(scores), 4) if scores else 0.0,
    }

    logger.info("Retrieval 평가  score=%.4f  chunks=%d", retrieval_score, chunk_count)
    return result
