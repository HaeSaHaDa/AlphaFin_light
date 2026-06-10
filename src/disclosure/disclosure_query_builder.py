"""Disclosure query helpers."""
from __future__ import annotations

from .disclosure_repository import list_disclosure_chunks


def build_disclosure_search_query(company_name: str, keywords: list[str]) -> str:
    parts = [company_name.strip()] + [k.strip() for k in keywords if k.strip()]
    return " ".join([p for p in parts if p])


def classify_report_type(report_name: str) -> tuple[str, str]:
    name = (report_name or "").strip()
    low = name.lower()
    if "사업보고서" in name:
        return ("BUSINESS_REPORT", "BUSINESS_REPORT")
    if "분기보고서" in name or "반기보고서" in name:
        return ("QUARTER_REPORT", "QUARTER_REPORT")
    if "실적" in name or "잠정" in name:
        return ("EARNINGS", "EARNINGS")
    if "ir" in low:
        return ("IR", "IR")
    return ("MAJOR_ISSUE", "MAJOR_ISSUE")


def build_section_name(text: str, default: str = "general") -> str:
    t = (text or "").strip()
    for key in ("CAPEX", "투자", "리스크", "매출", "실적", "사업"):
        if key.lower() in t.lower():
            return key.lower()
    return default


def pick_retrieval_candidates(ticker: str) -> list[dict]:
    return list_disclosure_chunks(ticker, limit=400)
