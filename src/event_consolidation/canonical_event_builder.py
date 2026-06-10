"""Canonical market event title/summary builder."""
from __future__ import annotations

import hashlib
import re

from .event_similarity import normalize_title, title_similarity


def make_event_id(ticker: str, canonical_title: str) -> str:
    raw = f"{ticker}:{normalize_title(canonical_title)}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    return f"evt_{digest}"


def normalize_canonical_title(title: str) -> str:
    t = re.sub(r"\s+", " ", (title or "").strip())
    t = re.sub(r"(추진|관련|보도|기사)\s*$", "", t).strip()
    return t[:200] if t else "시장 이벤트"


def build_canonical_title(cluster: list[dict], company_name: str = "") -> str:
    titles = [c.get("title", "") for c in cluster if c.get("title")]
    if not titles:
        return normalize_canonical_title(company_name or "시장 이벤트")

    base = max(titles, key=len)
    tokens: set[str] = set()
    for t in titles:
        for w in re.findall(r"[가-힣A-Za-z0-9]{2,}", t):
            if len(w) >= 2:
                tokens.add(w)

    core = normalize_canonical_title(base)
    prefix = (company_name or cluster[0].get("company_name") or "").strip()
    if prefix and prefix not in core:
        core = f"{prefix} {core}"
    return normalize_canonical_title(core)


def build_event_summary(cluster: list[dict], canonical_title: str) -> str:
    bodies = [c.get("body", "").strip() for c in cluster if c.get("body")]
    if bodies:
        body = bodies[0]
        if body == canonical_title:
            return canonical_title
        return f"{canonical_title} — {body}".strip()
    return canonical_title


def infer_event_type(cluster: list[dict]) -> str:
    text = " ".join(c.get("title", "") + " " + c.get("body", "")[:80] for c in cluster).lower()
    if any(k in text for k in ("투자", "증설", "capa", "생산")):
        return "investment"
    if any(k in text for k in ("실적", "매출", "영업이익")):
        return "earnings"
    if any(k in text for k in ("공시", "보고서")):
        return "disclosure"
    return "market_news"


def infer_impact_direction(cluster: list[dict]) -> str:
    text = " ".join(c.get("title", "") for c in cluster).lower()
    if any(k in text for k in ("확대", "증가", "호조", "성장")):
        return "positive"
    if any(k in text for k in ("감소", "하락", "우려", "리스크")):
        return "negative"
    return "neutral"


def merge_clusters(items: list[dict], threshold: float = 0.72) -> list[list[dict]]:
    """Group items into clusters by title similarity."""
    clusters: list[list[dict]] = []
    for item in sorted(items, key=lambda x: x.get("relevance_score", 0), reverse=True):
        placed = False
        for cluster in clusters:
            ref = {"canonical_title": build_canonical_title(cluster), "ticker": item.get("ticker")}
            if title_similarity(ref["canonical_title"], item.get("title", "")) >= threshold:
                cluster.append(item)
                placed = True
                break
        if not placed:
            clusters.append([item])
    return clusters
