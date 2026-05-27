"""Temporal Memory Lifecycle 관리 모듈."""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from temporal_tracker import (
    track_memory_evolution,
    build_event_evolution_chain,
    LONG_TERM_SIGNALS,
)
from decay_manager import (
    calculate_decay,
    should_decay,
    apply_temporal_importance_update,
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TEMPORAL_DIR = PROJECT_ROOT / "data" / "temporal_memory"
LAYERED_DIR = PROJECT_ROOT / "data" / "layered_memory"
IMPORTANCE_MODULE = PROJECT_ROOT / "src" / "rag" / "memory_importance"

sys.path.insert(0, str(IMPORTANCE_MODULE))
from retention_policy import (  # noqa: E402
    should_promote_memory,
    get_promote_target_layer,
    PROMOTE_THRESHOLD,
)


def _save_to_layer(memory: dict, layer: str) -> Path | None:
    """지정 Layer에 Memory를 저장한다."""
    layer_dir = LAYERED_DIR / layer
    layer_dir.mkdir(parents=True, exist_ok=True)

    persona = memory.get("persona", "default")
    filename = f"{persona}_{layer}.json"
    filepath = layer_dir / filename

    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, Exception):
            existing = []

    mem_id = memory.get("memory_id", "")
    existing = [m for m in existing if m.get("memory_id") != mem_id]
    existing.append(memory)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    logger.info("Layer 저장  %s  %s", layer, filepath.name)
    return filepath


def _build_promotion_reasons(memory: dict, evolution: dict) -> list[str]:
    reasons: list[str] = []
    if evolution.get("has_reoccurrence"):
        reasons.append(
            f"반복 등장 {evolution.get('reoccurrence_count', 0)}회"
        )
    if memory.get("importance_score", 0) >= PROMOTE_THRESHOLD:
        reasons.append(
            f"importance_score {memory.get('importance_score', 0):.2f} 이상"
        )
    if memory.get("reuse_count", 0) >= 2:
        reasons.append(f"Retrieval 재사용 {memory.get('reuse_count')}회")
    if memory.get("reflection_mentions", 0) > 0:
        reasons.append("Reflection 언급됨")
    if evolution.get("evolution_chains"):
        reasons.append(f"이벤트 진화: {evolution['evolution_chains'][0]}")
    if evolution.get("long_term_signal"):
        reasons.append("장기 산업 영향 신호 감지")
    return reasons[:5]


def _build_decay_reasons(memory: dict, evolution: dict, decay_info: dict) -> list[str]:
    reasons: list[str] = []
    if not evolution.get("has_reoccurrence"):
        reasons.append("재등장 없음")
    if memory.get("importance_score", 0) < 0.25:
        reasons.append("낮은 importance_score")
    if memory.get("reflection_mentions", 0) == 0:
        reasons.append("Reflection 미등장")
    if memory.get("reuse_count", 0) == 0:
        reasons.append("Retrieval 재사용 없음")
    if decay_info.get("decay_amount", 0) > 0:
        reasons.append(f"importance {decay_info['decay_amount']:.2f} 감소")
    return reasons[:5]


def should_promote(
    memory: dict,
    evolution: dict,
) -> bool:
    """Temporal 기준 promotion 판단."""
    if should_promote_memory(memory):
        return True
    if (
        evolution.get("has_reoccurrence")
        and evolution.get("reoccurrence_count", 0) >= 2
        and memory.get("importance_score", 0) >= 0.45
    ):
        return True
    text = " ".join([
        memory.get("summary", ""),
        memory.get("query", ""),
    ])
    if (
        evolution.get("long_term_signal")
        and memory.get("memory_layer") == "mid_term"
    ):
        return True
    if any(sig in text for sig in LONG_TERM_SIGNALS):
        if memory.get("memory_layer") in ("short_term", "mid_term"):
            return memory.get("importance_score", 0) >= 0.5
    return False


def promote_memory(
    memory: dict,
    evolution: dict | None = None,
    target_layer: str | None = None,
) -> dict | None:
    """Memory를 상위 Layer로 승격한다."""
    evolution = evolution or track_memory_evolution(memory, [memory])
    previous = memory.get("memory_layer", "short_term")
    target = target_layer or get_promote_target_layer(previous)

    if not target:
        logger.warning("승격 불가  이미 long_term  id=%s", memory.get("memory_id", ""))
        return None

    if not should_promote(memory, evolution):
        logger.info("승격 조건 미충족  id=%s", memory.get("memory_id", ""))
        return None

    reasons = _build_promotion_reasons(memory, evolution)
    updated = apply_temporal_importance_update(memory, evolution)
    updated["memory_layer"] = target
    updated["previous_layer"] = previous
    updated["promoted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _save_to_layer(updated, target)

    record = {
        "memory_id": updated.get("memory_id", ""),
        "previous_layer": previous,
        "current_layer": target,
        "promotion_reason": reasons,
        "importance_score": updated.get("importance_score", 0),
        "evolution_stage": evolution.get("evolution_stage", ""),
        "timestamp": updated["promoted_at"],
    }

    save_promotion_record(record)
    save_lifecycle_log({
        "action": "promote",
        "memory_id": record["memory_id"],
        "previous_layer": previous,
        "current_layer": target,
        "promotion_reason": reasons,
        "importance_score": record["importance_score"],
        "timestamp": record["timestamp"],
    })

    logger.info(
        "promote_memory  %s → %s  reasons=%d",
        previous, target, len(reasons),
    )
    return record


def decay_memory(
    memory: dict,
    evolution: dict | None = None,
) -> dict | None:
    """Memory를 decay 처리한다."""
    evolution = evolution or track_memory_evolution(memory, [memory])

    if not should_decay(memory, evolution):
        logger.info("decay 조건 미충족  id=%s", memory.get("memory_id", ""))
        return None

    decay_info = calculate_decay(memory, evolution)
    reasons = _build_decay_reasons(memory, evolution, decay_info)

    updated = dict(memory)
    updated["importance_score"] = decay_info["decayed_score"]
    updated["memory_layer"] = memory.get("memory_layer", "short_term")
    updated["decayed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated["decay_eligible"] = True

    record = {
        "memory_id": updated.get("memory_id", ""),
        "previous_layer": updated.get("memory_layer", "short_term"),
        "current_layer": "decayed",
        "decay_reason": reasons,
        "importance_score": updated["importance_score"],
        "previous_score": decay_info["previous_score"],
        "decay_amount": decay_info["decay_amount"],
        "timestamp": updated["decayed_at"],
    }

    save_decay_record(record)
    save_lifecycle_log({
        "action": "decay",
        "memory_id": record["memory_id"],
        "previous_layer": record["previous_layer"],
        "current_layer": "decayed",
        "decay_reason": reasons,
        "importance_score": record["importance_score"],
        "timestamp": record["timestamp"],
    })

    logger.info(
        "decay_memory  id=%s  score=%.4f → %.4f",
        record["memory_id"][:20],
        decay_info["previous_score"],
        decay_info["decayed_score"],
    )
    return record


def process_memory_lifecycle(
    memory: dict,
    all_memories: list[dict],
) -> dict:
    """단일 Memory의 lifecycle을 평가하고 promote/decay를 수행한다."""
    evolution = track_memory_evolution(memory, all_memories)
    updated = apply_temporal_importance_update(memory, evolution)

    result: dict = {
        "memory_id": updated.get("memory_id", ""),
        "evolution": evolution,
        "action": "keep",
    }

    if should_decay(updated, evolution):
        decay_record = decay_memory(updated, evolution)
        if decay_record:
            result["action"] = "decay"
            result["decay_record"] = decay_record
            return result

    if should_promote(updated, evolution):
        promote_record = promote_memory(updated, evolution)
        if promote_record:
            result["action"] = "promote"
            result["promotion_record"] = promote_record
            return result

    return result


def build_temporal_context(
    layers: dict[str, list[dict]],
    max_per_layer: int = 3,
) -> str:
    """Layer별 Temporal Context 문자열을 생성한다."""
    parts: list[str] = ["[Temporal Market Memory]"]

    labels = {
        "short_term": "Short-term",
        "mid_term": "Mid-term",
        "long_term": "Long-term",
    }

    for layer, label in labels.items():
        mems = layers.get(layer, [])
        if not mems:
            continue
        sorted_mems = sorted(
            mems,
            key=lambda m: m.get("importance_score", 0),
            reverse=True,
        )
        parts.append(f"[{label}]")
        for m in sorted_mems[:max_per_layer]:
            summary = m.get("summary", m.get("event_summary", ""))[:80]
            stage = m.get("evolution_stage", "")
            score = m.get("importance_score", 0)
            parts.append(f"- [score={score:.2f}] {summary}")
            if stage:
                parts.append(f"  (stage: {stage})")
        parts.append("")

    context = "\n".join(parts)
    logger.info("Temporal Context 생성  len=%d", len(context))
    return context


def save_lifecycle_log(entry: dict, output_dir: Path | None = None) -> Path:
    out = output_dir or (DEFAULT_TEMPORAL_DIR / "lifecycle_logs")
    out.mkdir(parents=True, exist_ok=True)
    filepath = out / "lifecycle_log.json"

    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, Exception):
            existing = []

    existing.append(entry)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    logger.info("lifecycle log 저장  action=%s", entry.get("action"))
    return filepath


def save_promotion_record(record: dict, output_dir: Path | None = None) -> Path:
    out = output_dir or (DEFAULT_TEMPORAL_DIR / "promotions")
    out.mkdir(parents=True, exist_ok=True)

    mem_id = record.get("memory_id", "unknown")[:30].replace(" ", "_")
    filepath = out / f"{mem_id}_promotion.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    logger.info("promotion 저장  %s", filepath.name)
    return filepath


def save_decay_record(record: dict, output_dir: Path | None = None) -> Path:
    out = output_dir or (DEFAULT_TEMPORAL_DIR / "decays")
    out.mkdir(parents=True, exist_ok=True)

    mem_id = record.get("memory_id", "unknown")[:30].replace(" ", "_")
    filepath = out / f"{mem_id}_decay.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    logger.info("decay 저장  %s", filepath.name)
    return filepath
