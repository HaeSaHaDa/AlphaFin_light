"""Character 기반 금융 분석 실행 모듈."""
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
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(CONTEXT_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))
sys.path.insert(0, str(EVALUATION_MODULE))

from retriever import retrieve_similar_chunks  # noqa: E402
from assembler import assemble_context  # noqa: E402
from evaluator import evaluate_analysis_result  # noqa: E402
from personas import get_persona_config, list_available_personas  # noqa: E402
from prompt_builder import build_character_prompt  # noqa: E402

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "character_analysis"

_client: OpenAI | None = None


def _load_api_key() -> str:
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise ValueError("OPENAI_API_KEY가 .env에 설정되지 않았습니다.")
    return key


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=_load_api_key())
        logger.info("OpenAI Chat 클라이언트 초기화 완료")
    return _client


def _call_chat_api(messages: list[dict], model: str = DEFAULT_MODEL) -> dict:
    """OpenAI Chat API를 호출하여 분석 결과를 반환한다."""
    client = _get_client()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=2000,
        )
        raw = resp.choices[0].message.content.strip()
        logger.info("Chat API 응답 수신  model=%s  len=%d", model, len(raw))

        cleaned = raw
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [ln for ln in lines if not ln.strip().startswith("```")]
            cleaned = "\n".join(lines)

        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("JSON 파싱 실패 — raw 응답을 summary로 저장")
        return {
            "bullish_factors": [],
            "bearish_factors": [],
            "risks": [],
            "summary": raw,
        }
    except Exception:
        logger.exception("Chat API 호출 실패  model=%s", model)
        return {}


def run_character_analysis(
    persona_name: str,
    query: str,
    top_k: int = 5,
    filters: dict | None = None,
    model: str = DEFAULT_MODEL,
) -> dict:
    """Persona 기반 분석을 실행한다.

    Args:
        persona_name: Persona 이름.
        query: 분석 질문.
        top_k: Retrieval Top-K.
        filters: Retrieval 필터.
        model: Chat 모델명.

    Returns:
        {
            "persona", "query", "bullish_factors", "bearish_factors",
            "risks", "summary", "referenced_chunks", "model",
            "evaluation"
        }
    """
    logger.info(
        "=== run_character_analysis  persona='%s'  query='%s' ===",
        persona_name, query[:40],
    )

    config = get_persona_config(persona_name)
    if config is None:
        return {"persona": persona_name, "query": query, "error": "Persona 없음"}

    chunks = retrieve_similar_chunks(query, top_k=top_k, filters=filters)
    if not chunks:
        logger.warning("Retrieval 결과 없음")
        return {"persona": persona_name, "query": query, "error": "Retrieval 결과 없음"}

    ctx = assemble_context(query, chunks)
    prompt_context = ctx["prompt_context"]

    messages = build_character_prompt(persona_name, query, prompt_context)

    analysis = _call_chat_api(messages, model)
    if not analysis:
        logger.error("분석 결과 생성 실패")
        return {"persona": persona_name, "query": query, "error": "분석 생성 실패"}

    referenced = []
    for chunk in chunks:
        referenced.append({
            "chunk_id": chunk.get("chunk_id"),
            "document_type": chunk.get("document_type"),
            "score": chunk.get("score"),
            "ticker": chunk.get("ticker"),
        })

    result = {
        "persona": persona_name,
        "persona_name": config["name"],
        "query": query,
        "bullish_factors": analysis.get("bullish_factors", []),
        "bearish_factors": analysis.get("bearish_factors", []),
        "risks": analysis.get("risks", []),
        "summary": analysis.get("summary", ""),
        "referenced_chunks": referenced,
        "model": model,
    }

    evaluation = evaluate_analysis_result(result, chunks, prompt_context)
    result["evaluation"] = evaluation

    logger.info(
        "분석 완료  persona=%s  bullish=%d  bearish=%d  risks=%d",
        persona_name,
        len(result["bullish_factors"]),
        len(result["bearish_factors"]),
        len(result["risks"]),
    )
    return result


def run_all_personas(
    query: str,
    top_k: int = 5,
    filters: dict | None = None,
    model: str = DEFAULT_MODEL,
) -> list[dict]:
    """모든 Persona에 대해 분석을 실행한다."""
    personas = list_available_personas()
    results = []

    for persona in personas:
        result = run_character_analysis(
            persona, query, top_k=top_k, filters=filters, model=model,
        )
        results.append(result)

    logger.info("전체 Persona 분석 완료  총=%d", len(results))
    return results


def compare_persona_results(results: list[dict]) -> dict:
    """Persona별 분석 결과를 비교한다."""
    comparison = {
        "query": results[0].get("query", "") if results else "",
        "persona_count": len(results),
        "personas": [],
    }

    for r in results:
        if r.get("error"):
            comparison["personas"].append({
                "persona": r["persona"],
                "error": r["error"],
            })
            continue

        eval_data = r.get("evaluation", {})
        hallucination = eval_data.get("hallucination_risk", {})

        comparison["personas"].append({
            "persona": r["persona"],
            "persona_name": r.get("persona_name", ""),
            "bullish_count": len(r.get("bullish_factors", [])),
            "bearish_count": len(r.get("bearish_factors", [])),
            "risks_count": len(r.get("risks", [])),
            "summary_preview": r.get("summary", "")[:80],
            "hallucination_risk": hallucination.get("risk_level", "unknown"),
        })

    return comparison


def save_character_json(
    result: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path | None:
    """Character 분석 결과를 JSON으로 저장한다."""
    out = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        persona = result.get("persona", "unknown")
        filename = f"samsung_{persona}.json"

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logger.info("Character 분석 JSON 저장  %s", filepath)
    return filepath
