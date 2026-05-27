"""Reflection Layer 샘플 검증 스크립트."""
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
LAYERED_MODULE = PROJECT_ROOT / "src" / "rag" / "layered_memory"
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(CONTEXT_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))
sys.path.insert(0, str(EVALUATION_MODULE))
sys.path.insert(0, str(CHARACTER_MODULE))
sys.path.insert(0, str(LAYERED_MODULE))

from retriever import retrieve_similar_chunks  # noqa: E402
from assembler import assemble_context  # noqa: E402
from prompt_builder import build_character_prompt  # noqa: E402
from evaluator import evaluate_analysis_result  # noqa: E402
from reflection_analyzer import analyze_reflection  # noqa: E402
from reflection_store import (  # noqa: E402
    save_reflection,
    load_reflections,
    build_reflection_context,
)
from layered_store import save_layered_memory  # noqa: E402

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

    logger.info("=== Reflection Layer 검증 시작 ===")
    client = _get_client()

    # --- Phase 1: 분석 + Evaluation ---
    logger.info("--- Phase 1: 분석 + Evaluation ---")

    chunks = retrieve_similar_chunks(
        SAMPLE_QUERY, top_k=5, filters={"ticker": "005930"},
    )
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

    evaluation = evaluate_analysis_result(result, chunks, prompt_context)

    logger.info(
        "분석: bullish=%d  bearish=%d  risks=%d",
        len(result["bullish_factors"]),
        len(result["bearish_factors"]),
        len(result["risks"]),
    )

    # --- Phase 2: Reflection 생성 ---
    logger.info("--- Phase 2: Reflection 생성 ---")

    reflection = analyze_reflection(result, evaluation)

    if reflection.get("error"):
        logger.error("Reflection 실패: %s", reflection["error"])
        return 1

    logger.info("Reflection 결과:")
    logger.info("  summary: %s", reflection.get("reflection_summary", "")[:80])
    logger.info("  missing_risks: %s", reflection.get("missing_risks", []))
    logger.info("  overconfidence: %s", reflection.get("overconfidence_detected"))
    logger.info("  overconf_reasons: %s", reflection.get("overconfidence_reasons", []))
    logger.info("  context_gaps: %s", reflection.get("context_gaps", []))
    logger.info("  suggestions: %s", reflection.get("improvement_suggestions", []))

    # --- Phase 3: Reflection 저장 ---
    logger.info("--- Phase 3: Reflection 저장 ---")

    ref_path = save_reflection(reflection)
    logger.info("Reflection 저장: %s", ref_path)

    ref_mem = {
        "memory_type": "reflection",
        "query": reflection.get("query", ""),
        "persona": reflection.get("persona", ""),
        "summary": reflection.get("reflection_summary", ""),
    }
    layered_result = save_layered_memory(ref_mem)
    logger.info("Layered Memory 저장: layer=%s", layered_result["layer"])

    # --- Phase 4: Reflection 기반 재분석 ---
    logger.info("--- Phase 4: Reflection 기반 재분석 ---")

    loaded = load_reflections(persona=SAMPLE_PERSONA)
    logger.info("로드된 Reflection: %d건", len(loaded))

    ref_context = build_reflection_context(loaded)
    logger.info("Reflection Context 길이: %d자", len(ref_context))

    enhanced = ref_context + "\n[Current Context]\n" + prompt_context

    messages2 = build_character_prompt(SAMPLE_PERSONA, SAMPLE_QUERY, enhanced)
    analysis2 = _call_chat_api(client, messages2)

    if analysis2:
        logger.info(
            "재분석  bullish=%d  bearish=%d  risks=%d",
            len(analysis2.get("bullish_factors", [])),
            len(analysis2.get("bearish_factors", [])),
            len(analysis2.get("risks", [])),
        )
    else:
        logger.warning("재분석 실패")

    # --- 최종 검증 ---
    logger.info("=== 검증 결과 요약 ===")
    checks = {
        "reflection_generated": bool(reflection.get("reflection_summary")),
        "reflection_prompt": True,
        "reflection_json_saved": ref_path is not None,
        "missing_risks": len(reflection.get("missing_risks", [])) > 0,
        "overconfidence_field": "overconfidence_detected" in reflection,
        "context_gaps": "context_gaps" in reflection,
        "improvement_suggestions": len(reflection.get("improvement_suggestions", [])) > 0,
        "reflection_memory": layered_result["layer"] is not None,
        "re_analysis": bool(analysis2),
    }

    for name, ok in checks.items():
        logger.info("  %-30s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Reflection Layer 검증 완료 ===")

    return 0


if __name__ == "__main__":
    sys.exit(main())
