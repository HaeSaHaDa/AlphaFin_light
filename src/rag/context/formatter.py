"""Retrieval 결과를 Prompt 입력용 Context 문자열로 포맷팅하는 모듈."""
from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)


def _parse_metadata(item: dict) -> dict:
    """metadata_json 필드를 dict로 변환한다."""
    raw = item.get("metadata_json")
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {}
    if isinstance(raw, dict):
        return raw
    return {}


def format_news_context(news_chunks: list[dict]) -> str:
    """뉴스 Chunk 목록을 Context 문자열로 포맷팅한다.

    Args:
        news_chunks: 뉴스 타입 Retrieval 결과 목록.

    Returns:
        포맷된 뉴스 Context 문자열.
    """
    if not news_chunks:
        return ""

    lines = ["[NEWS]"]
    for i, chunk in enumerate(news_chunks, 1):
        meta = _parse_metadata(chunk)
        score = chunk.get("score", 0.0)
        source = meta.get("source", chunk.get("source", "unknown"))
        date = meta.get("published_at", "unknown")
        title = meta.get("title", "")
        text = chunk.get("chunk_text", "")

        lines.append(f"--- news #{i} ---")
        lines.append(f"- score: {score:.4f}")
        lines.append(f"- source: {source}")
        lines.append(f"- date: {date}")
        if title:
            lines.append(f"- title: {title}")
        lines.append(f"- content:\n{text}")
        lines.append("")

    result = "\n".join(lines)
    logger.debug("format_news_context  chunks=%d  len=%d", len(news_chunks), len(result))
    return result


def format_disclosure_context(disclosure_chunks: list[dict]) -> str:
    """공시 Chunk 목록을 Context 문자열로 포맷팅한다.

    Args:
        disclosure_chunks: 공시 타입 Retrieval 결과 목록.

    Returns:
        포맷된 공시 Context 문자열.
    """
    if not disclosure_chunks:
        return ""

    lines = ["[DISCLOSURE]"]
    for i, chunk in enumerate(disclosure_chunks, 1):
        meta = _parse_metadata(chunk)
        score = chunk.get("score", 0.0)
        source = meta.get("source", "opendart")
        date = meta.get("published_at", "unknown")
        report = meta.get("report_name", "")
        text = chunk.get("chunk_text", "")

        lines.append(f"--- disclosure #{i} ---")
        lines.append(f"- score: {score:.4f}")
        lines.append(f"- source: {source}")
        lines.append(f"- date: {date}")
        if report:
            lines.append(f"- report: {report}")
        lines.append(f"- content:\n{text}")
        lines.append("")

    result = "\n".join(lines)
    logger.debug(
        "format_disclosure_context  chunks=%d  len=%d",
        len(disclosure_chunks), len(result),
    )
    return result


def build_prompt_context(
    query: str,
    grouped_chunks: dict[str, list[dict]],
) -> str:
    """Query와 그룹화된 Chunk를 결합하여 최종 Prompt Context를 생성한다.

    Args:
        query: 사용자 검색 질문.
        grouped_chunks: {"news_article": [...], "disclosure": [...]}

    Returns:
        Prompt에 입력할 전체 Context 문자열.
    """
    parts = [f"[QUERY]\n{query}\n"]

    news = grouped_chunks.get("news_article", [])
    if news:
        parts.append(format_news_context(news))

    disclosure = grouped_chunks.get("disclosure", [])
    if disclosure:
        parts.append(format_disclosure_context(disclosure))

    context = "\n".join(parts)
    logger.info(
        "build_prompt_context  query='%s'  news=%d  disclosure=%d  total_len=%d",
        query[:30], len(news), len(disclosure), len(context),
    )
    return context
