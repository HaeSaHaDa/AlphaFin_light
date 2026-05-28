"""정확 일치 우선 종목 검색 (삼성전자/삼성전기 분리)."""
from __future__ import annotations

import json
import logging
import re

from .company_master_repository import get_by_ticker, list_all

logger = logging.getLogger(__name__)


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", (text or "").strip().lower())


def _parse_aliases(raw) -> list[str]:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return []
    return []


def _score_row(q: str, row: dict) -> int:
    ticker = row.get("ticker", "")
    name = _norm(row.get("company_name", ""))
    qn = _norm(q)

    if not qn:
        return 0

    # ticker 정확·접두
    if qn == ticker or qn == ticker.lstrip("0"):
        return 200
    if ticker.startswith(qn) and len(qn) >= 4:
        return 190

    # 회사명 정확 일치 (최우선 — 삼성전기 vs 삼성전자)
    if qn == name:
        return 180

    for alias in _parse_aliases(row.get("aliases")):
        an = _norm(alias)
        if qn == an:
            return 170
        if name.startswith(qn) and len(qn) >= len(name) - 1:
            pass

    # 시작 일치 (삼성전 → 삼성전기, 삼성전자 각각 별도 점수)
    if name.startswith(qn) and len(qn) >= 2:
        # 긴 일치 우선: query가 name의 prefix일 때 name 길이 반영
        return 120 + min(len(qn), 20)

    for alias in _parse_aliases(row.get("aliases")):
        an = _norm(alias)
        if an.startswith(qn) and len(qn) >= 2:
            return 110 + min(len(qn), 15)

    # 부분 포함 — 낮은 점수, 짧은 query는 제외해 오매칭 완화
    if len(qn) >= 3 and qn in name:
        return 60

    return 0


def search_companies_master(query: str, limit: int = 10) -> list[dict]:
    """자동완성용 검색 — 점수순, 동점이면 이름순."""
    q = (query or "").strip()
    if not q:
        return []

    if re.fullmatch(r"\d{6}", q):
        row = get_by_ticker(q)
        return [row] if row else []

    rows = list_all(limit=500)
    if not rows:
        from .kospi200_loader import load_kospi200_companies
        load_kospi200_companies(sync_companies_table=False)
        rows = list_all(limit=500)

    hits: list[tuple[int, str, dict]] = []
    for row in rows:
        score = _score_row(q, row)
        if score > 0:
            hits.append((score, row["company_name"], row))

    hits.sort(key=lambda x: (-x[0], x[1]))
    result = [h[2] for h in hits[:limit]]
    logger.info("search_companies_master  q=%s  hits=%d", q, len(result))
    return result
