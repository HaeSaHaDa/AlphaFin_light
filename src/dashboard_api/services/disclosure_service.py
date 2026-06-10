"""Disclosure API service layer."""
from __future__ import annotations

from src.disclosure.dart_collector import collect_disclosures
from src.disclosure.disclosure_cache import (
    DISCLOSURE_BODY_CACHE_VERSION,
    get_disclosure_cache_status,
    has_fresh_body_cache,
    load_cache,
    save_cache,
)
from src.disclosure.disclosure_chunker import chunk_disclosure_documents
from src.disclosure.disclosure_embedder import embed_disclosure_chunks
from src.disclosure.disclosure_repository import (
    list_disclosures_by_ticker,
    list_timeline_events,
)
from src.disclosure.disclosure_retriever import retrieve_disclosure_chunks
from src.disclosure.disclosure_summary import build_disclosure_timeline

from .trace_service import get_unified_result_by_trace


def collect_disclosure_store(
    ticker: str,
    *,
    force: bool = False,
    days: int = 365,
    body_limit: int = 10,
) -> dict:
    cached = load_cache(ticker)
    cache_status = get_disclosure_cache_status(cached)
    if has_fresh_body_cache(cached) and not force:
        return {**cached, **cache_status, "status": "cached", "ticker": ticker}
    c = collect_disclosures(ticker, days=days, body_limit=body_limit)
    ch = chunk_disclosure_documents(ticker)
    emb = embed_disclosure_chunks(ticker)
    out = {
        "status": c.get("status", "completed"),
        "ticker": ticker,
        "fetched": c.get("fetched", 0),
        "upserted": c.get("upserted", 0),
        "body_fetched": c.get("body_fetched", 0),
        "body_failed": c.get("body_failed", 0),
        "body_chars": c.get("body_chars", 0),
        "chunks": ch.get("chunks", 0),
        "body_documents": ch.get("body_documents", 0),
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
    }


def fetch_disclosures(ticker: str) -> dict:
    docs = list_disclosures_by_ticker(ticker, limit=80)
    normalized = [
        {
            **doc,
            "report_date": str(doc["report_date"]) if doc.get("report_date") else None,
        }
        for doc in docs
    ]
    return {
        "ticker": ticker,
        "document_count": len(normalized),
        "documents": normalized,
    }


def search_disclosures(ticker: str, query: str, top_k: int = 8) -> dict:
    chunks = retrieve_disclosure_chunks(ticker, query, top_k=top_k)
    return {"ticker": ticker, "query": query, "top_k": top_k, "chunks": chunks}


def fetch_disclosure_timeline(ticker: str) -> dict:
    docs = list_timeline_events(ticker, limit=60)
    return {"ticker": ticker, "timeline": build_disclosure_timeline(docs, limit=30)}


def fetch_disclosure_evidence(trace_id: str) -> dict | None:
    result = get_unified_result_by_trace(trace_id)
    if not result:
        return None
    ticker = (result.get("ticker") or "").strip()
    query = result.get("query") or ""
    evidence = retrieve_disclosure_chunks(ticker, query, top_k=6)
    return {"trace_id": trace_id, "ticker": ticker, "query": query, "evidence": evidence}
