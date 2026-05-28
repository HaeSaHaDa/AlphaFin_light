"""ticker + company + topic keywords → runtime query."""
from __future__ import annotations


def build_runtime_query(
    company_name: str,
    ticker: str,
    keywords: list[str] | str,
) -> str:
    """Retrieval·Engine에 넘길 통합 query 문자열."""
    if isinstance(keywords, str):
        kw_list = [k.strip() for k in keywords.split() if k.strip()]
    else:
        kw_list = [k.strip() for k in keywords if k and str(k).strip()]

    parts = [company_name, ticker] + kw_list
    return " ".join(parts)


def build_news_search_keyword(company_name: str, keywords: list[str]) -> str:
    base = company_name
    if keywords:
        return f"{base} {' '.join(keywords[:3])}"
    return base
