"""Memory API 서비스 — trace·ticker 기준 필터."""
from __future__ import annotations

from .trace_service import (
    get_latest_unified_result,
    get_unified_result_by_trace,
    load_layer_memories,
)


def _memory_matches(item: dict, query: str, ticker: str) -> bool:
    q = (item.get("query") or "").strip()
    if query and q == query.strip():
        return True
    if ticker:
        for ch in item.get("referenced_chunks") or []:
            if isinstance(ch, dict) and ch.get("ticker") == ticker:
                return True
        if ticker in q:
            return True
    return False


def _layers_for_trace(result: dict) -> dict[str, list]:
    query = (result.get("query") or "").strip()
    ticker = (result.get("ticker") or "").strip()

    trace_short: list[dict] = []
    mem_up = result.get("memory_updates") or {}
    analysis_mem = mem_up.get("analysis_memory")
    if isinstance(analysis_mem, dict):
        trace_short.append(analysis_mem)

    layers = {
        "short_term": list(trace_short),
        "mid_term": [],
        "long_term": [],
    }

    for layer in ("short_term", "mid_term", "long_term"):
        for item in load_layer_memories(layer):
            if not isinstance(item, dict):
                continue
            if _memory_matches(item, query, ticker):
                if layer == "short_term" and item in layers["short_term"]:
                    continue
                layers[layer].append(item)

    if not layers["short_term"] and trace_short:
        layers["short_term"] = trace_short

    return layers


def _build_memory_payload(result: dict, trace_id: str) -> dict:
    layers = _layers_for_trace(result)
    return {
        "trace_id": trace_id,
        "query": result.get("query", ""),
        "ticker": result.get("ticker", ""),
        "memory_updates": result.get("memory_updates", {}),
        "temporal_result": result.get("temporal_result", {}),
        "layered_memory": layers,
        "layer_counts": {k: len(v) for k, v in layers.items()},
    }


def fetch_latest_memory() -> dict | None:
    result = get_latest_unified_result()
    if not result:
        return None
    trace_id = result.get("trace_id", "")
    return _build_memory_payload(result, trace_id)


def fetch_memory_by_trace(trace_id: str) -> dict | None:
    result = get_unified_result_by_trace(trace_id)
    if not result:
        return None
    return _build_memory_payload(result, trace_id)


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
