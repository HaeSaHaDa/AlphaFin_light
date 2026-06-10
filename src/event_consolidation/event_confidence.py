"""Event-level confidence normalization."""
from __future__ import annotations

from datetime import datetime, timezone

from .event_similarity import parse_date

SOURCE_RELIABILITY = {
    "DISCLOSURE": 0.95,
    "NEWS": 0.75,
    "CHUNK": 0.7,
    "MEMORY": 0.65,
}


def compute_event_confidence(evidence: list[dict]) -> float:
    if not evidence:
        return 0.0

    scores = [float(e.get("relevance_score") or 0) for e in evidence]
    avg_rel = sum(scores) / len(scores) if scores else 0.0

    rel_w = min(1.0, avg_rel) * 0.45
    src_scores = [SOURCE_RELIABILITY.get(e.get("source_type", "CHUNK"), 0.7) for e in evidence]
    src_w = (sum(src_scores) / len(src_scores)) * 0.25
    count_w = min(len(evidence) * 0.04, 0.15)

    has_disclosure = any(e.get("source_type") == "DISCLOSURE" for e in evidence)
    disclosure_w = 0.12 if has_disclosure else 0.0

    now = datetime.now(timezone.utc)
    recency_vals: list[float] = []
    for e in evidence:
        dt = parse_date(e.get("published_at"))
        if not dt:
            recency_vals.append(0.5)
            continue
        days = max(0, (now - dt).days)
        recency_vals.append(max(0.2, 1.0 - days / 30.0))
    recency_w = (sum(recency_vals) / len(recency_vals)) * 0.13 if recency_vals else 0.05

    raw = rel_w + src_w + count_w + disclosure_w + recency_w
    return round(min(0.99, max(0.1, raw)), 4)
