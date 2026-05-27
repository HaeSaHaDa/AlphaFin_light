"""Memory Layer 샘플 검증 스크립트."""
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
EVALUATION_MODULE = PROJECT_ROOT / "src" / "rag" / "evaluation"
CHARACTER_MODULE = PROJECT_ROOT / "src" / "rag" / "character"
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(CONTEXT_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))
sys.path.insert(0, str(EVALUATION_MODULE))
sys.path.insert(0, str(CHARACTER_MODULE))

from retriever import retrieve_similar_chunks  # noqa: E402
from assembler import assemble_context  # noqa: E402
from prompt_builder import build_character_prompt  # noqa: E402
from memory_store import (  # noqa: E402
    build_analysis_memory,
    save_analysis_memory,
    load_analysis_memories,
)
from event_memory import (  # noqa: E402
    extract_market_events,
    save_market_event_memory,
    load_market_events,
)
from memory_retriever import (  # noqa: E402
    retrieve_related_memories,
    retrieve_persona_memories,
    retrieve_ticker_events,
    build_memory_context,
)

SAMPLE_QUERY = "삼성전자 반도체 전망 분석"
SAMPLE_PERSONA = "growth_investor"
DEFAULT_MODEL = "gpt-4o-mini"


def _get_client() -> OpenAI:
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)
    key = os.getenv("OPENAI_API_KEY", "").strip()
    return OpenAI(api_key=key)


def _call_chat_api(client: OpenAI, messages: list[dict]) -> dict:
    try:
        resp = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            temperature=0.3,
            max_tokens=2000,
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

    logger.info("=== Memory Layer 검증 시작 ===")

    client = _get_client()

    # --- Phase 1: 첫 번째 분석 → Memory 저장 ---
    logger.info("--- Phase 1: 첫 번째 분석 및 Memory 저장 ---")

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
        "Phase 1 분석 완료  bullish=%d  bearish=%d  risks=%d",
        len(result["bullish_factors"]),
        len(result["bearish_factors"]),
        len(result["risks"]),
    )

    # Analysis Memory 저장
    mem = build_analysis_memory(result)
    mem_path = save_analysis_memory(mem)
    logger.info("Analysis Memory 저장: %s", mem_path)

    # Event Memory 저장
    events = extract_market_events(result)
    logger.info("추출된 이벤트: %d건", len(events))
    if events:
        evt_path = save_market_event_memory(events)
        logger.info("Event Memory 저장: %s", evt_path)

    # --- Phase 2: Memory Retrieval 검증 ---
    logger.info("--- Phase 2: Memory Retrieval 검증 ---")

    related = retrieve_related_memories(SAMPLE_QUERY, persona=SAMPLE_PERSONA)
    logger.info("관련 Memory: %d건", len(related))
    for r in related:
        logger.info(
            "  score=%.4f  persona=%s  query='%s'",
            r.get("relevance_score", 0), r.get("persona", ""), r.get("query", "")[:30],
        )

    persona_mems = retrieve_persona_memories(SAMPLE_PERSONA)
    logger.info("Persona Memory: %d건", len(persona_mems))

    ticker_evts = retrieve_ticker_events("005930")
    logger.info("Ticker Event: %d건", len(ticker_evts))

    # --- Phase 3: Memory 기반 Context 생성 + 재분석 ---
    logger.info("--- Phase 3: Memory 기반 Context + 재분석 ---")

    memory_context = build_memory_context(related, ticker_evts)
    logger.info("Memory Context 길이: %d자", len(memory_context))

    enhanced_context = memory_context + "\n[Current Context]\n" + prompt_context

    messages2 = build_character_prompt(SAMPLE_PERSONA, SAMPLE_QUERY, enhanced_context)
    analysis2 = _call_chat_api(client, messages2)

    if analysis2:
        logger.info(
            "Memory 기반 재분석 완료  bullish=%d  bearish=%d  risks=%d",
            len(analysis2.get("bullish_factors", [])),
            len(analysis2.get("bearish_factors", [])),
            len(analysis2.get("risks", [])),
        )
        logger.info("Summary: %s", analysis2.get("summary", "")[:100])
    else:
        logger.warning("Memory 기반 재분석 실패")

    # --- Phase 4: 결과 저장 ---
    logger.info("--- Phase 4: 결과 저장 ---")

    output = {
        "phase1_analysis": result,
        "memory_stored": {
            "analysis_memory": mem,
            "market_events_count": len(events),
        },
        "memory_retrieval": {
            "related_memories": len(related),
            "persona_memories": len(persona_mems),
            "ticker_events": len(ticker_evts),
        },
        "phase3_memory_analysis": analysis2 if analysis2 else {},
        "memory_context_length": len(memory_context),
    }

    out_dir = PROJECT_ROOT / "data" / "memory"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "samsung_memory_verification.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    logger.info("검증 결과 저장: %s", out_path)

    # --- 최종 검증 ---
    logger.info("=== 검증 결과 요약 ===")
    checks = {
        "analysis_memory_saved": mem_path is not None,
        "event_memory_saved": len(events) > 0,
        "memory_retrieval": len(related) > 0,
        "persona_memory": len(persona_mems) > 0,
        "ticker_events": len(ticker_evts) > 0,
        "memory_context": len(memory_context) > 0,
        "memory_analysis": bool(analysis2),
        "json_saved": out_path.exists(),
    }

    for name, ok in checks.items():
        logger.info("  %-25s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Memory Layer 검증 완료 ===")

    return 0


if __name__ == "__main__":
    sys.exit(main())
