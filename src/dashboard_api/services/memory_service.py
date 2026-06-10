"""Memory API 서비스 — trace·ticker 기준 필터."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from .trace_service import (
    get_latest_unified_result,
    get_unified_result_by_trace,
    load_layer_memories,
)
from .retrieval_service import hydrate_retrieval_chunks

logger = logging.getLogger(__name__)

_LAYERED_DIR = Path(__file__).resolve().parents[2] / "rag" / "layered_memory"
if str(_LAYERED_DIR) not in sys.path:
    sys.path.insert(0, str(_LAYERED_DIR))

from layered_store import (  # noqa: E402
    collapse_layers_for_display,
    repair_layer_duplicates,
)


def _selected_company(query: str, ticker: str) -> str:
    if not query or not ticker or ticker not in query:
        return ""
    company_prefix = query.split(ticker, 1)[0].strip()
    return company_prefix.split()[-1] if company_prefix else ""


def _matches_company_context(item: dict, company: str, ticker: str) -> bool:
    if not company:
        return True
    text = " ".join(
        str(item.get(key) or "")
        for key in ("query", "summary", "event_name", "event_summary")
    )
    return company in text or ticker in text


def _memory_matches(item: dict, query: str, ticker: str) -> bool:
    q = (item.get("query") or "").strip()
    if not ticker:
        return bool(query and q == query.strip())

    company = _selected_company(query, ticker)
    explicit_ticker = (item.get("ticker") or "").strip()
    if explicit_ticker:
        return (
            explicit_ticker == ticker
            and _matches_company_context(item, company, ticker)
        )

    referenced_tickers = {
        str(ch.get("ticker") or "").strip()
        for ch in item.get("referenced_chunks") or []
        if isinstance(ch, dict) and ch.get("ticker")
    }
    if referenced_tickers:
        return (
            referenced_tickers == {ticker}
            and _matches_company_context(item, company, ticker)
        )

    return ticker in q and _matches_company_context(item, company, ticker)


def _layers_for_trace(result: dict) -> dict[str, list]:
    query = (result.get("query") or "").strip()
    ticker = (result.get("ticker") or "").strip()

    trace_short: list[dict] = []
    mem_up = result.get("memory_updates") or {}
    analysis_mem = mem_up.get("analysis_memory")
    if isinstance(analysis_mem, dict) and _memory_matches(
        analysis_mem,
        query,
        ticker,
    ):
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


def _dedupe_layer_items(items: list[dict]) -> list[dict]:
    from src.event_consolidation.event_similarity import title_similarity

    kept: list[dict] = []
    for item in items:
        title = (item.get("summary") or item.get("query") or "").strip()
        if any(
            title_similarity(title, (k.get("summary") or k.get("query") or "")) > 0.82
            for k in kept
        ):
            continue
        kept.append(item)
    return kept


def _has_cross_layer_duplicates(layers: dict[str, list]) -> bool:
    seen: dict[str, str] = {}
    for layer_name, items in layers.items():
        for item in items:
            if not isinstance(item, dict):
                continue
            mid = item.get("memory_id")
            if not mid:
                continue
            if mid in seen and seen[mid] != layer_name:
                return True
            seen[mid] = layer_name
    return False


def _repair_layer_files_if_needed(layers: dict[str, list]) -> None:
    if not _has_cross_layer_duplicates(layers):
        return
    try:
        n = repair_layer_duplicates()
        if n:
            logger.info("layer memory 중복 repair  corrected=%d", n)
    except Exception:
        logger.exception("layer memory repair 실패")


def _build_memory_payload(result: dict, trace_id: str) -> dict:
    memory_updates = dict(result.get("memory_updates") or {})
    analysis_memory = memory_updates.get("analysis_memory")
    if isinstance(analysis_memory, dict):
        analysis_memory = dict(analysis_memory)
        analysis_memory["referenced_chunks"] = hydrate_retrieval_chunks(result)
        memory_updates["analysis_memory"] = analysis_memory
        result = {**result, "memory_updates": memory_updates}

    layers = _layers_for_trace(result)
    _repair_layer_files_if_needed(layers)
    layers = _layers_for_trace(result)
    layers = collapse_layers_for_display(layers)

    for key in layers:
        layers[key] = _dedupe_layer_items(layers[key])

    event_memory_layers: list[dict] = []
    try:
        from .events_service import fetch_memory_events

        ev = fetch_memory_events(trace_id, ticker=result.get("ticker"))
        if ev:
            event_memory_layers = ev.get("memory_layers") or []
    except Exception:
        pass

    return {
        "trace_id": trace_id,
        "query": result.get("query", ""),
        "ticker": result.get("ticker", ""),
        "memory_updates": memory_updates,
        "temporal_result": result.get("temporal_result", {}),
        "layered_memory": layers,
        "layer_counts": {k: len(v) for k, v in layers.items()},
        "event_memory_layers": event_memory_layers,
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
