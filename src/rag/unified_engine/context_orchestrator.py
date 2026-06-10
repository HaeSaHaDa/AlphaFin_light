"""Unified Context 조립 모듈."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def _matches_ticker(item: dict, ticker: str) -> bool:
    if str(item.get("ticker") or "").strip() == ticker:
        return True
    if ticker in str(item.get("query") or ""):
        return True
    return any(
        str(ref.get("ticker") or "").strip() == ticker
        for ref in item.get("referenced_chunks", [])
        if isinstance(ref, dict)
    )


def _filter_layers_by_ticker(
    layers: dict[str, list[dict]],
    ticker: str,
) -> dict[str, list[dict]]:
    return {
        layer: [
            item for item in items
            if item.get("memory_type") == "event_memory"
            and _matches_ticker(item, ticker)
        ]
        for layer, items in layers.items()
    }


def build_unified_context(state: dict) -> str:
    """Pipeline 상태에서 Unified Context 문자열을 생성한다."""
    parts: list[str] = ["[Unified Context]"]

    query = state.get("query", "")
    parts.append(f"[Query] {query}")
    parts.append("")

    retrieval_ctx = state.get("prompt_context", "")
    if retrieval_ctx:
        parts.append("[Retrieval Context]")
        parts.append(retrieval_ctx[:3000])
        parts.append("")

    for key, heading in [
        ("graph_context", "[Event Graph]"),
        ("temporal_context", "[Temporal Memory]"),
        ("stock_chain_context", "[Stock Chain]"),
        ("reflection_context", "[Reflection]"),
        ("layered_context", "[Layered Memory]"),
    ]:
        ctx = state.get(key, "")
        if ctx:
            parts.append(heading)
            parts.append(ctx[:1500])
            parts.append("")

    unified = "\n".join(parts)

    state["unified_context"] = unified
    state["unified_context_length"] = len(unified)

    logger.info("Unified Context 생성  len=%d", len(unified))
    return unified


def load_enhancement_contexts(state: dict) -> dict:
    """기존 저장 데이터에서 보강 Context를 로드한다."""
    from graph_store import load_related_graphs  # noqa: E402
    from reflection_store import load_reflections  # noqa: E402
    from layered_retriever import retrieve_all_layers, build_layered_context  # noqa: E402
    from lifecycle_manager import build_temporal_context  # noqa: E402
    from layered_store import load_all_layers  # noqa: E402
    from chain_store import load_related_chains  # noqa: E402

    query = state.get("query", "")
    ticker = str(state.get("ticker") or "").strip()
    if not ticker:
        raise ValueError("ticker is required to load enhancement contexts")
    persona = state.get("persona", "growth_investor")

    graphs = load_related_graphs(ticker)
    state["graph_context"] = ""
    state["event_graphs"] = graphs

    reflections = [
        item for item in load_reflections(persona)
        if _matches_ticker(item, ticker)
    ]
    state["reflection_context"] = ""
    state["reflections"] = reflections

    layered = retrieve_all_layers(
        query,
        max_per_layer=2,
        ticker=ticker,
        memory_type="event_memory",
    )
    state["layered_context"] = build_layered_context(layered)
    state["layered_memories"] = layered

    layers = _filter_layers_by_ticker(load_all_layers(), ticker)
    state["temporal_context"] = build_temporal_context(layers)

    chains = load_related_chains(ticker)
    state["stock_chain_context"] = ""
    state["stock_chains"] = chains

    logger.info(
        "보강 Context 로드  graph=%d  reflection=%d  chain=%d",
        len(graphs), len(reflections), len(chains),
    )
    return state
