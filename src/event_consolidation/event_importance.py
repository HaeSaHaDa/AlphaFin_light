"""Event importance score for memory promotion."""
from __future__ import annotations

from .event_confidence import compute_event_confidence


def compute_event_importance(
    evidence: list[dict],
    *,
    confidence: float | None = None,
    memory_layer: str | None = None,
) -> float:
    conf = confidence if confidence is not None else compute_event_confidence(evidence)
    layer_boost = {"LONG": 0.15, "MID": 0.08, "SHORT": 0.0}.get(memory_layer or "SHORT", 0.0)
    disclosure_boost = 0.1 if any(e.get("source_type") == "DISCLOSURE" for e in evidence) else 0.0
    count_boost = min(len(evidence) * 0.03, 0.12)
    raw = conf * 0.7 + layer_boost + disclosure_boost + count_boost
    return round(min(1.0, max(0.1, raw)), 4)
