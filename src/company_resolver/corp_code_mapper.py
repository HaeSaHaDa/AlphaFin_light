"""OpenDART corp_code 매핑."""
from __future__ import annotations

from .company_registry import COMPANY_REGISTRY


def corp_code_for_ticker(ticker: str) -> str | None:
    for rec in COMPANY_REGISTRY:
        if rec["ticker"] == ticker:
            return rec["corp_code"]
    return None
