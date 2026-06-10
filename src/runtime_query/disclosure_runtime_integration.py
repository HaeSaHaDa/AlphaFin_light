"""runQuery disclosure collect + retrieval integration."""
from __future__ import annotations

import logging

from src.disclosure.disclosure_cache import (
    DISCLOSURE_BODY_CACHE_VERSION,
    get_disclosure_cache_status,
    has_fresh_body_cache,
    load_cache,
)
from src.disclosure.disclosure_repository import get_latest_disclosure_report_date
from src.disclosure.disclosure_retriever import retrieve_disclosure_chunks

from .disclosure_retrieval_ranker import rank_disclosure_chunks
from .disclosure_timeout_guard import run_with_timeout

logger = logging.getLogger(__name__)


def prefetch_disclosure_collect(ticker: str, *, force: bool = False) -> dict:
    """Warm disclosure store on runQuery (cache-aware)."""
    cached = load_cache(ticker)
    cache_status = get_disclosure_cache_status(cached)
    if has_fresh_body_cache(cached) and not force:
        logger.info("disclosure collect cache hit  ticker=%s", ticker)
        return {
            **cached,
            **cache_status,
            "status": "cached",
            "ticker": ticker,
            "data_as_of": get_latest_disclosure_report_date(ticker),
        }

    def _collect() -> dict:
        from src.disclosure.dart_collector import collect_disclosures
        from src.disclosure.disclosure_chunker import chunk_disclosure_documents
        from src.disclosure.disclosure_embedder import embed_disclosure_chunks
        from src.disclosure.disclosure_cache import save_cache

        c = collect_disclosures(ticker, days=365, body_limit=1)
        ch = chunk_disclosure_documents(ticker)
        emb = embed_disclosure_chunks(ticker)
        out = {
            "status": c.get("status", "completed"),
            "fetched": c.get("fetched", 0),
            "body_fetched": c.get("body_fetched", 0),
            "chunks": ch.get("chunks", 0),
            "embedded": emb.get("embedded", 0),
            "body_cache_version": DISCLOSURE_BODY_CACHE_VERSION,
        }
        saved = save_cache(ticker, out)
        return {
            **saved,
            "cache_status": "REFRESHED",
            "cache_fresh": True,
            "cache_ttl_hours": cache_status["cache_ttl_hours"],
            "cache_updated_at": saved["updated_at"],
            "data_as_of": get_latest_disclosure_report_date(ticker),
        }

    result = run_with_timeout(
        _collect,
        timeout_sec=12.0,
        fallback={"status": "timeout", "ticker": ticker},
        label="disclosure_collect",
    )
    return result or {"status": "failed", "ticker": ticker}


def retrieve_disclosure_runtime(
    ticker: str,
    query: str,
    *,
    top_k: int = 5,
) -> list[dict]:
    if not ticker or not query:
        return []

    def _retrieve() -> list[dict]:
        return retrieve_disclosure_chunks(ticker, query, top_k=top_k)

    chunks = run_with_timeout(
        _retrieve,
        timeout_sec=8.0,
        fallback=[],
        label="disclosure_retrieval",
    )
    return rank_disclosure_chunks(chunks or [])


def integrate_disclosure_runtime(ticker: str, query: str) -> dict:
    """Collect prefetch + retrieval for selectedTicker."""
    collect = prefetch_disclosure_collect(ticker)
    chunks = retrieve_disclosure_runtime(ticker, query)
    return {
        "ticker": ticker,
        "collect_status": collect.get("status", "unknown"),
        "collect": collect,
        "disclosure_chunk_count": len(chunks),
        "disclosure_chunks": chunks,
    }
