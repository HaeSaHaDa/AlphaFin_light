"""Unified Engine 결과 및 Trace 저장 모듈."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "unified_engine"


def build_unified_result(state: dict) -> dict:
    """Pipeline 상태에서 Unified Result dict를 생성한다."""
    result = {
        "trace_id": state.get("trace_id", ""),
        "query": state.get("query", ""),
        "persona": state.get("persona", ""),
        "ticker": state.get("ticker", ""),
        "analysis_result": state.get("analysis_result", {}),
        "evaluation_result": state.get("evaluation_result", {}),
        "reflection_result": state.get("reflection_result", {}),
        "memory_updates": {
            "analysis_memory": state.get("analysis_memory"),
            "layered_memory": state.get("layered_save_result"),
            "importance": state.get("importance_result"),
        },
        "temporal_result": state.get("temporal_result"),
        "event_graph": state.get("event_graph"),
        "stock_chain": state.get("stock_chain"),
        "unified_context_length": state.get("unified_context_length", 0),
        "retrieval_chunk_count": len(state.get("chunks", [])),
        "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    logger.info("Unified Result 생성  trace_id=%s", result["trace_id"])
    return result


def save_unified_result(
    result: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path:
    """Unified Result를 JSON으로 저장한다."""
    out = Path(output_dir) if output_dir else (DEFAULT_OUTPUT_DIR / "final_results")
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        trace_id = result.get("trace_id", "run")
        filename = f"{trace_id}_result.json"

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logger.info("Unified Result 저장  %s", filepath)
    return filepath


def save_full_trace(
    state: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path:
    """Full Engine Trace를 JSON으로 저장한다."""
    out = Path(output_dir) if output_dir else (DEFAULT_OUTPUT_DIR / "traces")
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        trace_id = state.get("trace_id", "trace")
        filename = f"{trace_id}_trace.json"

    trace = {
        "trace_id": state.get("trace_id", ""),
        "query": state.get("query", ""),
        "persona": state.get("persona", ""),
        "ticker": state.get("ticker", ""),
        "started_at": state.get("started_at", ""),
        "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "steps": state.get("trace_log", []),
        "retrieval_summary": {
            "chunk_count": len(state.get("chunks", [])),
            "max_score": max(
                (c.get("score", 0) for c in state.get("chunks", [])),
                default=0,
            ),
        },
        "reflection_summary": state.get("reflection_result", {}).get(
            "reflection_summary", "",
        )[:200],
        "temporal_action": state.get("temporal_result", {}).get("action", ""),
        "stock_chain_links": len(
            (state.get("stock_chain") or {}).get("links", []),
        ),
    }

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)

    logger.info("Full Trace 저장  %s  steps=%d", filepath.name, len(trace["steps"]))
    return filepath


def save_pipeline_log(state: dict) -> Path:
    """Pipeline 실행 로그를 engine_runs에 저장한다."""
    out = DEFAULT_OUTPUT_DIR / "engine_runs"
    out.mkdir(parents=True, exist_ok=True)

    trace_id = state.get("trace_id", "run")
    filepath = out / f"{trace_id}_pipeline.json"

    log_entry = {
        "trace_id": trace_id,
        "query": state.get("query", ""),
        "status": "completed",
        "steps_completed": len(state.get("trace_log", [])),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, Exception):
            existing = []

    if isinstance(existing, dict):
        existing = [existing]
    existing.append(log_entry)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    logger.info("Pipeline log 저장  %s", filepath.name)
    return filepath
