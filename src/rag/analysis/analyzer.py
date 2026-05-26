"""RAG 기반 금융 분석 모듈."""
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
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(CONTEXT_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))

from retriever import retrieve_similar_chunks  # noqa: E402
from assembler import assemble_context  # noqa: E402
from prompts import build_analysis_prompt  # noqa: E402

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "analysis"

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


def generate_financial_analysis(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
) -> dict:
    """OpenAI Chat API를 호출하여 금융 분석 결과를 생성한다.

    Args:
        messages: Prompt 메시지 목록.
        model: Chat 모델명.

    Returns:
        파싱된 분석 결과 dict.
        실패 시 빈 dict.
    """
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
            lines = [l for l in lines if not l.strip().startswith("```")]
            cleaned = "\n".join(lines)

        result = json.loads(cleaned)
        return result
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


def analyze_financial_query(
    query: str,
    top_k: int = 5,
    filters: dict | None = None,
    model: str = DEFAULT_MODEL,
) -> dict:
    """Query에 대한 전체 금융 분석 Flow를 실행한다.

    흐름: Retrieval → Context Assembly → Prompt → Chat API → 결과

    Args:
        query: 분석 질문.
        top_k: Retrieval Top-K.
        filters: Retrieval 필터 (ticker, document_type 등).
        model: Chat 모델명.

    Returns:
        {
            "query": str,
            "bullish_factors": [...],
            "bearish_factors": [...],
            "risks": [...],
            "summary": str,
            "referenced_chunks": [...],
            "model": str,
        }
    """
    logger.info("=== analyze_financial_query  query='%s' ===", query[:40])

    chunks = retrieve_similar_chunks(query, top_k=top_k, filters=filters)
    if not chunks:
        logger.warning("Retrieval 결과 없음 — 분석 중단")
        return {"query": query, "error": "Retrieval 결과 없음"}

    ctx = assemble_context(query, chunks)
    prompt_context = ctx["prompt_context"]

    messages = build_analysis_prompt(query, prompt_context)

    analysis = generate_financial_analysis(messages, model)
    if not analysis:
        logger.error("분석 결과 생성 실패")
        return {"query": query, "error": "분석 생성 실패"}

    referenced = []
    for chunk in chunks:
        referenced.append({
            "chunk_id": chunk.get("chunk_id"),
            "document_type": chunk.get("document_type"),
            "score": chunk.get("score"),
            "ticker": chunk.get("ticker"),
        })

    result = {
        "query": query,
        "bullish_factors": analysis.get("bullish_factors", []),
        "bearish_factors": analysis.get("bearish_factors", []),
        "risks": analysis.get("risks", []),
        "summary": analysis.get("summary", ""),
        "referenced_chunks": referenced,
        "model": model,
    }

    logger.info(
        "분석 완료  bullish=%d  bearish=%d  risks=%d",
        len(result["bullish_factors"]),
        len(result["bearish_factors"]),
        len(result["risks"]),
    )
    return result


def save_analysis_json(
    result: dict,
    output_dir: Path | str | None = None,
    filename: str = "analysis.json",
) -> Path | None:
    """분석 결과를 JSON으로 저장한다.

    Args:
        result: analyze_financial_query 결과.
        output_dir: 저장 디렉토리.
        filename: 저장 파일명.

    Returns:
        저장된 파일 경로.
    """
    out = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logger.info("분석 결과 JSON 저장  %s", filepath)
    return filepath
