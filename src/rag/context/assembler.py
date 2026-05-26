"""Retrieval 결과를 RAG Context로 조립하는 모듈."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "context"

DEFAULT_MAX_CHUNKS = 10
DEFAULT_MAX_CHARS = 8000


def group_chunks_by_type(chunks: list[dict]) -> dict[str, list[dict]]:
    """Retrieval 결과를 document_type 기준으로 그룹화한다.

    Args:
        chunks: Retrieval 결과 목록.

    Returns:
        {"news_article": [...], "disclosure": [...], ...}
    """
    grouped: dict[str, list[dict]] = {}
    for chunk in chunks:
        doc_type = chunk.get("document_type", "unknown")
        grouped.setdefault(doc_type, []).append(chunk)

    for doc_type, items in grouped.items():
        logger.info("  group  %s: %d건", doc_type, len(items))

    return grouped


def limit_context_length(
    chunks: list[dict],
    max_chunks: int = DEFAULT_MAX_CHUNKS,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> list[dict]:
    """Context에 포함할 Chunk 수와 총 문자 수를 제한한다.

    score 순서를 유지하면서 제한을 적용한다.

    Args:
        chunks: score 순으로 정렬된 Retrieval 결과.
        max_chunks: 최대 Chunk 수.
        max_chars: 최대 총 문자 수.

    Returns:
        제한이 적용된 Chunk 목록.
    """
    limited: list[dict] = []
    total_chars = 0

    for chunk in chunks[:max_chunks]:
        text_len = len(chunk.get("chunk_text", ""))
        if total_chars + text_len > max_chars:
            break
        limited.append(chunk)
        total_chars += text_len

    if len(limited) < len(chunks):
        logger.info(
            "Context 제한 적용  원본=%d  결과=%d  총문자=%d (max=%d)",
            len(chunks), len(limited), total_chars, max_chars,
        )

    return limited


def assemble_context(
    query: str,
    chunks: list[dict],
    max_chunks: int = DEFAULT_MAX_CHUNKS,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> dict:
    """Retrieval 결과를 Context 구조로 조립한다.

    Args:
        query: 사용자 검색 질문.
        chunks: Retrieval 결과 (score 순).
        max_chunks: 최대 Chunk 수.
        max_chars: 최대 총 문자 수.

    Returns:
        {
            "query": str,
            "total_chunks": int,
            "limited_chunks": int,
            "grouped": {"news_article": [...], "disclosure": [...]},
            "prompt_context": str,
        }
    """
    from formatter import build_prompt_context  # noqa: E402 — 순환 방지

    logger.info(
        "assemble_context  query='%s'  chunks=%d", query[:30], len(chunks),
    )

    limited = limit_context_length(chunks, max_chunks, max_chars)
    grouped = group_chunks_by_type(limited)
    prompt_context = build_prompt_context(query, grouped)

    result = {
        "query": query,
        "total_chunks": len(chunks),
        "limited_chunks": len(limited),
        "grouped": grouped,
        "prompt_context": prompt_context,
    }

    logger.info(
        "Context 조립 완료  total=%d  limited=%d  context_len=%d",
        len(chunks), len(limited), len(prompt_context),
    )
    return result


def save_context_json(
    context: dict,
    output_dir: Path | str | None = None,
    filename: str = "context.json",
) -> Path | None:
    """조립된 Context를 JSON으로 저장한다.

    Args:
        context: assemble_context 결과.
        output_dir: 저장 디렉토리.
        filename: 저장 파일명.

    Returns:
        저장된 파일 경로.
    """
    out = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    save_data = {
        "query": context["query"],
        "total_chunks": context["total_chunks"],
        "limited_chunks": context["limited_chunks"],
        "prompt_context": context["prompt_context"],
        "chunks_summary": [],
    }

    for doc_type, items in context.get("grouped", {}).items():
        for item in items:
            save_data["chunks_summary"].append({
                "chunk_id": item.get("chunk_id"),
                "document_type": doc_type,
                "score": item.get("score"),
                "ticker": item.get("ticker"),
                "chunk_length": item.get("chunk_length"),
            })

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)

    logger.info("Context JSON 저장  %s", filepath)
    return filepath
