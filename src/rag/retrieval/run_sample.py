"""삼성전자 관련 샘플 Query Retrieval 검증 스크립트."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
EMBEDDING_MODULE = PROJECT_ROOT / "src" / "rag" / "embedding"
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))

from connection import get_connection  # noqa: E402
from embedder import generate_embedding  # noqa: E402
from retriever import (  # noqa: E402
    fetch_embeddings_from_db,
    filter_chunks_by_metadata,
    retrieve_similar_chunks,
)
from similarity import cosine_similarity, rank_similar_chunks  # noqa: E402

SAMPLE_QUERIES = [
    "삼성전자 반도체 실적 전망",
    "HBM 수요 증가",
    "AI 반도체 시장 성장",
]


def test_cosine_similarity(logger: logging.Logger) -> bool:
    """Cosine Similarity 기본 계산 검증."""
    logger.info("--- Cosine Similarity 기본 검증 ---")

    vec_a = [1.0, 0.0, 0.0]
    vec_b = [1.0, 0.0, 0.0]
    score_same = cosine_similarity(vec_a, vec_b)
    logger.info("동일 벡터  score=%.4f  (기대: 1.0)", score_same)

    vec_c = [1.0, 0.0, 0.0]
    vec_d = [0.0, 1.0, 0.0]
    score_orth = cosine_similarity(vec_c, vec_d)
    logger.info("직교 벡터  score=%.4f  (기대: 0.0)", score_orth)

    vec_e = [1.0, 0.0, 0.0]
    vec_f = [-1.0, 0.0, 0.0]
    score_opp = cosine_similarity(vec_e, vec_f)
    logger.info("반대 벡터  score=%.4f  (기대: -1.0)", score_opp)

    ok = (
        abs(score_same - 1.0) < 1e-6
        and abs(score_orth - 0.0) < 1e-6
        and abs(score_opp - (-1.0)) < 1e-6
    )
    logger.info("Cosine Similarity 검증: %s", "OK" if ok else "FAIL")
    return ok


def test_rank_similar(logger: logging.Logger) -> bool:
    """rank_similar_chunks 정렬 검증."""
    logger.info("--- rank_similar_chunks 검증 ---")

    query_vec = [1.0, 0.5, 0.0]
    chunks = [
        {"chunk_id": 100, "embedding_vector": [0.0, 1.0, 0.0]},
        {"chunk_id": 101, "embedding_vector": [1.0, 0.5, 0.0]},
        {"chunk_id": 102, "embedding_vector": [0.5, 0.5, 0.5]},
    ]

    ranked = rank_similar_chunks(query_vec, chunks, top_k=2)
    logger.info("Top-2 결과:")
    for r in ranked:
        logger.info("  chunk_id=%s  score=%.4f", r["chunk_id"], r["score"])

    ok = len(ranked) == 2 and ranked[0]["chunk_id"] == 101
    logger.info("rank_similar_chunks 검증: %s", "OK" if ok else "FAIL")
    return ok


def test_db_retrieval(logger: logging.Logger) -> bool:
    """DB Embedding 조회 및 Retrieval 흐름 검증."""
    logger.info("--- DB Retrieval 검증 ---")

    embeddings = fetch_embeddings_from_db({"ticker": "005930"})
    logger.info("DB Embedding 조회: %d건", len(embeddings))

    if not embeddings:
        logger.warning("DB에 Embedding 없음 — 건너뜀")
        return False

    for emb in embeddings[:3]:
        vec = emb.get("embedding_vector", [])
        logger.info(
            "  chunk_id=%s  type=%s  dim=%d  text_len=%s",
            emb["chunk_id"],
            emb["document_type"],
            len(vec) if isinstance(vec, list) else 0,
            emb.get("chunk_length"),
        )

    ref_vec = embeddings[0]["embedding_vector"]
    ranked = rank_similar_chunks(ref_vec, embeddings, top_k=3)
    logger.info("더미 Query(첫 번째 chunk 벡터) 기반 Top-3:")
    for r in ranked:
        logger.info(
            "  chunk_id=%s  score=%.4f  type=%s",
            r["chunk_id"], r["score"], r["document_type"],
        )

    ok = len(ranked) > 0 and ranked[0]["score"] > 0
    logger.info("DB Retrieval 검증: %s", "OK" if ok else "FAIL")
    return ok


def test_metadata_filter(logger: logging.Logger) -> bool:
    """Metadata 필터링 검증."""
    logger.info("--- Metadata 필터링 검증 ---")

    sample_results = [
        {
            "chunk_id": 1,
            "score": 0.95,
            "metadata_json": json.dumps({
                "source": "연합뉴스",
                "published_at": "2025-05-20",
            }),
        },
        {
            "chunk_id": 2,
            "score": 0.90,
            "metadata_json": json.dumps({
                "source": "조선일보",
                "published_at": "2025-05-18",
            }),
        },
        {
            "chunk_id": 3,
            "score": 0.85,
            "metadata_json": json.dumps({
                "source": "연합뉴스",
                "published_at": "2025-05-15",
            }),
        },
    ]

    filtered_source = filter_chunks_by_metadata(
        sample_results, {"source": "연합뉴스"},
    )
    logger.info("source='연합뉴스' 필터: %d건 (기대: 2)", len(filtered_source))

    filtered_date = filter_chunks_by_metadata(
        sample_results, {"published_at_from": "2025-05-18"},
    )
    logger.info("published_at >= 2025-05-18 필터: %d건 (기대: 2)", len(filtered_date))

    ok = len(filtered_source) == 2 and len(filtered_date) == 2
    logger.info("Metadata 필터링 검증: %s", "OK" if ok else "FAIL")
    return ok


def test_openai_retrieval(logger: logging.Logger) -> bool:
    """OpenAI API 기반 실제 Retrieval 테스트."""
    logger.info("--- OpenAI API Retrieval 검증 ---")

    query = SAMPLE_QUERIES[0]
    query_vec = generate_embedding(query)

    if not query_vec:
        logger.warning("OpenAI API 사용 불가 (쿼터 초과 등) — 건너뜀")
        return False

    logger.info("Query Embedding 성공  dim=%d", len(query_vec))

    results = retrieve_similar_chunks(
        query, top_k=3,
        filters={"ticker": "005930"},
        query_vec=query_vec,
    )

    logger.info("Retrieval 결과: %d건", len(results))
    for r in results:
        logger.info(
            "  chunk_id=%s  score=%.4f  type=%s  text=%s...",
            r["chunk_id"], r["score"], r["document_type"],
            r.get("chunk_text", "")[:40],
        )

    return len(results) > 0


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Retrieval 샘플 검증 시작 ===")

    results = {}

    # 1. Cosine Similarity 검증
    results["cosine"] = test_cosine_similarity(logger)

    # 2. rank_similar_chunks 검증
    results["rank"] = test_rank_similar(logger)

    # 3. Metadata 필터링 검증
    results["metadata"] = test_metadata_filter(logger)

    # 4. DB Retrieval 검증
    results["db_retrieval"] = test_db_retrieval(logger)

    # 5. OpenAI API Retrieval 검증
    results["openai"] = test_openai_retrieval(logger)

    # 요약
    logger.info("=== 검증 결과 요약 ===")
    for name, ok in results.items():
        status = "OK" if ok else "SKIP/FAIL"
        logger.info("  %-15s : %s", name, status)

    core_ok = results["cosine"] and results["rank"] and results["metadata"]
    logger.info(
        "핵심 검증: %s  |  DB: %s  |  OpenAI: %s",
        "OK" if core_ok else "FAIL",
        "OK" if results["db_retrieval"] else "SKIP",
        "OK" if results["openai"] else "SKIP",
    )
    logger.info("=== Retrieval 샘플 검증 완료 ===")

    return 0 if core_ok else 1


if __name__ == "__main__":
    sys.exit(main())
