"""Reflection 저장 및 조회 모듈."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REFLECTION_DIR = PROJECT_ROOT / "data" / "reflection"


def save_reflection(
    reflection: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path | None:
    """Reflection 결과를 JSON에 추가 저장한다."""
    out = Path(output_dir) if output_dir else DEFAULT_REFLECTION_DIR
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        persona = reflection.get("persona", "default")
        filename = f"{persona}_reflections.json"

    filepath = out / filename

    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, Exception):
            logger.warning("기존 파일 파싱 실패, 새로 생성  %s", filepath)
            existing = []

    existing.append(reflection)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    logger.info(
        "Reflection 저장  %s  총=%d건", filepath.name, len(existing),
    )
    return filepath


def load_reflections(
    persona: str | None = None,
    output_dir: Path | str | None = None,
) -> list[dict]:
    """저장된 Reflection을 로드한다."""
    out = Path(output_dir) if output_dir else DEFAULT_REFLECTION_DIR
    if not out.exists():
        return []

    all_reflections: list[dict] = []

    if persona:
        filepath = out / f"{persona}_reflections.json"
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    all_reflections = json.load(f)
            except (json.JSONDecodeError, Exception):
                logger.warning("파일 파싱 실패  %s", filepath)
    else:
        for fp in out.glob("*_reflections.json"):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_reflections.extend(data)
            except (json.JSONDecodeError, Exception):
                logger.warning("파일 파싱 실패  %s", fp)

    logger.info(
        "Reflection 로드  persona=%s  총=%d건",
        persona or "all", len(all_reflections),
    )
    return all_reflections


def build_reflection_context(reflections: list[dict], max_items: int = 3) -> str:
    """Reflection을 Prompt Context 문자열로 변환한다."""
    if not reflections:
        return ""

    parts: list[str] = ["[Reflection]"]

    sorted_refs = sorted(
        reflections,
        key=lambda r: r.get("timestamp", ""),
        reverse=True,
    )

    for ref in sorted_refs[:max_items]:
        ts = ref.get("timestamp", "")
        summary = ref.get("reflection_summary", "")
        parts.append(f"- ({ts}) {summary[:100]}")

        missing = ref.get("missing_risks", [])
        if missing:
            parts.append(f"  주의: {', '.join(missing[:2])}")

    parts.append("")
    context = "\n".join(parts)

    logger.info(
        "Reflection Context 생성  items=%d  len=%d",
        min(len(sorted_refs), max_items), len(context),
    )
    return context
