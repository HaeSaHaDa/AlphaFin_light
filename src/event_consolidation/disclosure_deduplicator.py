"""Disclosure deduplication — receipt/title/date."""
from __future__ import annotations

from .event_similarity import items_are_duplicate, title_similarity


def deduplicate_disclosures(items: list[dict]) -> list[dict]:
    disc = [
        i
        for i in items
        if i.get("source_type") == "DISCLOSURE"
        or i.get("document_type") == "disclosure"
    ]
    kept: list[dict] = []
    for item in sorted(disc, key=lambda x: x.get("relevance_score", 0), reverse=True):
        dup = False
        for k in kept:
            if items_are_duplicate(item, k):
                dup = True
                break
            if title_similarity(item.get("title", ""), k.get("title", "")) > 0.9:
                dup = True
                break
        if not dup:
            kept.append(item)
    return kept
