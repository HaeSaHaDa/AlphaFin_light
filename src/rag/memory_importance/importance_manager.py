"""Memory Importance 관리 모듈."""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from importance_calculator import calculate_importance
from retention_policy import (
    get_promote_target_layer,
    get_retention_action,
    should_decay_memory,
    should_promote_memory,
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_IMPORTANCE_DIR = PROJECT_ROOT / "data" / "memory_importance"
LAYERED_MODULE = PROJECT_ROOT / "src" / "rag" / "layered_memory"
REFLECTION_MODULE = PROJECT_ROOT / "src" / "rag" / "reflection"
EVENT_GRAPH_MODULE = PROJECT_ROOT / "src" / "rag" / "event_graph"


def update_memory_importance(
    memory: dict,
    reflections: list[dict] | None = None,
    graphs: list[dict] | None = None,
    reuse_count: int = 0,
) -> dict:
    """Memory에 importance 정보를 추가하여 반환한다."""
    importance = calculate_importance(
        memory, reflections, graphs, reuse_count,
    )

    updated = dict(memory)
    updated["importance_score"] = importance["importance_score"]
    updated["importance_factors"] = importance["importance_factors"]
    updated["importance_reasons"] = importance["importance_reasons"]
    updated["reuse_count"] = importance["reuse_count"]
    updated["reflection_mentions"] = importance["reflection_mentions"]
    updated["memory_id"] = importance["memory_id"]
    updated["retention_action"] = get_retention_action(updated)

    logger.info(
        "update_memory_importance  id=%s  score=%.4f  action=%s",
        updated["memory_id"][:20],
        updated["importance_score"],
        updated["retention_action"],
    )
    return updated


def rank_memories_by_importance(memories: list[dict]) -> list[dict]:
    """importance_score 기준 내림차순 정렬."""
    ranked = sorted(
        memories,
        key=lambda m: m.get("importance_score", 0.0),
        reverse=True,
    )
    for i, mem in enumerate(ranked):
        mem_copy = dict(mem)
        mem_copy["importance_rank"] = i + 1
        ranked[i] = mem_copy

    logger.info("rank_memories  총=%d건", len(ranked))
    return ranked


def prioritize_for_retrieval(
    memories: list[dict],
    query: str,
    max_results: int = 5,
) -> list[dict]:
    """keyword 유사도 + importance_score 기반 Retrieval 우선순위."""
    query_words = set(re.findall(r"[\w가-힣]+", query.lower()))
    if not query_words:
        return rank_memories_by_importance(memories)[:max_results]

    scored: list[tuple[float, dict]] = []
    for mem in memories:
        mem_text = " ".join([
            mem.get("query", ""),
            mem.get("summary", ""),
            mem.get("event_name", ""),
            mem.get("event_summary", ""),
        ]).lower()
        mem_words = set(re.findall(r"[\w가-힣]+", mem_text))

        overlap = len(query_words & mem_words)
        total = len(query_words | mem_words) if (query_words | mem_words) else 1
        keyword_score = overlap / total

        importance = mem.get("importance_score", 0.0)
        combined = round(keyword_score * 0.5 + importance * 0.5, 4)

        mem_copy = dict(mem)
        mem_copy["retrieval_priority_score"] = combined
        scored.append((combined, mem_copy))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = [mem for _, mem in scored[:max_results]]
    logger.info(
        "prioritize_for_retrieval  query='%s'  결과=%d건",
        query[:20], len(results),
    )
    return results


def load_layered_memories_all() -> list[dict]:
    """Layered Memory 전체를 로드한다."""
    import sys
    sys.path.insert(0, str(LAYERED_MODULE))
    from layered_store import load_all_layers  # noqa: E402

    layers = load_all_layers()
    all_mem: list[dict] = []
    for layer, mems in layers.items():
        for m in mems:
            m_copy = dict(m)
            if "memory_layer" not in m_copy:
                m_copy["memory_layer"] = layer
            all_mem.append(m_copy)
    return all_mem


def load_reflections_all() -> list[dict]:
    """Reflection 전체를 로드한다."""
    import sys
    sys.path.insert(0, str(REFLECTION_MODULE))
    from reflection_store import load_reflections  # noqa: E402
    return load_reflections()


def load_event_graphs_all(ticker: str = "005930") -> list[dict]:
    """Event Graph를 로드한다."""
    import sys
    sys.path.insert(0, str(EVENT_GRAPH_MODULE))
    from graph_store import load_related_graphs  # noqa: E402
    return load_related_graphs(ticker)


def save_importance_record(
    record: dict,
    output_dir: Path | str | None = None,
    filename: str = "importance_records.json",
) -> Path | None:
    """Importance 기록을 JSON에 저장한다."""
    out = Path(output_dir) if output_dir else DEFAULT_IMPORTANCE_DIR
    out.mkdir(parents=True, exist_ok=True)

    filepath = out / filename
    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, Exception):
            logger.warning("기존 파일 파싱 실패  %s", filepath)
            existing = []

    existing.append(record)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    logger.info("Importance 저장  %s  총=%d건", filepath.name, len(existing))
    return filepath


def apply_retention_to_memory(memory: dict) -> dict:
    """Retention 정책을 적용한 Memory 메타데이터를 반환한다."""
    action = get_retention_action(memory)
    result = dict(memory)
    result["retention_action"] = action

    if action == "promote":
        target = get_promote_target_layer(memory.get("memory_layer", "short_term"))
        result["promote_target_layer"] = target
    elif action == "decay":
        result["decay_eligible"] = True

    return result
