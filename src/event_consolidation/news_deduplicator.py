"""News deduplication — title/url/ticker proximity."""
from __future__ import annotations

from .event_similarity import items_are_duplicate


def deduplicate_news(items: list[dict]) -> list[dict]:
    """Remove duplicate news items; keep highest relevance per cluster."""
    news = [i for i in items if i.get("source_type") in ("NEWS", "CHUNK") and i.get("document_type", "news_article") != "disclosure"]
    if not news:
        news = [i for i in items if i.get("source_type") == "NEWS"]
    kept: list[dict] = []
    for item in sorted(news, key=lambda x: x.get("relevance_score", 0), reverse=True):
        if any(items_are_duplicate(item, k) for k in kept):
            continue
        kept.append(item)
    return kept
