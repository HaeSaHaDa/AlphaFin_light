"""Disclosure chunk ranking — priority, freshness, relevance."""
from __future__ import annotations

import math
from datetime import datetime

SOURCE_PRIORITY = {
    "DISCLOSURE": 1.0,
    "EARNINGS": 0.95,
    "BUSINESS_REPORT": 0.92,
    "QUARTERLY": 0.9,
    "NEWS": 0.65,
    "CHUNK": 0.6,
    "SOCIAL": 0.35,
}


def _report_priority(report_type: str) -> float:
    rt = (report_type or "").upper()
    if "EARNINGS" in rt or "실적" in rt:
        return SOURCE_PRIORITY["EARNINGS"]
    if "BUSINESS" in rt or "사업" in rt:
        return SOURCE_PRIORITY["BUSINESS_REPORT"]
    if "QUARTER" in rt or "분기" in rt:
        return SOURCE_PRIORITY["QUARTERLY"]
    return SOURCE_PRIORITY["DISCLOSURE"]


def _freshness_boost(report_date: str | None) -> float:
    if not report_date:
        return 0.5
    try:
        raw = str(report_date)[:10]
        dt = datetime.strptime(raw, "%Y-%m-%d")
        days = max(0, (datetime.now() - dt).days)
        return math.pow(0.5, days / 90.0)
    except ValueError:
        return 0.5


def rank_disclosure_chunk(chunk: dict) -> float:
    base = float(chunk.get("score") or 0)
    imp = float(chunk.get("importance_score") or 0.5)
    pri = _report_priority(chunk.get("report_type", ""))
    fresh = _freshness_boost(chunk.get("report_date"))
    return round(min(1.0, base * 0.4 + pri * 0.25 + imp * 0.15 + fresh * 0.2), 4)


def rank_disclosure_chunks(chunks: list[dict]) -> list[dict]:
    ranked = []
    for ch in chunks:
        score = rank_disclosure_chunk(ch)
        ranked.append({
            **ch,
            "similarity_score": float(ch.get("score") or 0),
            "freshness_score": round(_freshness_boost(ch.get("report_date")), 4),
            "rank_score": score,
            "priority": "HIGH",
        })
    ranked.sort(key=lambda x: x.get("rank_score", 0), reverse=True)
    return ranked
