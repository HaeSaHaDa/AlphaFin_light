"""Unified Engine Runner 모듈."""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from pipeline_manager import (
    setup_module_paths,
    create_pipeline_state,
    log_step,
    PIPELINE_STEPS,
)
from context_orchestrator import build_unified_context, load_enhancement_contexts
from result_builder import (
    build_unified_result,
    save_unified_result,
    save_full_trace,
    save_pipeline_log,
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL = "gpt-4o-mini"


def _finalize_pipeline(state: dict) -> dict:
    """Unified Result·Trace를 항상 저장한 뒤 반환한다 (Dashboard API 404 방지)."""
    result = build_unified_result(state)
    save_unified_result(result)
    save_full_trace(state)
    save_pipeline_log(state)
    log_step(state, "result_save", "ok", f"trace_id={state['trace_id']}")
    return result


def _get_openai_client() -> OpenAI:
    load_dotenv(PROJECT_ROOT / ".env")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY", "").strip())


def _call_chat_api(client: OpenAI, messages: list[dict]) -> dict:
    try:
        resp = client.chat.completions.create(
            model=DEFAULT_MODEL, messages=messages,
            temperature=0.3, max_tokens=2000,
        )
        raw = resp.choices[0].message.content.strip()
        cleaned = raw
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [ln for ln in lines if not ln.strip().startswith("```")]
            cleaned = "\n".join(lines)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "bullish_factors": [], "bearish_factors": [],
            "risks": [], "summary": raw,
        }
    except Exception:
        logger.exception("Chat API 호출 실패")
        return {}


def run_unified_pipeline(
    query: str,
    persona: str = "growth_investor",
    ticker: str = "005930",
    trace_id: str | None = None,
) -> dict:
    """End-to-End Unified Pipeline을 실행한다.

    Returns:
        Unified Result dict.
    """
    setup_module_paths()

    from retriever import retrieve_similar_chunks  # noqa: E402
    from assembler import assemble_context  # noqa: E402
    from prompt_builder import build_character_prompt  # noqa: E402
    from evaluator import evaluate_analysis_result  # noqa: E402
    from reflection_analyzer import analyze_reflection  # noqa: E402
    from reflection_store import save_reflection  # noqa: E402
    from memory_store import build_analysis_memory, save_analysis_memory  # noqa: E402
    from event_extractor import extract_event_nodes  # noqa: E402
    from relation_builder import (  # noqa: E402
        build_event_relations,
        detect_market_impact_relations,
    )
    from graph_store import build_event_graph, save_event_graph  # noqa: E402
    from layered_store import save_layered_memory  # noqa: E402
    from importance_manager import update_memory_importance  # noqa: E402
    from temporal_tracker import track_memory_evolution  # noqa: E402
    from lifecycle_manager import process_memory_lifecycle  # noqa: E402
    from entity_extractor import extract_market_entities as sc_extract_entities  # noqa: E402
    from entity_extractor import normalize_entities  # noqa: E402
    from chain_builder import build_stock_chain, merge_event_graph_links  # noqa: E402
    from propagation_engine import calculate_propagation  # noqa: E402
    from chain_store import save_stock_chain, save_propagation_log  # noqa: E402
    from propagation_engine import propagate_market_impact  # noqa: E402

    state = create_pipeline_state(query, persona, ticker, trace_id)
    client = _get_openai_client()

    logger.info("=== Unified Engine 시작  trace_id=%s ===", state["trace_id"])

    # --- Retrieval ---
    chunks = retrieve_similar_chunks(query, top_k=5, filters={"ticker": ticker})
    log_step(state, "retrieval", "ok" if chunks else "warn",
             f"chunks={len(chunks)}")

    if not chunks:
        log_step(state, "pipeline", "error", "Retrieval 결과 없음")
        state["analysis_result"] = {
            "persona": persona,
            "query": query,
            "bullish_factors": [],
            "bearish_factors": [],
            "risks": [
                "해당 종목의 embedding 데이터가 없어 검색할 수 없습니다. "
                "ingestion을 실행하거나 발표 모드를 해제한 뒤 다시 시도해 주세요.",
            ],
            "summary": (
                f"{ticker} 관련 문서를 찾지 못했습니다. "
                "뉴스·공시 수집 및 embedding 생성이 필요합니다."
            ),
            "referenced_chunks": [],
            "model": DEFAULT_MODEL,
        }
        state["evaluation_result"] = {
            "retrieval_quality": {"score": 0, "note": "no_chunks"},
            "context_usage": {},
            "hallucination_risk": {"risk_level": "n/a"},
        }
        return _finalize_pipeline(state)

    state["chunks"] = chunks

    # --- Context Assembly ---
    ctx = assemble_context(query, chunks)
    state["prompt_context"] = ctx["prompt_context"]
    log_step(state, "context_assembly", "ok", f"len={len(state['prompt_context'])}")

    # --- Enhancement + Unified Context ---
    state = load_enhancement_contexts(state)
    unified_ctx = build_unified_context(state)
    log_step(state, "unified_context", "ok", f"len={state.get('unified_context_length', 0)}")

    # --- Character Analysis ---
    messages = build_character_prompt(persona, query, unified_ctx)
    analysis_raw = _call_chat_api(client, messages)

    referenced = [
        {
            "chunk_id": c.get("chunk_id"),
            "document_type": c.get("document_type"),
            "score": c.get("score"),
            "ticker": c.get("ticker"),
        }
        for c in chunks
    ]

    analysis_result = {
        "persona": persona,
        "query": query,
        "bullish_factors": analysis_raw.get("bullish_factors", []),
        "bearish_factors": analysis_raw.get("bearish_factors", []),
        "risks": analysis_raw.get("risks", []),
        "summary": analysis_raw.get("summary", ""),
        "referenced_chunks": referenced,
        "model": DEFAULT_MODEL,
    }
    state["analysis_result"] = analysis_result
    log_step(state, "character_analysis", "ok" if analysis_result.get("summary") else "warn",
             f"bullish={len(analysis_result['bullish_factors'])}")

    # --- Evaluation ---
    evaluation = evaluate_analysis_result(
        analysis_result, chunks, state["prompt_context"],
    )
    state["evaluation_result"] = evaluation
    log_step(state, "evaluation", "ok",
             f"hallucination={evaluation.get('hallucination_risk', {}).get('risk_level', '?')}")

    # --- Reflection ---
    reflection = analyze_reflection(analysis_result, evaluation)
    state["reflection_result"] = reflection
    save_reflection(reflection)
    log_step(state, "reflection", "ok" if reflection.get("reflection_summary") else "warn",
             reflection.get("reflection_summary", "")[:50])

    # --- Memory ---
    analysis_memory = build_analysis_memory(analysis_result)
    save_analysis_memory(analysis_memory)
    state["analysis_memory"] = analysis_memory

    reflections = state.get("reflections", [])
    graphs = state.get("event_graphs", [])
    importance_mem = update_memory_importance(
        analysis_memory, reflections=reflections, graphs=graphs,
        reuse_count=1,
    )
    layered_save = save_layered_memory(importance_mem)
    state["importance_result"] = {
        "importance_score": importance_mem.get("importance_score"),
        "retention_action": importance_mem.get("retention_action"),
    }
    state["layered_save_result"] = layered_save
    log_step(state, "memory_save", "ok", f"layer={layered_save.get('layer', '?')}")
    log_step(state, "importance_update", "ok",
             f"score={importance_mem.get('importance_score', 0):.2f}")

    # --- Temporal ---
    all_memories = [importance_mem]
    evolution = track_memory_evolution(importance_mem, all_memories)
    temporal_result = process_memory_lifecycle(importance_mem, all_memories)
    state["temporal_result"] = {
        "evolution": evolution,
        "action": temporal_result.get("action", "keep"),
    }
    log_step(state, "temporal_tracking", "ok",
             f"action={temporal_result.get('action', 'keep')}")

    # --- Event Graph ---
    all_text = " ".join([
        unified_ctx,
        analysis_result.get("summary", ""),
        " ".join(analysis_result.get("bullish_factors", [])),
    ])
    nodes = extract_event_nodes(all_text)
    relations = build_event_relations(nodes)
    relations += detect_market_impact_relations(analysis_result, nodes)
    graph = build_event_graph(nodes, relations, query=query, ticker=ticker)
    save_event_graph(graph)
    state["event_graph"] = {
        "node_count": len(nodes),
        "relation_count": len(relations),
        "query": query,
    }
    log_step(state, "event_graph", "ok",
             f"nodes={len(nodes)} rels={len(relations)}")

    # --- Stock Chain ---
    entities = normalize_entities(sc_extract_entities(all_text))
    chain = build_stock_chain(entities, query=query, ticker=ticker)
    chain = merge_event_graph_links(chain, graph)
    paths = calculate_propagation(chain, start_source="NVIDIA")
    prop = propagate_market_impact(chain, "HBM")
    save_stock_chain(chain, filename=f"{state['trace_id']}_chain.json")
    save_propagation_log(prop)
    state["stock_chain"] = {
        "entity_count": len(entities),
        "link_count": len(chain.get("links", [])),
        "propagation_paths": len(paths),
    }
    log_step(state, "stock_chain", "ok",
             f"links={len(chain.get('links', []))}")

    result = _finalize_pipeline(state)
    logger.info("=== Unified Engine 완료  trace_id=%s ===", state["trace_id"])
    return result
