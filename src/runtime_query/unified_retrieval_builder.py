"""Unified news + disclosure retrieval builder."""
from __future__ import annotations

import logging

from src.runtime_flow.retrieval_executor import execute_retrieval

from .disclosure_retrieval_ranker import rank_disclosure_chunks
from .runtime_evidence_merger import merge_runtime_evidence

logger = logging.getLogger(__name__)


def normalize_news_chunk(ch: dict) -> dict:
    return {
        **ch,
        "document_type": ch.get("document_type", "news_article"),
        "source": ch.get("source", "document_chunks"),
        "priority": "MEDIUM",
    }


def normalize_disclosure_chunk(ch: dict) -> dict:
    text = ch.get("chunk_text") or ch.get("text", "")
    return {
        **ch,
        "chunk_id": ch.get("chunk_id"),
        "document_type": "disclosure",
        "score": ch.get("rank_score") or ch.get("score", 0),
        "source": "disclosure_documents",
        "priority": "HIGH",
        "text": text,
        "chunk_text": text,
    }


def build_unified_retrieval(
    query: str,
    ticker: str,
    *,
    news_chunks: list[dict] | None = None,
    disclosure_chunks: list[dict] | None = None,
    news_top_k: int = 6,
    disclosure_top_k: int = 5,
) -> tuple[list[dict], list[dict], list[dict]]:
    """Returns (news, disclosure, merged) chunk lists."""
    news_source = (
        news_chunks
        if news_chunks is not None
        else execute_retrieval(
            query,
            ticker,
            top_k=news_top_k,
            document_type="news_article",
        )
    )
    news = [
        normalize_news_chunk(c)
        for c in news_source
    ]
    disc_raw = disclosure_chunks or []
    disc = [normalize_disclosure_chunk(c) for c in rank_disclosure_chunks(disc_raw)[:disclosure_top_k]]
    merged = merge_runtime_evidence(news, disc)
    logger.info(
        "unified_retrieval  ticker=%s  news=%d  disclosure=%d  merged=%d",
        ticker,
        len(news),
        len(disc),
        len(merged),
    )
    return news, disc, merged
