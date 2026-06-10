"""Layer별 Memory Retrieval 및 Layered Context 생성 모듈."""
from __future__ import annotations

import logging
import re

from layered_store import load_layer_memories, load_all_layers

logger = logging.getLogger(__name__)


def retrieve_short_term_memories(
    query: str,
    max_results: int = 3,
    ticker: str | None = None,
    memory_type: str | None = None,
) -> list[dict]:
    """Short-term Memory를 query 기반으로 조회한다."""
    return _retrieve_layer("short_term", query, max_results, ticker, memory_type)


def retrieve_mid_term_memories(
    query: str,
    max_results: int = 3,
    ticker: str | None = None,
    memory_type: str | None = None,
) -> list[dict]:
    """Mid-term Memory를 query 기반으로 조회한다."""
    return _retrieve_layer("mid_term", query, max_results, ticker, memory_type)


def retrieve_long_term_memories(
    query: str,
    max_results: int = 3,
    ticker: str | None = None,
    memory_type: str | None = None,
) -> list[dict]:
    """Long-term Memory를 query 기반으로 조회한다."""
    return _retrieve_layer("long_term", query, max_results, ticker, memory_type)


def retrieve_all_layers(
    query: str,
    max_per_layer: int = 2,
    ticker: str | None = None,
    memory_type: str | None = None,
) -> dict[str, list[dict]]:
    """전체 Layer에서 query 기반으로 Memory를 조회한다.

    Returns:
        {"short_term": [...], "mid_term": [...], "long_term": [...]}
    """
    return {
        "short_term": retrieve_short_term_memories(
            query, max_per_layer, ticker, memory_type
        ),
        "mid_term": retrieve_mid_term_memories(
            query, max_per_layer, ticker, memory_type
        ),
        "long_term": retrieve_long_term_memories(
            query, max_per_layer, ticker, memory_type
        ),
    }


def build_layered_context(
    layered_memories: dict[str, list[dict]],
) -> str:
    """Layer별 Memory를 Prompt Context 문자열로 변환한다.

    Args:
        layered_memories: {"short_term": [...], "mid_term": [...], "long_term": [...]}

    Returns:
        Layered Context 문자열.
    """
    parts: list[str] = []

    short = layered_memories.get("short_term", [])
    if short:
        parts.append("[Short-term Memory]")
        for m in short:
            summary = m.get("summary", m.get("event_summary", ""))
            ts = m.get("timestamp", "")
            score = m.get("importance_score", 0)
            parts.append(f"- ({ts}) [score={score:.2f}] {summary[:100]}")
        parts.append("")

    mid = layered_memories.get("mid_term", [])
    if mid:
        parts.append("[Mid-term Memory]")
        for m in mid:
            summary = m.get("summary", m.get("event_summary", ""))
            ts = m.get("timestamp", "")
            score = m.get("importance_score", 0)
            parts.append(f"- ({ts}) [score={score:.2f}] {summary[:100]}")
        parts.append("")

    long = layered_memories.get("long_term", [])
    if long:
        parts.append("[Long-term Memory]")
        for m in long:
            summary = m.get("summary", m.get("event_summary", ""))
            ts = m.get("timestamp", "")
            score = m.get("importance_score", 0)
            parts.append(f"- ({ts}) [score={score:.2f}] {summary[:100]}")
        parts.append("")

    context = "\n".join(parts)

    total = len(short) + len(mid) + len(long)
    logger.info(
        "Layered Context 생성  short=%d  mid=%d  long=%d  총=%d  len=%d",
        len(short), len(mid), len(long), total, len(context),
    )
    return context


def _retrieve_layer(
    layer: str,
    query: str,
    max_results: int,
    ticker: str | None = None,
    memory_type: str | None = None,
) -> list[dict]:
    """특정 Layer에서 keyword 매칭 기반으로 Memory를 조회한다."""
    memories = load_layer_memories(layer)
    if not memories:
        return []

    query_words = set(re.findall(r"[\w가-힣]+", query))

    scored: list[tuple[float, dict]] = []
    for mem in memories:
        if ticker and not _matches_ticker(mem, ticker):
            continue
        if memory_type and mem.get("memory_type") != memory_type:
            continue
        mem_text = " ".join([
            mem.get("query", ""),
            mem.get("summary", ""),
            mem.get("event_name", ""),
            mem.get("event_summary", ""),
            " ".join(mem.get("bullish_factors", [])),
            " ".join(mem.get("bearish_factors", [])),
        ])
        mem_words = set(re.findall(r"[\w가-힣]+", mem_text))

        overlap = len(query_words & mem_words)
        total = len(query_words | mem_words) if (query_words | mem_words) else 1
        keyword_score = overlap / total

        importance = mem.get("importance_score", 0.0)
        combined = round(keyword_score * 0.6 + importance * 0.4, 4)

        scored.append((combined, mem))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, mem in scored[:max_results]:
        mem_copy = dict(mem)
        mem_copy["retrieval_score"] = score
        results.append(mem_copy)

    logger.info(
        "Layer Retrieval  layer=%s  query='%s'  결과=%d건",
        layer, query[:20], len(results),
    )
    return results


def _matches_ticker(item: dict, ticker: str) -> bool:
    normalized = str(ticker).strip()
    if not normalized:
        return True
    if str(item.get("ticker") or "").strip() == normalized:
        return True
    if normalized in str(item.get("query") or ""):
        return True
    if normalized in str(item.get("source_query") or ""):
        return True
    return any(
        str(ref.get("ticker") or "").strip() == normalized
        for ref in item.get("referenced_chunks", [])
        if isinstance(ref, dict)
    )
