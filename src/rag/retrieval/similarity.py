"""Cosine Similarity 기반 벡터 유사도 계산 모듈."""
from __future__ import annotations

import logging
import math

logger = logging.getLogger(__name__)


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """두 벡터 간의 Cosine Similarity를 계산한다.

    Args:
        vec1: 벡터 1.
        vec2: 벡터 2.

    Returns:
        -1.0 ~ 1.0 사이의 유사도 값.
        벡터가 비어있거나 길이가 다르면 0.0을 반환한다.
    """
    if not vec1 or not vec2:
        return 0.0
    if len(vec1) != len(vec2):
        logger.warning(
            "벡터 차원 불일치  vec1=%d  vec2=%d", len(vec1), len(vec2),
        )
        return 0.0

    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0

    return dot / (norm1 * norm2)


def rank_similar_chunks(
    query_vec: list[float],
    chunk_embeddings: list[dict],
    top_k: int = 5,
) -> list[dict]:
    """Query 벡터와 Chunk 벡터 목록 간의 유사도를 계산하고 Top-K를 반환한다.

    Args:
        query_vec: Query Embedding 벡터.
        chunk_embeddings: [{"chunk_id", "embedding_vector", ...}, ...]
        top_k: 반환할 상위 결과 수.

    Returns:
        유사도 순으로 정렬된 상위 K개 결과.
        [{"chunk_id", "score", ...}, ...]
    """
    if not query_vec:
        logger.warning("빈 Query 벡터 — 검색 불가")
        return []

    scored: list[dict] = []
    for item in chunk_embeddings:
        vec = item.get("embedding_vector", [])
        score = cosine_similarity(query_vec, vec)
        scored.append({
            **item,
            "score": round(score, 6),
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    results = scored[:top_k]
    logger.info(
        "rank_similar_chunks  총=%d  top_k=%d  최고score=%.4f",
        len(chunk_embeddings),
        top_k,
        results[0]["score"] if results else 0.0,
    )
    return results
