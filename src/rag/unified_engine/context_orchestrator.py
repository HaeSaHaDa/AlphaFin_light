"""Unified Context 조립 모듈."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


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
    from graph_store import load_related_graphs, build_graph_context  # noqa: E402
    from reflection_store import load_reflections, build_reflection_context  # noqa: E402
    from layered_retriever import retrieve_all_layers, build_layered_context  # noqa: E402
    from lifecycle_manager import build_temporal_context  # noqa: E402
    from layered_store import load_all_layers  # noqa: E402
    from chain_store import load_related_chains, build_stock_chain_context  # noqa: E402

    query = state.get("query", "")
    ticker = state.get("ticker", "005930")
    persona = state.get("persona", "growth_investor")

    graphs = load_related_graphs(ticker)
    state["graph_context"] = build_graph_context(graphs) if graphs else ""
    state["event_graphs"] = graphs

    reflections = load_reflections(persona)
    state["reflection_context"] = build_reflection_context(reflections)
    state["reflections"] = reflections

    layered = retrieve_all_layers(query, max_per_layer=2)
    state["layered_context"] = build_layered_context(layered)
    state["layered_memories"] = layered

    layers = load_all_layers()
    state["temporal_context"] = build_temporal_context(layers)

    chains = load_related_chains(ticker)
    state["stock_chain_context"] = build_stock_chain_context(chains)
    state["stock_chains"] = chains

    logger.info(
        "보강 Context 로드  graph=%d  reflection=%d  chain=%d",
        len(graphs), len(reflections), len(chains),
    )
    return state
