"""Layer별 Memory 저장 모듈."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from memory_classifier import (
    classify_memory_layer,
    calculate_importance_score,
    is_expired,
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASE_DIR = PROJECT_ROOT / "data" / "layered_memory"


def _get_layer_dir(layer: str, base_dir: Path | None = None) -> Path:
    base = base_dir or DEFAULT_BASE_DIR
    return base / layer


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

    layer_dir = _get_layer_dir(layer, base)
    layer_dir.mkdir(parents=True, exist_ok=True)

    if filename is None:
        persona = memory.get("persona", "default")
        filename = f"{persona}_{layer}.json"

    filepath = layer_dir / filename

    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, Exception):
            logger.warning("기존 파일 파싱 실패, 새로 생성  %s", filepath)
            existing = []

    existing.append(memory)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

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
