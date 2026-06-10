"""DB 기반 vector retrieval 실행."""
from __future__ import annotations

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

RETRIEVAL_DIR = Path(__file__).resolve().parents[1] / "rag" / "retrieval"


def execute_retrieval(
    query: str,
    ticker: str,
    *,
    top_k: int = 8,
    document_type: str | None = None,
    max_age_days: int | None = None,
) -> list[dict]:
    """ticker 필터로 DB embedding 유사도 검색."""
    rdir = str(RETRIEVAL_DIR)
    if rdir not in sys.path:
        sys.path.insert(0, rdir)

    from retriever import retrieve_similar_chunks  # type: ignore[import]

    filters = {"ticker": ticker}
    if document_type:
        filters["document_type"] = document_type
    if document_type == "news_article":
        age_days = max_age_days if max_age_days is not None else 90
        filters["published_at_from"] = (
            datetime.now() - timedelta(days=age_days)
        ).strftime("%Y-%m-%d")

    chunks = retrieve_similar_chunks(
        query,
        top_k=top_k,
        filters=filters,
    )
    logger.info(
        "execute_retrieval  query=%s  ticker=%s  type=%s  hits=%d",
        query[:40], ticker, document_type or "all", len(chunks),
    )
    return chunks
