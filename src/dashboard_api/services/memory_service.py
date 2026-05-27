"""Memory API 서비스."""
from __future__ import annotations

from .trace_service import (
    get_latest_unified_result,
    load_layer_memories,
)


def fetch_latest_memory() -> dict | None:
    result = get_latest_unified_result()
    if not result:
        return None

    layers = {
        "short_term": load_layer_memories("short_term"),
        "mid_term": load_layer_memories("mid_term"),
        "long_term": load_layer_memories("long_term"),
    }

    return {
        "trace_id": result.get("trace_id", ""),
        "query": result.get("query", ""),
        "memory_updates": result.get("memory_updates", {}),
        "temporal_result": result.get("temporal_result", {}),
        "layered_memory": layers,
        "layer_counts": {k: len(v) for k, v in layers.items()},
    }


def fetch_memory_by_layer(layer: str) -> dict | None:
    valid = {"short_term", "mid_term", "long_term"}
    if layer not in valid:
        return None
    memories = load_layer_memories(layer)
    return {
        "layer": layer,
        "memory_count": len(memories),
        "memories": memories[:20],
    }
