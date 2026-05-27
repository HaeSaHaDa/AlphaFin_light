"""Layered Memory 샘플 검증 스크립트."""
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
EVENT_GRAPH_MODULE = PROJECT_ROOT / "src" / "rag" / "event_graph"
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(CONTEXT_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))
sys.path.insert(0, str(CHARACTER_MODULE))
sys.path.insert(0, str(MEMORY_MODULE))
sys.path.insert(0, str(EVENT_GRAPH_MODULE))

from retriever import retrieve_similar_chunks  # noqa: E402
from assembler import assemble_context  # noqa: E402
from prompt_builder import build_character_prompt  # noqa: E402
from memory_store import build_analysis_memory  # noqa: E402
from event_memory import extract_market_events  # noqa: E402
from memory_classifier import (  # noqa: E402
    classify_memory_layer,
    calculate_importance_score,
)
from layered_store import (  # noqa: E402
    save_layered_memory,
    load_all_layers,
)
from layered_retriever import (  # noqa: E402
    retrieve_all_layers,
    build_layered_context,
)

SAMPLE_QUERIES = [
    "삼성전자 반도체 전망 분석",
    "HBM 시장 성장",
]
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

    logger.info("=== Layered Memory 검증 시작 ===")
    client = _get_client()

    # --- Phase 1: 분석 → Layered Memory 저장 ---
    logger.info("--- Phase 1: 분석 + Layered Memory 저장 ---")

    saved_layers: list[dict] = []

    for query in SAMPLE_QUERIES:
        logger.info("Query: '%s'", query)

        chunks = retrieve_similar_chunks(
            query, top_k=5, filters={"ticker": "005930"},
        )
        if not chunks:
            logger.warning("Retrieval 없음, 건너뜀")
            continue

        ctx = assemble_context(query, chunks)
        prompt_context = ctx["prompt_context"]

        messages = build_character_prompt(SAMPLE_PERSONA, query, prompt_context)
        analysis = _call_chat_api(client, messages)
        if not analysis:
            continue

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
            "query": query,
            "bullish_factors": analysis.get("bullish_factors", []),
            "bearish_factors": analysis.get("bearish_factors", []),
            "risks": analysis.get("risks", []),
            "summary": analysis.get("summary", ""),
            "referenced_chunks": referenced,
            "model": DEFAULT_MODEL,
        }

        mem = build_analysis_memory(result)
        save_result = save_layered_memory(mem)
        saved_layers.append(save_result)
        logger.info(
            "  저장: layer=%s  score=%.4f  count=%d",
            save_result["layer"],
            save_result["importance_score"],
            save_result["memory_count"],
        )

        events = extract_market_events(result)
        for evt in events[:2]:
            evt_save = save_layered_memory(evt)
            saved_layers.append(evt_save)

    # --- Phase 2: Layer 로드 검증 ---
    logger.info("--- Phase 2: Layer 로드 검증 ---")

    all_layers = load_all_layers()
    for layer_name, mems in all_layers.items():
        logger.info("  %-12s : %d건", layer_name, len(mems))
        for m in mems[:2]:
            summary = m.get("summary", m.get("event_summary", ""))[:60]
            score = m.get("importance_score", 0)
            logger.info("    score=%.4f  %s", score, summary)

    # --- Phase 3: Layer별 Retrieval ---
    logger.info("--- Phase 3: Layer별 Retrieval ---")

    layered_results = retrieve_all_layers(SAMPLE_QUERIES[0], max_per_layer=2)
    for layer_name, mems in layered_results.items():
        logger.info("  %-12s : %d건", layer_name, len(mems))
        for m in mems:
            logger.info(
                "    ret_score=%.4f  imp=%.4f  %s",
                m.get("retrieval_score", 0),
                m.get("importance_score", 0),
                m.get("summary", m.get("event_summary", ""))[:50],
            )

    # --- Phase 4: Layered Context 생성 + 강화 분석 ---
    logger.info("--- Phase 4: Layered Context + 강화 분석 ---")

    layered_context = build_layered_context(layered_results)
    logger.info("Layered Context 길이: %d자", len(layered_context))

    chunks0 = retrieve_similar_chunks(
        SAMPLE_QUERIES[0], top_k=5, filters={"ticker": "005930"},
    )
    ctx0 = assemble_context(SAMPLE_QUERIES[0], chunks0)

    enhanced_context = layered_context + "\n[Current Context]\n" + ctx0["prompt_context"]

    messages_enh = build_character_prompt(
        SAMPLE_PERSONA, SAMPLE_QUERIES[0], enhanced_context,
    )
    analysis_enh = _call_chat_api(client, messages_enh)

    if analysis_enh:
        logger.info(
            "강화 분석  bullish=%d  bearish=%d  risks=%d",
            len(analysis_enh.get("bullish_factors", [])),
            len(analysis_enh.get("bearish_factors", [])),
            len(analysis_enh.get("risks", [])),
        )
    else:
        logger.warning("강화 분석 실패")

    # --- Phase 5: 결과 저장 ---
    logger.info("--- Phase 5: 결과 저장 ---")

    verification = {
        "queries": SAMPLE_QUERIES,
        "saved_layers": saved_layers,
        "layer_counts": {k: len(v) for k, v in all_layers.items()},
        "retrieval_counts": {k: len(v) for k, v in layered_results.items()},
        "layered_context_length": len(layered_context),
        "enhanced_analysis": analysis_enh if analysis_enh else {},
    }

    out_dir = PROJECT_ROOT / "data" / "layered_memory"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "samsung_layered_verification.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(verification, f, ensure_ascii=False, indent=2)
    logger.info("검증 결과: %s", out_path)

    # --- 최종 검증 ---
    logger.info("=== 검증 결과 요약 ===")

    has_short = len(all_layers.get("short_term", [])) > 0
    has_mid = len(all_layers.get("mid_term", [])) > 0
    has_any_layer = has_short or has_mid or len(all_layers.get("long_term", [])) > 0
    has_importance = any(s.get("importance_score", 0) > 0 for s in saved_layers)
    has_retrieval = any(len(v) > 0 for v in layered_results.values())

    checks = {
        "layer_storage": has_any_layer,
        "importance_score": has_importance,
        "layer_retrieval": has_retrieval,
        "layered_context": len(layered_context) > 0,
        "enhanced_analysis": bool(analysis_enh),
        "json_saved": out_path.exists(),
    }

    for name, ok in checks.items():
        logger.info("  %-25s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Layered Memory 검증 완료 ===")

    return 0


if __name__ == "__main__":
    sys.exit(main())
