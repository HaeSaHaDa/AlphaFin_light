"""Retrieval freshness scoring helpers."""
from __future__ import annotations

import json
import math
from datetime import datetime

NEWS_FRESHNESS_WEIGHT = 0.2
NEWS_FRESHNESS_HALF_LIFE_DAYS = 14


def parse_document_date(item: dict) -> datetime | None:
    metadata = item.get("metadata_json")
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except (json.JSONDecodeError, TypeError):
            metadata = {}
    if not isinstance(metadata, dict):
        metadata = {}

    raw = (
        item.get("published_at")
        or metadata.get("published_at")
        or item.get("report_date")
        or ""
    )
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        try:
            return datetime.strptime(str(raw)[:10], "%Y-%m-%d")
        except ValueError:
            return None


def freshness_score(
    item: dict,
    *,
    half_life_days: int = NEWS_FRESHNESS_HALF_LIFE_DAYS,
) -> float:
    published = parse_document_date(item)
    if not published:
        return 0.0
    age_days = max(0.0, (datetime.now() - published).total_seconds() / 86400)
    return round(math.pow(0.5, age_days / max(1, half_life_days)), 6)


def rank_with_freshness(
    results: list[dict],
    *,
    freshness_weight: float = NEWS_FRESHNESS_WEIGHT,
) -> list[dict]:
    ranked: list[dict] = []
    relevance_weight = 1.0 - freshness_weight
    for item in results:
        similarity = max(0.0, float(item.get("score") or 0.0))
        fresh = freshness_score(item)
        combined = relevance_weight * similarity + freshness_weight * fresh
        ranked.append(
            {
                **item,
                "similarity_score": round(similarity, 6),
                "freshness_score": fresh,
                "score": round(min(1.0, combined), 6),
            },
        )
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked
