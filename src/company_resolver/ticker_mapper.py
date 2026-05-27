"""ticker 매핑."""
from __future__ import annotations

from .company_registry import COMPANY_REGISTRY


def ticker_for_name(company_name: str) -> str | None:
    name = company_name.strip()
    for rec in COMPANY_REGISTRY:
        if rec["company_name"] == name:
            return rec["ticker"]
    return None
