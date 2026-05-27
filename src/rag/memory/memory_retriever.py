"""Memory 조회 및 Context 생성 모듈."""
from __future__ import annotations

import logging
from pathlib import Path

from memory_store import load_analysis_memories
from event_memory import load_market_events

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def retrieve_related_memories(
    query: str,
    persona: str | None = None,
    max_results: int = 3,
) -> list[dict]:
    """Query와 관련된 Analysis Memory를 조회한다.

    현재 단계에서는 키워드 매칭 기반으로 유사도를 추정한다.

    Args:
        query: 검색 질문.
        persona: 특정 Persona Memory만 조회.
        max_results: 최대 반환 수.

    Returns:
        관련 Memory 목록 (relevance_score 포함).
    """
    memories = load_analysis_memories(persona=persona)
    if not memories:
        logger.info("저장된 Analysis Memory 없음")
        return []

    scored: list[tuple[float, dict]] = []
    query_words = set(query.split())

    for mem in memories:
        mem_text = " ".join([
            mem.get("query", ""),
            mem.get("summary", ""),
            " ".join(mem.get("bullish_factors", [])),
            " ".join(mem.get("bearish_factors", [])),
        ])
        mem_words = set(mem_text.split())

        overlap = len(query_words & mem_words)
        total = len(query_words | mem_words) if (query_words | mem_words) else 1
        score = round(overlap / total, 4)

        scored.append((score, mem))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, mem in scored[:max_results]:
        mem_copy = dict(mem)
        mem_copy["relevance_score"] = score
        results.append(mem_copy)

    logger.info(
        "Memory 조회  query='%s'  persona=%s  결과=%d건",
        query[:30], persona or "all", len(results),
    )
    return results


def retrieve_persona_memories(
    persona: str,
    max_results: int = 5,
) -> list[dict]:
    """특정 Persona의 Analysis Memory를 최신순으로 조회한다."""
    memories = load_analysis_memories(persona=persona)
    sorted_mems = sorted(
        memories,
        key=lambda m: m.get("timestamp", ""),
        reverse=True,
    )

    results = sorted_mems[:max_results]
    logger.info(
        "Persona Memory 조회  persona=%s  결과=%d건", persona, len(results),
    )
    return results


def retrieve_ticker_events(
    ticker: str,
    impact_type: str | None = None,
    max_results: int = 5,
) -> list[dict]:
    """특정 종목의 Market Event를 조회한다.

    Args:
        ticker: 종목 코드.
        impact_type: 필터 (positive/negative/neutral/mixed).
        max_results: 최대 반환 수.
    """
    events = load_market_events(ticker=ticker)

    if impact_type:
        events = [e for e in events if e.get("impact_type") == impact_type]

    sorted_events = sorted(
        events,
        key=lambda e: e.get("timestamp", ""),
        reverse=True,
    )

    results = sorted_events[:max_results]
    logger.info(
        "Event 조회  ticker=%s  impact=%s  결과=%d건",
        ticker, impact_type or "all", len(results),
    )
    return results


def build_memory_context(
    related_memories: list[dict],
    ticker_events: list[dict],
) -> str:
    """Memory를 Prompt Context 문자열로 변환한다.

    Args:
        related_memories: 관련 Analysis Memory 목록.
        ticker_events: 관련 Market Event 목록.

    Returns:
        Memory Context 문자열.
    """
    parts: list[str] = []

    if related_memories:
        parts.append("[Previous Analysis]")
        for mem in related_memories:
            persona = mem.get("persona", "default")
            ts = mem.get("timestamp", "")
            summary = mem.get("summary", "")
            parts.append(f"- [{persona}] ({ts}) {summary}")
        parts.append("")

    if ticker_events:
        parts.append("[Market Events]")
        seen_names: set[str] = set()
        for evt in ticker_events:
            name = evt.get("event_name", "")
            if name in seen_names:
                continue
            seen_names.add(name)
            impact = evt.get("impact_type", "")
            date = evt.get("event_date", "")
            parts.append(f"- [{impact}] ({date}) {name}")
        parts.append("")

    context = "\n".join(parts)

    logger.info(
        "Memory Context 생성  memories=%d  events=%d  len=%d",
        len(related_memories), len(ticker_events), len(context),
    )
    return context
