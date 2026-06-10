"""회사명 · 질문 텍스트 → CompanyRecord 해석."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .alias_resolver import search_companies
from .company_registry import COMPANY_REGISTRY, CompanyRecord
from .corp_code_mapper import corp_code_for_ticker


@dataclass
class ResolvedCompany:
    company_name: str
    ticker: str
    corp_code: str
    market: str


def resolve_company(text: str) -> ResolvedCompany | None:
    """질문 또는 회사명에서 종목을 식별한다."""
    text = (text or "").strip()
    if not text:
        return None

    hits = search_companies(text, limit=5)
    if hits:
        return _to_resolved(_best_match(text, hits))

    for rec in COMPANY_REGISTRY:
        if rec["company_name"] in text:
            return _to_resolved(rec)

    ticker_match = re.search(r"\b(\d{6})\b", text)
    if ticker_match:
        ticker = ticker_match.group(1)
        from src.company_master.company_master_repository import get_by_ticker

        master = get_by_ticker(ticker)
        if master and master.get("corp_code"):
            return ResolvedCompany(
                company_name=master.get("company_name", ""),
                ticker=ticker,
                corp_code=master.get("corp_code", ""),
                market=master.get("market", "KOSPI"),
            )
        corp = corp_code_for_ticker(ticker)
        if corp:
            for rec in COMPANY_REGISTRY:
                if rec["ticker"] == ticker:
                    return _to_resolved(rec)

    return None


def _best_match(text: str, hits: list[CompanyRecord]) -> CompanyRecord:
    text_n = text.replace(" ", "")
    for rec in hits:
        if rec["company_name"] in text or rec["company_name"].replace(" ", "") in text_n:
            return rec
    return hits[0]


def _to_resolved(rec: CompanyRecord) -> ResolvedCompany:
    return ResolvedCompany(
        company_name=rec["company_name"],
        ticker=rec["ticker"],
        corp_code=rec["corp_code"],
        market=rec["market"],
    )
