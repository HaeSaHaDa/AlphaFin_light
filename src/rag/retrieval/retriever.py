"""Query 기반 Chunk Retrieval 모듈."""
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
from embedder import generate_embedding, DEFAULT_MODEL  # noqa: E402
from similarity import cosine_similarity, rank_similar_chunks  # noqa: E402
from freshness import rank_with_freshness  # noqa: E402

logger = logging.getLogger(__name__)


def generate_query_embedding(
    query: str,
    model: str = DEFAULT_MODEL,
) -> list[float]:
    """사용자 Query를 Embedding 벡터로 변환한다.

    Args:
        query: 검색 질문 텍스트.
        model: Embedding 모델명.

    Returns:
        float 리스트 (벡터). 실패 시 빈 리스트.
    """
    logger.info("Query Embedding 생성  query='%s'  model=%s", query[:50], model)
    vec = generate_embedding(query, model)
    if vec:
        logger.info("Query Embedding 성공  dim=%d", len(vec))
    else:
        logger.error("Query Embedding 실패")
    return vec


def fetch_embeddings_from_db(
    filters: dict | None = None,
) -> list[dict]:
    """document_embeddings + document_chunks 조인 데이터를 조회한다.

    Args:
        filters: 선택적 필터.
            - ticker: 종목코드
            - document_type: 문서유형 (news_article, disclosure)

    Returns:
        [{"chunk_id", "embedding_vector", "chunk_text",
          "ticker", "document_type", "metadata_json", ...}, ...]
    """
    where_clauses = []
    params: list = []

    if filters:
        if filters.get("ticker"):
            where_clauses.append("dc.ticker = %s")
            params.append(filters["ticker"])
        if filters.get("document_type"):
            where_clauses.append("dc.document_type = %s")
            params.append(filters["document_type"])

    where_sql = ""
    if where_clauses:
        where_sql = "AND " + " AND ".join(where_clauses)

    sql = f"""
        SELECT
            de.chunk_id,
            de.embedding_model,
            de.embedding_dimension,
            de.embedding_vector,
            dc.chunk_text,
            dc.chunk_length,
            dc.ticker,
            dc.document_type,
            dc.source_table,
            dc.source_id,
            dc.chunk_index,
            dc.metadata_json
        FROM document_embeddings de
        JOIN document_chunks dc ON de.chunk_id = dc.id
        WHERE 1=1 {where_sql}
        ORDER BY de.chunk_id
    """

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        results = []
        for row in rows:
            vec_raw = row["embedding_vector"]
            if isinstance(vec_raw, str):
                vec_raw = json.loads(vec_raw)
            row["embedding_vector"] = vec_raw
            results.append(row)

        logger.info("DB Embedding 조회  %d건  filters=%s", len(results), filters)
        return results
    except Exception:
        logger.exception("DB Embedding 조회 실패")
        return []
    finally:
        conn.close()


def filter_chunks_by_metadata(
    results: list[dict],
    filters: dict | None = None,
) -> list[dict]:
    """Retrieval 결과를 Metadata 기반으로 추가 필터링한다.

    metadata_json 내부 필드(source, published_at 등)를 기준으로 필터링한다.

    Args:
        results: Retrieval 결과 목록.
        filters: 필터 조건.
            - source: 언론사/데이터 소스
            - published_at_from: 시작일 (문자열 YYYY-MM-DD)
            - published_at_to: 종료일 (문자열 YYYY-MM-DD)

    Returns:
        필터링된 결과 목록.
    """
    if not filters:
        return results

    source_filter = filters.get("source")
    date_from = filters.get("published_at_from")
    date_to = filters.get("published_at_to")

    if not source_filter and not date_from and not date_to:
        return results

    filtered = []
    for item in results:
        meta_raw = item.get("metadata_json")
        if isinstance(meta_raw, str):
            try:
                meta = json.loads(meta_raw)
            except (json.JSONDecodeError, TypeError):
                meta = {}
        elif isinstance(meta_raw, dict):
            meta = meta_raw
        else:
            meta = {}

        if source_filter and meta.get("source") != source_filter:
            continue

        pub = meta.get("published_at", "")
        if date_from and (not pub or pub < date_from):
            continue
        if date_to and pub and pub > date_to:
            continue

        filtered.append(item)

    logger.info(
        "Metadata 필터링  before=%d  after=%d  filters=%s",
        len(results), len(filtered), filters,
    )
    return filtered


def retrieve_similar_chunks(
    query: str,
    top_k: int = 5,
    filters: dict | None = None,
    query_vec: list[float] | None = None,
) -> list[dict]:
    """Query와 유사한 Chunk를 검색하여 반환한다.

    Args:
        query: 검색 질문 텍스트.
        top_k: 반환할 상위 결과 수.
        filters: DB 필터 (ticker, document_type) +
                 Metadata 필터 (source, published_at_from/to).
        query_vec: 미리 생성된 Query 벡터. None이면 자동 생성.

    Returns:
        유사도 순으로 정렬된 결과 목록.
        [{"chunk_id", "score", "chunk_text", "ticker",
          "document_type", "metadata_json", ...}, ...]
    """
    logger.info(
        "retrieve_similar_chunks  query='%s'  top_k=%d  filters=%s",
        query[:50], top_k, filters,
    )

    if query_vec is None:
        query_vec = generate_query_embedding(query)
    if not query_vec:
        logger.error("Query Embedding 생성 실패 — 검색 중단")
        return []

    db_filters = {}
    meta_filters = {}
    if filters:
        if filters.get("ticker"):
            db_filters["ticker"] = filters["ticker"]
        if filters.get("document_type"):
            db_filters["document_type"] = filters["document_type"]
        if filters.get("source"):
            meta_filters["source"] = filters["source"]
        if filters.get("published_at_from"):
            meta_filters["published_at_from"] = filters["published_at_from"]
        if filters.get("published_at_to"):
            meta_filters["published_at_to"] = filters["published_at_to"]

    embeddings = fetch_embeddings_from_db(db_filters if db_filters else None)
    if not embeddings:
        logger.warning("DB에 Embedding 데이터 없음")
        return []

    ranked = rank_similar_chunks(query_vec, embeddings, top_k=len(embeddings))

    if meta_filters:
        ranked = filter_chunks_by_metadata(ranked, meta_filters)

    if (db_filters.get("document_type") or "") == "news_article":
        ranked = rank_with_freshness(ranked)

    results = ranked[:top_k]

    for r in results:
        r.pop("embedding_vector", None)

    logger.info(
        "Retrieval 완료  결과=%d건  최고score=%.4f",
        len(results),
        results[0]["score"] if results else 0.0,
    )
    return results
