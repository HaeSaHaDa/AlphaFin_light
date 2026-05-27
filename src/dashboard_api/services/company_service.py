"""Company search API 서비스."""
from __future__ import annotations

from src.company_resolver.alias_resolver import search_companies


def search_company(q: str) -> list[dict]:
    results = search_companies(q, limit=10)
    return [
        {
            "company_name": r["company_name"],
            "ticker": r["ticker"],
            "corp_code": r["corp_code"],
            "market": r["market"],
        }
        for r in results
    ]
