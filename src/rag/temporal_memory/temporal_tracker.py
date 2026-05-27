"""Temporal Memory 추적 모듈."""
from __future__ import annotations

import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

EVOLUTION_CHAINS = [
    ["NVIDIA", "실적", "HBM", "수요"],
    ["HBM", "공급", "AI", "메모리"],
    ["AI", "서버", "투자", "장기", "성장"],
]

LONG_TERM_SIGNALS = [
    "장기", "구조적", "사이클", "산업 재편", "패러다임", "글로벌 추세",
]


def _memory_text(memory: dict) -> str:
    return " ".join([
        memory.get("query", ""),
        memory.get("summary", ""),
        memory.get("event_name", ""),
        memory.get("event_summary", ""),
    ])


def _keyword_overlap(text_a: str, text_b: str) -> int:
    words_a = set(re.findall(r"[\w가-힣]+", text_a.lower()))
    words_b = set(re.findall(r"[\w가-힣]+", text_b.lower()))
    return len(words_a & words_b)


def track_event_reoccurrence(
    memory: dict,
    all_memories: list[dict],
) -> dict:
    """동일/유사 이벤트 반복 등장을 추적한다."""
    mem_text = _memory_text(memory)
    similar: list[dict] = []

    for other in all_memories:
        if other is memory:
            continue
        other_id = other.get("memory_id", id(other))
        mem_id = memory.get("memory_id", id(memory))
        if other_id == mem_id:
            continue

        overlap = _keyword_overlap(mem_text, _memory_text(other))
        if overlap >= 2:
            similar.append({
                "memory_id": other.get("memory_id", ""),
                "query": other.get("query", other.get("event_name", "")),
                "overlap": overlap,
            })

    count = len(similar) + memory.get("appearance_count", 1) - 1
    count = max(count, memory.get("reuse_count", 0))

    result = {
        "reoccurrence_count": count,
        "similar_memories": similar[:5],
        "has_reoccurrence": count >= 2,
    }

    logger.info(
        "track_event_reoccurrence  id=%s  count=%d",
        str(memory.get("memory_id", ""))[:20], count,
    )
    return result


def track_memory_evolution(
    memory: dict,
    all_memories: list[dict],
) -> dict:
    """Memory의 시간적 진화 상태를 추적한다."""
    reoccurrence = track_event_reoccurrence(memory, all_memories)
    text = _memory_text(memory)

    chain_matches: list[str] = []
    for chain in EVOLUTION_CHAINS:
        hits = sum(1 for kw in chain if kw in text)
        if hits >= 2:
            chain_matches.append(" → ".join(chain[:hits]))

    long_term_signal = any(sig in text for sig in LONG_TERM_SIGNALS)
    evolution_stage = _infer_evolution_stage(memory, reoccurrence, long_term_signal)

    evolution = {
        "memory_id": memory.get("memory_id", ""),
        "current_layer": memory.get("memory_layer", "short_term"),
        "reoccurrence_count": reoccurrence["reoccurrence_count"],
        "has_reoccurrence": reoccurrence["has_reoccurrence"],
        "evolution_chains": chain_matches,
        "long_term_signal": long_term_signal,
        "evolution_stage": evolution_stage,
        "tracked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    logger.info(
        "track_memory_evolution  stage=%s  reoccurrence=%d  chains=%d",
        evolution_stage,
        reoccurrence["reoccurrence_count"],
        len(chain_matches),
    )
    return evolution


def build_event_evolution_chain(
    memories: list[dict],
    seed_query: str = "",
) -> list[dict]:
    """관련 Memory들의 Event evolution 체인을 구성한다."""
    if seed_query:
        seed_words = set(re.findall(r"[\w가-힣]+", seed_query.lower()))
        related = [
            m for m in memories
            if len(seed_words & set(re.findall(r"[\w가-힣]+", _memory_text(m).lower()))) >= 1
        ]
    else:
        related = memories

    chain: list[dict] = []
    for mem in sorted(related, key=lambda m: m.get("timestamp", "")):
        evolution = track_memory_evolution(mem, memories)
        chain.append({
            "query": mem.get("query", mem.get("event_name", "")),
            "layer": mem.get("memory_layer", "short_term"),
            "importance_score": mem.get("importance_score", 0),
            "evolution_stage": evolution["evolution_stage"],
            "reoccurrence_count": evolution["reoccurrence_count"],
        })

    logger.info("build_event_evolution_chain  steps=%d", len(chain))
    return chain


def _infer_evolution_stage(
    memory: dict,
    reoccurrence: dict,
    long_term_signal: bool,
) -> str:
    layer = memory.get("memory_layer", "short_term")
    count = reoccurrence.get("reoccurrence_count", 0)

    if long_term_signal or layer == "long_term":
        return "structural_shift"
    if count >= 3 or layer == "mid_term":
        return "trend_established"
    if count >= 2:
        return "emerging_trend"
    return "initial_event"
