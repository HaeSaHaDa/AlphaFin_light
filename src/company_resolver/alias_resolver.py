"""회사명 alias · 부분 검색."""
from __future__ import annotations

from .company_registry import COMPANY_REGISTRY, CompanyRecord


def _norm(text: str) -> str:
    return text.strip().lower().replace(" ", "")


def search_companies(query: str, limit: int = 10) -> list[CompanyRecord]:
    """부분 일치로 회사 목록을 반환한다."""
    q = _norm(query)
    if not q:
        return []

    hits: list[tuple[int, CompanyRecord]] = []
    for rec in COMPANY_REGISTRY:
        name = _norm(rec["company_name"])
        score = 0
        if q in name or name in q:
            score = 100
        elif any(q in _norm(a) or _norm(a) in q for a in rec["aliases"]):
            score = 80
        elif q[:2] in name:
            score = 40
        if score > 0:
            hits.append((score, rec))

    hits.sort(key=lambda x: -x[0])
    return [r for _, r in hits[:limit]]
