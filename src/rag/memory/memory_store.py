"""Analysis Memory 저장 및 관리 모듈."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ANALYSIS_DIR = PROJECT_ROOT / "data" / "memory" / "analysis_memory"


def _memory_evidence(chunks: list[dict]) -> list[dict]:
    fields = (
        "chunk_id",
        "document_type",
        "ticker",
        "score",
        "merge_score",
        "source_priority",
        "source",
        "title",
        "report_name",
        "report_type",
        "report_date",
        "section_name",
        "published_at",
        "url",
        "document_url",
        "text",
        "chunk_text",
        "metadata_json",
    )
    return [
        {field: chunk.get(field) for field in fields if chunk.get(field) is not None}
        for chunk in chunks
        if isinstance(chunk, dict)
    ]


def build_analysis_memory(analysis_result: dict) -> dict:
    """분석 결과를 Memory 형태로 변환한다.

    Args:
        analysis_result: Character/Financial Analysis 결과 dict.

    Returns:
        Analysis Memory dict.
    """
    memory = {
        "memory_type": "analysis_memory",
        "query": analysis_result.get("query", ""),
        "ticker": analysis_result.get("ticker", ""),
        "keywords": analysis_result.get("keywords", []),
        "persona": analysis_result.get("persona", "default"),
        "bullish_factors": analysis_result.get("bullish_factors", []),
        "bearish_factors": analysis_result.get("bearish_factors", []),
        "risks": analysis_result.get("risks", []),
        "summary": analysis_result.get("summary", ""),
        "referenced_chunks": _memory_evidence(
            analysis_result.get("referenced_chunks", []),
        ),
        "model": analysis_result.get("model", ""),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    logger.info(
        "Analysis Memory 생성  query='%s'  persona=%s",
        memory["query"][:30], memory["persona"],
    )
    return memory


def save_analysis_memory(
    memory: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path | None:
    """Analysis Memory를 JSON 파일에 추가 저장한다.

    기존 파일이 있으면 목록에 추가, 없으면 새로 생성한다.
    """
    out = Path(output_dir) if output_dir else DEFAULT_ANALYSIS_DIR
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        persona = memory.get("persona", "default")
        filename = f"{persona}_memories.json"

    filepath = out / filename

    memories: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                memories = json.load(f)
        except (json.JSONDecodeError, Exception):
            logger.warning("기존 Memory 파일 파싱 실패, 새로 생성  %s", filepath)
            memories = []

    memories.append(memory)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False, indent=2)

    logger.info(
        "Analysis Memory 저장  %s  총=%d건", filepath.name, len(memories),
    )
    return filepath


def load_analysis_memories(
    persona: str | None = None,
    output_dir: Path | str | None = None,
) -> list[dict]:
    """저장된 Analysis Memory를 로드한다.

    Args:
        persona: 특정 Persona의 Memory만 로드. None이면 전체.
        output_dir: Memory 저장 디렉토리.

    Returns:
        Memory dict 목록.
    """
    out = Path(output_dir) if output_dir else DEFAULT_ANALYSIS_DIR
    if not out.exists():
        return []

    all_memories: list[dict] = []

    if persona:
        filepath = out / f"{persona}_memories.json"
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    all_memories = json.load(f)
            except (json.JSONDecodeError, Exception):
                logger.warning("Memory 파일 파싱 실패  %s", filepath)
    else:
        for fp in out.glob("*_memories.json"):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_memories.extend(data)
            except (json.JSONDecodeError, Exception):
                logger.warning("Memory 파일 파싱 실패  %s", fp)

    logger.info(
        "Analysis Memory 로드  persona=%s  총=%d건",
        persona or "all", len(all_memories),
    )
    return all_memories
