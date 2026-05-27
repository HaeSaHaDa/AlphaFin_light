"""Event Graph 샘플 검증 스크립트."""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
RETRIEVAL_MODULE = PROJECT_ROOT / "src" / "rag" / "retrieval"
CONTEXT_MODULE = PROJECT_ROOT / "src" / "rag" / "context"
EMBEDDING_MODULE = PROJECT_ROOT / "src" / "rag" / "embedding"
CHARACTER_MODULE = PROJECT_ROOT / "src" / "rag" / "character"
MEMORY_MODULE = PROJECT_ROOT / "src" / "rag" / "memory"
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(CONTEXT_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))
sys.path.insert(0, str(CHARACTER_MODULE))
sys.path.insert(0, str(MEMORY_MODULE))

from retriever import retrieve_similar_chunks  # noqa: E402
from assembler import assemble_context  # noqa: E402
from prompt_builder import build_character_prompt  # noqa: E402
from memory_store import build_analysis_memory, save_analysis_memory  # noqa: E402
from event_extractor import extract_event_nodes, extract_market_entities  # noqa: E402
from relation_builder import (  # noqa: E402
    build_event_relations,
    detect_market_impact_relations,
)
from graph_store import (  # noqa: E402
    build_event_graph,
    save_event_graph,
    load_related_graphs,
    build_graph_context,
)

SAMPLE_QUERY = "삼성전자 반도체 전망 분석"
SAMPLE_PERSONA = "growth_investor"
DEFAULT_MODEL = "gpt-4o-mini"


def _get_client() -> OpenAI:
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
        return {"bullish_factors": [], "bearish_factors": [], "risks": [], "summary": raw}
    except Exception as e:
        logging.getLogger(__name__).exception("Chat API 실패: %s", e)
        return {}


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Event Graph 검증 시작 ===")
    client = _get_client()

    # --- Phase 1: Retrieval + 분석 ---
    logger.info("--- Phase 1: Retrieval + 분석 ---")

    chunks = retrieve_similar_chunks(
        SAMPLE_QUERY, top_k=5, filters={"ticker": "005930"},
    )
    logger.info("Retrieval: %d건", len(chunks))
    if not chunks:
        logger.error("Retrieval 결과 없음")
        return 1

    ctx = assemble_context(SAMPLE_QUERY, chunks)
    prompt_context = ctx["prompt_context"]

    messages = build_character_prompt(SAMPLE_PERSONA, SAMPLE_QUERY, prompt_context)
    analysis = _call_chat_api(client, messages)
    if not analysis:
        logger.error("분석 실패")
        return 1

    referenced = []
    for c in chunks:
        referenced.append({
            "chunk_id": c.get("chunk_id"),
            "document_type": c.get("document_type"),
            "score": c.get("score"),
            "ticker": c.get("ticker"),
        })

    result = {
        "persona": SAMPLE_PERSONA,
        "query": SAMPLE_QUERY,
        "bullish_factors": analysis.get("bullish_factors", []),
        "bearish_factors": analysis.get("bearish_factors", []),
        "risks": analysis.get("risks", []),
        "summary": analysis.get("summary", ""),
        "referenced_chunks": referenced,
        "model": DEFAULT_MODEL,
    }

    logger.info(
        "분석 완료  bullish=%d  bearish=%d  risks=%d",
        len(result["bullish_factors"]),
        len(result["bearish_factors"]),
        len(result["risks"]),
    )

    # --- Phase 2: Event Node + Entity 추출 ---
    logger.info("--- Phase 2: Event Node 추출 ---")

    all_text = " ".join([
        prompt_context,
        result.get("summary", ""),
        " ".join(result.get("bullish_factors", [])),
        " ".join(result.get("bearish_factors", [])),
        " ".join(result.get("risks", [])),
    ])

    nodes = extract_event_nodes(all_text)
    logger.info("추출된 Node: %d개", len(nodes))
    for n in nodes:
        logger.info("  [%s] %s  ticker=%s", n["node_type"], n["name"], n.get("ticker", "-"))

    entities = extract_market_entities(all_text)
    logger.info("Entity: 기업=%d  산업=%d  제품=%d",
        len(entities["companies"]),
        len(entities["industries"]),
        len(entities["products"]),
    )

    # --- Phase 3: Relation 생성 ---
    logger.info("--- Phase 3: Relation 생성 ---")

    relations = build_event_relations(nodes)
    logger.info("규칙 기반 Relation: %d건", len(relations))
    for r in relations[:5]:
        logger.info(
            "  %s → %s  [%s] conf=%.2f",
            r["source"], r["target"], r["relation_type"], r["confidence"],
        )

    impact_rels = detect_market_impact_relations(result, nodes)
    logger.info("Impact Relation: %d건", len(impact_rels))

    all_relations = relations + impact_rels

    # --- Phase 4: Graph 저장 ---
    logger.info("--- Phase 4: Graph 저장 ---")

    graph = build_event_graph(
        nodes, all_relations,
        query=SAMPLE_QUERY, ticker="005930",
    )
    graph_path = save_event_graph(graph)
    logger.info("Graph 저장: %s", graph_path)

    # --- Phase 5: Graph 조회 + Context 강화 ---
    logger.info("--- Phase 5: Graph 조회 + Context 강화 ---")

    related_graphs = load_related_graphs("005930")
    logger.info("관련 Graph: %d건", len(related_graphs))

    graph_context = build_graph_context(related_graphs)
    logger.info("Graph Context 길이: %d자", len(graph_context))

    enhanced_context = graph_context + "\n" + prompt_context

    messages2 = build_character_prompt(SAMPLE_PERSONA, SAMPLE_QUERY, enhanced_context)
    analysis2 = _call_chat_api(client, messages2)

    if analysis2:
        logger.info(
            "Graph 강화 재분석  bullish=%d  bearish=%d  risks=%d",
            len(analysis2.get("bullish_factors", [])),
            len(analysis2.get("bearish_factors", [])),
            len(analysis2.get("risks", [])),
        )
    else:
        logger.warning("Graph 기반 재분석 실패")

    # --- Phase 6: Memory 연동 ---
    logger.info("--- Phase 6: Memory 연동 ---")

    mem = build_analysis_memory(result)
    mem_path = save_analysis_memory(mem)
    logger.info("Memory 저장: %s", mem_path)

    # --- 최종 검증 ---
    logger.info("=== 검증 결과 요약 ===")
    checks = {
        "event_nodes": len(nodes) > 0,
        "ticker_connected": any(n.get("ticker") for n in nodes),
        "relations": len(relations) > 0,
        "relation_types": len(set(r["relation_type"] for r in all_relations)) > 0,
        "confidence_scores": all(r.get("confidence", 0) > 0 for r in all_relations),
        "graph_saved": graph_path is not None,
        "graph_query": len(related_graphs) > 0,
        "memory_saved": mem_path is not None,
        "context_enhanced": len(graph_context) > 0,
    }

    for name, ok in checks.items():
        logger.info("  %-25s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Event Graph 검증 완료 ===")

    return 0


if __name__ == "__main__":
    sys.exit(main())
