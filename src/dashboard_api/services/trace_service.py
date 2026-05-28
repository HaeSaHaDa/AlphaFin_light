"""Trace 및 Unified Result JSON 로드."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
UNIFIED_RESULTS = PROJECT_ROOT / "data" / "unified_engine" / "final_results"
UNIFIED_TRACES = PROJECT_ROOT / "data" / "unified_engine" / "traces"
EVAL_REPORTS = PROJECT_ROOT / "data" / "evaluation_suite" / "reports"
STOCK_CHAIN_DIR = PROJECT_ROOT / "data" / "stock_chain"
LAYERED_DIR = PROJECT_ROOT / "data" / "layered_memory"


def load_json_file(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("JSON 로드 실패  %s  %s", path, e)
        return None


def get_latest_unified_result() -> dict | None:
    if not UNIFIED_RESULTS.exists():
        return None
    files = sorted(UNIFIED_RESULTS.glob("*_result.json"), reverse=True)
    if not files:
        return None
    data = load_json_file(files[0])
    return data if isinstance(data, dict) else None


def get_unified_result_by_trace(trace_id: str) -> dict | None:
    path = UNIFIED_RESULTS / f"{trace_id}_result.json"
    data = load_json_file(path)
    return data if isinstance(data, dict) else None


def get_trace_by_id(trace_id: str) -> dict | None:
    path = UNIFIED_TRACES / f"{trace_id}_trace.json"
    data = load_json_file(path)
    return data if isinstance(data, dict) else None


def get_latest_trace() -> dict | None:
    result = get_latest_unified_result()
    if not result:
        return None
    return get_trace_by_id(result.get("trace_id", ""))


def find_evaluation_report(trace_id: str) -> dict | None:
    """trace_id 일치 report만 (latest fallback 제거)."""
    if not trace_id or not EVAL_REPORTS.exists():
        return None
    for fp in EVAL_REPORTS.glob("*_report.json"):
        data = load_json_file(fp)
        if isinstance(data, dict) and data.get("trace_id") == trace_id:
            return data
    return None


def load_stock_chain_file(trace_id: str) -> dict | None:
    """해당 trace_id chain만 (다른 종목 chain fallback 제거)."""
    if not trace_id:
        return None
    path = STOCK_CHAIN_DIR / f"{trace_id}_chain.json"
    data = load_json_file(path)
    return data if isinstance(data, dict) else None


def load_layer_memories(layer: str) -> list[dict]:
    layer_dir = LAYERED_DIR / layer
    if not layer_dir.exists():
        return []
    memories: list[dict] = []
    for fp in layer_dir.glob("*.json"):
        data = load_json_file(fp)
        if isinstance(data, list):
            memories.extend(data)
    return memories
