"""Event memory layer — active uniqueness and promotion lifecycle."""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from .event_importance import compute_event_importance
from .event_repository import set_memory_layer
from .event_similarity import title_similarity

logger = logging.getLogger(__name__)

LAYER_MAP = {
    "short_term": "SHORT",
    "mid_term": "MID",
    "long_term": "LONG",
}


def _memory_title(item: dict) -> str:
    return (
        item.get("event_title")
        or item.get("summary")
        or item.get("query")
        or ""
    ).strip()


def assign_memory_layers(
    events: list[dict],
    layered_memory: dict[str, list[dict]],
    *,
    persist: bool = True,
) -> list[dict]:
    """Map canonical events to memory layers; ensure one active layer per event."""
    event_by_title: list[tuple[dict, str]] = [
        (e, e.get("canonical_title", "")) for e in events
    ]
    layers_out: list[dict] = []

    for json_layer, db_layer in LAYER_MAP.items():
        for mem in layered_memory.get(json_layer) or []:
            if not isinstance(mem, dict):
                continue
            mt = _memory_title(mem)
            if not mt:
                continue
            matched = None
            best_sim = 0.0
            for ev, ct in event_by_title:
                sim = title_similarity(ct, mt)
                if sim > best_sim and sim >= 0.55:
                    best_sim = sim
                    matched = ev
            if not matched:
                continue
            imp = compute_event_importance(
                matched.get("evidence") or [],
                confidence=matched.get("confidence_score"),
                memory_layer=db_layer,
            )
            layer_row = {
                "event_id": matched["event_id"],
                "memory_layer": db_layer,
                "entered_at": mem.get("timestamp") or datetime.now(timezone.utc).isoformat(),
                "promoted_from": mem.get("promoted_from"),
                "importance_score": imp,
                "is_active": True,
                "canonical_title": matched.get("canonical_title"),
            }
            layers_out.append(layer_row)
            if persist:
                promoted_from = None
                action = mem.get("retention_action") or ""
                if action == "promote" and json_layer == "mid_term":
                    promoted_from = "SHORT"
                set_memory_layer(
                    matched["event_id"],
                    db_layer,
                    promoted_from=promoted_from,
                    importance_score=imp,
                    deactivate_others=True,
                )
                logger.info(
                    "memory layer assigned  event=%s  layer=%s  promoted_from=%s",
                    matched["event_id"],
                    db_layer,
                    promoted_from,
                )

    return dedupe_active_layers(layers_out)


def dedupe_active_layers(layers: list[dict]) -> list[dict]:
    """Keep only highest layer active per event_id in API payload."""
    priority = {"LONG": 3, "MID": 2, "SHORT": 1}
    best: dict[str, dict] = {}
    for row in layers:
        eid = row["event_id"]
        cur = best.get(eid)
        if not cur or priority.get(row["memory_layer"], 0) >= priority.get(cur["memory_layer"], 0):
            best[eid] = row
    out = list(best.values())
    for row in out:
        row["is_active"] = True
    return out


def promote_event_memory(event_id: str, to_layer: str, *, from_layer: str | None = None) -> None:
    set_memory_layer(
        event_id,
        to_layer,
        promoted_from=from_layer,
        deactivate_others=True,
    )
    logger.info("promoted event memory  %s  %s -> %s", event_id, from_layer, to_layer)


def deactivate_previous_layer(event_id: str) -> None:
    set_memory_layer(event_id, "SHORT", deactivate_others=True)
