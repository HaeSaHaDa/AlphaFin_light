"""Layer별 Memory 저장 모듈."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from memory_classifier import (
    classify_memory_layer,
    calculate_importance_score,
    is_expired,
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASE_DIR = PROJECT_ROOT / "data" / "layered_memory"

LAYER_ORDER = ["short_term", "mid_term", "long_term"]
LAYER_RANK = {name: i for i, name in enumerate(LAYER_ORDER, start=1)}


def _get_layer_dir(layer: str, base_dir: Path | None = None) -> Path:
    base = base_dir or DEFAULT_BASE_DIR
    return base / layer


def _layer_filepath(layer: str, persona: str, base_dir: Path | None = None) -> Path:
    layer_dir = _get_layer_dir(layer, base_dir)
    layer_dir.mkdir(parents=True, exist_ok=True)
    return layer_dir / f"{persona}_{layer}.json"


def remove_memory_from_layer(
    memory_id: str,
    layer: str,
    base_dir: Path | str | None = None,
) -> bool:
    """지정 layer JSON 파일들에서 memory_id 항목을 제거한다."""
    if not memory_id:
        return False
    layer_dir = _get_layer_dir(layer, Path(base_dir) if base_dir else None)
    if not layer_dir.exists():
        return False
    changed = False
    for fp in layer_dir.glob("*.json"):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, list):
            continue
        filtered = [m for m in data if m.get("memory_id") != memory_id]
        if len(filtered) == len(data):
            continue
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)
        changed = True
        logger.info("memory 이동 — 제거  layer=%s  id=%s  file=%s", layer, memory_id[:24], fp.name)
    return changed


def remove_memory_from_all_layers(
    memory_id: str,
    *,
    except_layer: str | None = None,
    base_dir: Path | str | None = None,
) -> list[str]:
    """모든 layer에서 memory_id 제거 (except_layer 제외)."""
    removed: list[str] = []
    for layer in LAYER_ORDER:
        if layer == except_layer:
            continue
        if remove_memory_from_layer(memory_id, layer, base_dir=base_dir):
            removed.append(layer)
    return removed


def upsert_memory_in_layer(
    memory: dict,
    layer: str | None = None,
    base_dir: Path | str | None = None,
) -> Path:
    """단일 layer 파일에 memory_id 기준 upsert."""
    target = layer or memory.get("memory_layer") or classify_memory_layer(memory)
    memory["memory_layer"] = target
    persona = memory.get("persona", "default")
    filepath = _layer_filepath(target, persona, base_dir)

    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing = []

    mem_id = memory.get("memory_id", "")
    if mem_id:
        existing = [m for m in existing if m.get("memory_id") != mem_id]
    existing.append(memory)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    logger.info(
        "Layer upsert  layer=%s  id=%s  file=%s  count=%d",
        target,
        str(mem_id)[:24],
        filepath.name,
        len(existing),
    )
    return filepath


def move_memory_to_layer(
    memory: dict,
    target_layer: str,
    base_dir: Path | str | None = None,
) -> dict:
    """복사가 아닌 이동: 이전 layer 전부 제거 후 target layer에만 저장."""
    mem_id = memory.get("memory_id", "")
    if not mem_id:
        logger.warning("move_memory_to_layer — memory_id 없음, 이동 스킵")
        return {}

    previous = memory.get("memory_layer", "short_term")
    removed_from = remove_memory_from_all_layers(mem_id, base_dir=base_dir)

    memory["memory_layer"] = target_layer
    memory["previous_layer"] = previous
    memory["retention_action"] = "promote" if LAYER_RANK.get(target_layer, 0) > LAYER_RANK.get(previous, 0) else "demote"
    memory["moved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    upsert_memory_in_layer(memory, target_layer, base_dir=base_dir)

    logger.info(
        "move_memory  %s → %s  id=%s  removed_from=%s",
        previous,
        target_layer,
        mem_id[:24],
        removed_from,
    )
    return {
        "memory_id": mem_id,
        "previous_layer": previous,
        "current_layer": target_layer,
        "removed_from_layers": removed_from,
    }


def collapse_layers_for_display(
    layers: dict[str, list[dict]],
) -> dict[str, list[dict]]:
    """동일 memory_id가 여러 layer에 있으면 memory_layer(또는 상위 layer)만 유지."""
    best: dict[str, tuple[str, dict]] = {}

    for layer_name in LAYER_ORDER:
        for item in layers.get(layer_name) or []:
            if not isinstance(item, dict):
                continue
            key = item.get("memory_id") or _content_fingerprint(item)
            declared = item.get("memory_layer") or layer_name
            rank = LAYER_RANK.get(declared, LAYER_RANK.get(layer_name, 0))
            if key not in best or rank >= LAYER_RANK.get(best[key][0], 0):
                best[key] = (declared, {**item, "memory_layer": declared})

    collapsed: dict[str, list[dict]] = {name: [] for name in LAYER_ORDER}
    for _key, (layer_name, item) in best.items():
        if layer_name not in collapsed:
            layer_name = "short_term"
        collapsed[layer_name].append(item)
    return collapsed


def _content_fingerprint(item: dict) -> str:
    q = (item.get("query") or "").strip()
    s = (item.get("summary") or item.get("event_summary") or "")[:80].strip()
    return f"fp:{q}::{s}"


def repair_layer_duplicates(base_dir: Path | str | None = None) -> int:
    """디스크 상 cross-layer 중복을 이동 규칙으로 정리한다."""
    best: dict[str, dict] = {}
    for layer in LAYER_ORDER:
        for m in load_layer_memories(layer, base_dir=base_dir, exclude_expired=False):
            key = m.get("memory_id")
            if not key:
                continue
            declared = m.get("memory_layer") or layer
            if key not in best:
                best[key] = {**m, "memory_layer": declared}
                continue
            cur = best[key].get("memory_layer", "short_term")
            if LAYER_RANK.get(declared, 0) >= LAYER_RANK.get(cur, 0):
                best[key] = {**m, "memory_layer": declared}

    for key, m in best.items():
        move_memory_to_layer(m, m["memory_layer"], base_dir=base_dir)
    return len(best)


def save_layered_memory(
    memory: dict,
    base_dir: Path | str | None = None,
    filename: str | None = None,
) -> dict:
    """Memory를 분류하여 해당 Layer에 저장한다.

    Returns:
        {
            "layer", "importance_score", "filepath",
            "memory_count"
        }
    """
    base = Path(base_dir) if base_dir else DEFAULT_BASE_DIR

    layer = classify_memory_layer(memory)
    score = calculate_importance_score(memory)
    memory["memory_layer"] = layer
    memory["importance_score"] = score

    mem_id = memory.get("memory_id", "")
    if mem_id:
        remove_memory_from_all_layers(mem_id, base_dir=base)

    filepath = upsert_memory_in_layer(memory, layer, base_dir=base)

    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing = []

    result = {
        "layer": layer,
        "importance_score": score,
        "filepath": str(filepath),
        "memory_count": len(existing),
    }

    logger.info(
        "Layered Memory 저장  layer=%s  score=%.4f  파일=%s  총=%d건",
        layer, score, filepath.name, len(existing),
    )
    return result


def load_layer_memories(
    layer: str,
    base_dir: Path | str | None = None,
    exclude_expired: bool = True,
) -> list[dict]:
    """특정 Layer의 Memory를 로드한다.

    Args:
        layer: "short_term" | "mid_term" | "long_term".
        base_dir: 기본 디렉토리.
        exclude_expired: 만료된 Memory 제외 여부.

    Returns:
        Memory dict 목록.
    """
    base = Path(base_dir) if base_dir else DEFAULT_BASE_DIR
    layer_dir = _get_layer_dir(layer, base)

    if not layer_dir.exists():
        return []

    all_memories: list[dict] = []
    for fp in layer_dir.glob("*.json"):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_memories.extend(data)
        except (json.JSONDecodeError, Exception):
            logger.warning("파일 파싱 실패  %s", fp)

    if exclude_expired:
        active = [m for m in all_memories if not is_expired(m, layer)]
    else:
        active = all_memories

    logger.info(
        "Layer 로드  layer=%s  전체=%d  활성=%d",
        layer, len(all_memories), len(active),
    )
    return active


def load_all_layers(
    base_dir: Path | str | None = None,
    exclude_expired: bool = True,
) -> dict[str, list[dict]]:
    """전체 Layer의 Memory를 로드한다.

    Returns:
        {"short_term": [...], "mid_term": [...], "long_term": [...]}
    """
    layers = {}
    for layer in ["short_term", "mid_term", "long_term"]:
        layers[layer] = load_layer_memories(
            layer, base_dir=base_dir, exclude_expired=exclude_expired,
        )

    total = sum(len(v) for v in layers.values())
    logger.info(
        "전체 Layer 로드  short=%d  mid=%d  long=%d  총=%d",
        len(layers["short_term"]),
        len(layers["mid_term"]),
        len(layers["long_term"]),
        total,
    )
    return layers
