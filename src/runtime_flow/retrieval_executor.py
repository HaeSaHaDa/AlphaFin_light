"""DB 기반 vector retrieval 실행."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

RETRIEVAL_DIR = Path(__file__).resolve().parents[1] / "rag" / "retrieval"


def execute_retrieval(
    query: str,
    ticker: str,
    *,
    top_k: int = 8,
) -> list[dict]:
    """ticker 필터로 DB embedding 유사도 검색."""
    rdir = str(RETRIEVAL_DIR)
    if rdir not in sys.path:
        sys.path.insert(0, rdir)

    from retriever import retrieve_similar_chunks  # type: ignore[import]

    chunks = retrieve_similar_chunks(
        query,
        top_k=top_k,
        filters={"ticker": ticker},
    )
    logger.info(
        "execute_retrieval  query=%s  ticker=%s  hits=%d",
        query[:40], ticker, len(chunks),
    )
    return chunks
