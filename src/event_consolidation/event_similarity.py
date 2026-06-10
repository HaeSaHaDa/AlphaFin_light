"""Event similarity — title/body fuzzy match, ticker, date proximity."""
from __future__ import annotations

import re
from datetime import datetime
from difflib import SequenceMatcher


TITLE_THRESHOLD = 0.72
BODY_THRESHOLD = 0.68
DATE_PROXIMITY_DAYS = 3


def normalize_title(title: str) -> str:
    t = re.sub(r"[^\w\s가-힣]", " ", title or "")
    t = re.sub(r"\s+", " ", t.strip().lower())
    return t


def title_similarity(a: str, b: str) -> float:
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    if na in nb or nb in na:
        return 0.88
    return SequenceMatcher(None, na, nb).ratio()


def body_similarity(a: str, b: str) -> float:
    na, nb = normalize_title(a)[:500], normalize_title(b)[:500]
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    raw = str(value).strip()[:19]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y%m%d"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def dates_close(d1: datetime | None, d2: datetime | None, days: int = DATE_PROXIMITY_DAYS) -> bool:
    if not d1 or not d2:
        return True
    return abs((d1 - d2).days) <= days


def items_are_duplicate(
    a: dict,
    b: dict,
    *,
    title_threshold: float = TITLE_THRESHOLD,
) -> bool:
    if a.get("ticker") and b.get("ticker") and a["ticker"] != b["ticker"]:
        return False
    if a.get("url") and a.get("url") == b.get("url"):
        return True
    if a.get("source_id") and a.get("source_id") == b.get("source_id"):
        return True
    t_sim = title_similarity(a.get("title", ""), b.get("title", ""))
    if t_sim < title_threshold:
        return False
    b_sim = body_similarity(a.get("body", ""), b.get("body", ""))
    if a.get("body") and b.get("body") and b_sim < BODY_THRESHOLD:
        return False
    d1 = parse_date(a.get("published_at"))
    d2 = parse_date(b.get("published_at"))
    return dates_close(d1, d2)


def cluster_similarity(a: dict, b: dict) -> float:
    """Canonical event cluster merge score."""
    t = title_similarity(a.get("canonical_title", a.get("title", "")), b.get("title", ""))
    ticker_match = 1.0 if (not a.get("ticker") or not b.get("ticker") or a["ticker"] == b["ticker"]) else 0.0
    src_bonus = 0.12 if a.get("source_type") != b.get("source_type") else 0.0
    return min(1.0, t * 0.85 + ticker_match * 0.1 + src_bonus)
