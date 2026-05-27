"""Stock Chain API 서비스."""
from __future__ import annotations

from .trace_service import (
    get_latest_unified_result,
    load_stock_chain_file,
    STOCK_CHAIN_DIR,
)
import json
from pathlib import Path


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
                chain = json.load(f)
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
        latest = fetch_latest_stock_chain()
        if latest and latest.get("ticker") == ticker:
            return latest
        return None

    return {
        "ticker": ticker,
        "chain_count": len(chains),
        "chains": chains,
    }
