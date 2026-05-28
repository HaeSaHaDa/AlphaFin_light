"""Company search · resolve — company_master 기반."""
from __future__ import annotations

from src.company_master.company_master_repository import get_by_ticker
from src.company_master.company_search_service import search_companies_master
from src.company_master.ticker_selection_service import resolve_by_ticker
from src.company_resolver.company_resolver import resolve_company
from src.ingestion_pipeline.dart_ingestor import ingest_dart
from src.ingestion_pipeline.ticker_stats import fetch_recent_disclosures, get_ticker_stats


def search_company(q: str) -> list[dict]:
    results = search_companies_master(q, limit=15)
    return [
        {
            "company_name": r["company_name"],
            "ticker": r["ticker"],
            "corp_code": r.get("corp_code", ""),
            "market": r.get("market", "KOSPI"),
            "sector": r.get("sector", ""),
            "industry": r.get("industry", ""),
        }
        for r in results
    ]


def get_company_by_ticker(ticker: str) -> dict | None:
    row = get_by_ticker(ticker)
    if not row:
        return None
    return {
        "company_name": row["company_name"],
        "ticker": row["ticker"],
        "corp_code": row.get("corp_code", ""),
        "market": row.get("market", "KOSPI"),
        "sector": row.get("sector", ""),
        "industry": row.get("industry", ""),
        "aliases": row.get("aliases", []),
    }


def resolve_company_query(q: str, *, prefetch: bool = False, ticker: str | None = None) -> dict | None:
    if ticker:
        row = get_by_ticker(ticker)
        if not row:
            return None
    else:
        row = None
        sel = resolve_by_ticker(q) if len(q) == 6 and q.isdigit() else None
        if sel:
            row = get_by_ticker(sel.ticker)
        if not row:
            resolved = resolve_company(q)
            if resolved:
                row = get_by_ticker(resolved.ticker) or {
                    "company_name": resolved.company_name,
                    "ticker": resolved.ticker,
                    "corp_code": resolved.corp_code,
                    "market": resolved.market,
                    "sector": "",
                    "industry": "",
                }

    if not row:
        return None

    t = row["ticker"]
    stats = get_ticker_stats(t)
    if prefetch and stats["disclosure_count"] < 3 and row.get("corp_code"):
        try:
            ingest_dart(row["corp_code"], t)
            stats = get_ticker_stats(t)
        except Exception:
            pass

    return {
        "company_name": row["company_name"],
        "ticker": t,
        "corp_code": row.get("corp_code", ""),
        "market": row.get("market", ""),
        "sector": row.get("sector", ""),
        "industry": row.get("industry", ""),
        "stats": stats,
        "recent_disclosures": fetch_recent_disclosures(t, 8),
        "cache_ready": stats["embedding_count"] >= 3,
    }
