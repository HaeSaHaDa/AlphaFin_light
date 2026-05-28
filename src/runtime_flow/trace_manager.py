"""Runtime trace — trace_id 기준만 조회 (fallback 없음)."""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UNIFIED_RESULTS = PROJECT_ROOT / "data" / "unified_engine" / "final_results"
UNIFIED_TRACES = PROJECT_ROOT / "data" / "unified_engine" / "traces"
STOCK_CHAIN_DIR = PROJECT_ROOT / "data" / "stock_chain"
EVAL_REPORTS = PROJECT_ROOT / "data" / "evaluation_suite" / "reports"


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    import json
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (json.JSONDecodeError, OSError):
        return None


def get_unified_result(trace_id: str) -> dict | None:
    if not trace_id:
        return None
    return _load_json(UNIFIED_RESULTS / f"{trace_id}_result.json")


def get_trace(trace_id: str) -> dict | None:
    if not trace_id:
        return None
    return _load_json(UNIFIED_TRACES / f"{trace_id}_trace.json")


def get_stock_chain(trace_id: str) -> dict | None:
    if not trace_id:
        return None
    return _load_json(STOCK_CHAIN_DIR / f"{trace_id}_chain.json")


def get_evaluation_report(trace_id: str) -> dict | None:
    """trace_id 일치 report만 반환 (latest fallback 없음)."""
    if not trace_id or not EVAL_REPORTS.exists():
        return None
    for fp in EVAL_REPORTS.glob("*_report.json"):
        data = _load_json(fp)
        if data and data.get("trace_id") == trace_id:
            return data
    return None


def trace_exists(trace_id: str) -> bool:
    return get_unified_result(trace_id) is not None
