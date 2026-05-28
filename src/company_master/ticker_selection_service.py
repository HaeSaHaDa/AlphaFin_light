"""확정 ticker → ResolvedCompany."""
from __future__ import annotations

from dataclasses import dataclass

from src.company_resolver.company_resolver import ResolvedCompany

from .company_master_repository import get_by_ticker
from .company_search_service import search_companies_master


@dataclass
class SelectedCompany:
    ticker: str
    company_name: str
    corp_code: str
    market: str
    sector: str = ""
    industry: str = ""


def resolve_by_ticker(ticker: str) -> SelectedCompany | None:
    row = get_by_ticker(ticker)
    if not row:
        return None
    return SelectedCompany(
        ticker=row["ticker"],
        company_name=row["company_name"],
        corp_code=row.get("corp_code") or "",
        market=row.get("market") or "KOSPI",
        sector=row.get("sector") or "",
        industry=row.get("industry") or "",
    )


def to_resolved_company(sel: SelectedCompany) -> ResolvedCompany:
    return ResolvedCompany(
        company_name=sel.company_name,
        ticker=sel.ticker,
        corp_code=sel.corp_code,
        market=sel.market,
    )


def pick_best_from_query(query: str) -> SelectedCompany | None:
    """자동 선택 금지 권장 — 검색 결과 1건만 있고 정확 일치일 때만."""
    hits = search_companies_master(query, limit=3)
    if len(hits) != 1:
        return None
    row = hits[0]
    return SelectedCompany(
        ticker=row["ticker"],
        company_name=row["company_name"],
        corp_code=row.get("corp_code") or "",
        market=row.get("market") or "KOSPI",
        sector=row.get("sector") or "",
        industry=row.get("industry") or "",
    )
