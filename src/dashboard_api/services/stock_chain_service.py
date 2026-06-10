"""Stock Chain API 서비스."""
from __future__ import annotations

from .trace_service import (
    get_latest_unified_result,
    load_stock_chain_file,
    STOCK_CHAIN_DIR,
)
import json
from pathlib import Path


def _event_graph_chain(chain: dict) -> dict:
    """과거 고정 규칙 링크를 제외하고 Runtime Event Graph 링크만 유지한다."""
    return {
        **chain,
        "links": [
            link
            for link in chain.get("links", [])
            if link.get("from_event_graph") is True
        ],
    }


def fetch_stock_chain_by_trace(trace_id: str) -> dict | None:
    from .ticker_centric_chain import build_ticker_centric_chain
    from .trace_service import get_unified_result_by_trace

    result = get_unified_result_by_trace(trace_id)
    if not result:
        return None
    chain_file = _event_graph_chain(load_stock_chain_file(trace_id) or {})
    ticker = (result.get("ticker") or "").strip()
    query = result.get("query") or ""
    from .retrieval_service import hydrate_retrieval_chunks

    chunks = hydrate_retrieval_chunks(result)

    centered = build_ticker_centric_chain(
        chain_file,
        ticker,
        query,
        retrieval_chunks=chunks,
    )
    return {
        "trace_id": trace_id,
        "query": query,
        "ticker": ticker,
        "center_name": centered.get("center_name", ""),
        "center_ticker": centered.get("center_ticker", ticker),
        "summary": result.get("stock_chain", {}),
        "chain": {
            "entities": centered["entities"],
            "links": centered["links"],
        },
    }


def fetch_latest_stock_chain() -> dict | None:
    result = get_latest_unified_result()
    if not result:
        return None
    trace_id = result.get("trace_id", "")
    chain = load_stock_chain_file(trace_id) or {}
    return {
        "trace_id": trace_id,
        "query": result.get("query", ""),
        "ticker": result.get("ticker", ""),
        "summary": result.get("stock_chain", {}),
        "chain": chain,
    }


def fetch_stock_chain_by_ticker(ticker: str) -> dict | None:
    chains: list[dict] = []
    if not STOCK_CHAIN_DIR.exists():
        return None

    for fp in STOCK_CHAIN_DIR.glob("*_chain.json"):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                chain = _event_graph_chain(json.load(f))
        except (json.JSONDecodeError, OSError):
            continue
        if chain.get("ticker") == ticker:
            chains.append(chain)
            continue
        for ent in chain.get("entities", []):
            if ent.get("ticker") == ticker:
                chains.append(chain)
                break

    if not chains:
        return None

    return {
        "ticker": ticker,
        "chain_count": len(chains),
        "chains": chains,
    }
