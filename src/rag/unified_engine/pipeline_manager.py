"""Unified Engine Pipeline 단계 관리 모듈."""
from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODULE_PATHS = {
    "db": PROJECT_ROOT / "src" / "common" / "db",
    "retrieval": PROJECT_ROOT / "src" / "rag" / "retrieval",
    "context": PROJECT_ROOT / "src" / "rag" / "context",
    "embedding": PROJECT_ROOT / "src" / "rag" / "embedding",
    "evaluation": PROJECT_ROOT / "src" / "rag" / "evaluation",
    "character": PROJECT_ROOT / "src" / "rag" / "character",
    "memory": PROJECT_ROOT / "src" / "rag" / "memory",
    "event_graph": PROJECT_ROOT / "src" / "rag" / "event_graph",
    "reflection": PROJECT_ROOT / "src" / "rag" / "reflection",
    "layered_memory": PROJECT_ROOT / "src" / "rag" / "layered_memory",
    "memory_importance": PROJECT_ROOT / "src" / "rag" / "memory_importance",
    "temporal_memory": PROJECT_ROOT / "src" / "rag" / "temporal_memory",
    "stock_chain": PROJECT_ROOT / "src" / "rag" / "stock_chain",
}

PIPELINE_STEPS = [
    "retrieval",
    "context_assembly",
    "unified_context",
    "character_analysis",
    "evaluation",
    "reflection",
    "memory_save",
    "importance_update",
    "temporal_tracking",
    "event_graph",
    "stock_chain",
    "result_save",
]

_paths_initialized = False


def setup_module_paths() -> None:
    """모든 RAG 모듈 경로를 sys.path에 등록한다."""
    global _paths_initialized
    if _paths_initialized:
        return

    order = [
        "db", "embedding", "retrieval", "context", "evaluation",
        "memory", "event_graph", "reflection", "layered_memory",
        "memory_importance", "temporal_memory", "stock_chain",
        "character",
    ]
    for key in order:
        path = str(MODULE_PATHS[key])
        if path not in sys.path:
            sys.path.insert(0, path)

    _paths_initialized = True
    logger.info("모듈 경로 등록 완료  modules=%d", len(order))


def create_pipeline_state(
    query: str,
    persona: str = "growth_investor",
    ticker: str = "005930",
    trace_id: str | None = None,
) -> dict[str, Any]:
    """Pipeline 초기 상태 dict를 생성한다."""
    if trace_id is None:
        trace_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    return {
        "query": query,
        "persona": persona,
        "ticker": ticker,
        "trace_id": trace_id,
        "trace_log": [],
        "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def log_step(
    state: dict[str, Any],
    step: str,
    status: str = "ok",
    summary: str = "",
    details: dict | None = None,
) -> None:
    """Pipeline trace에 단계 기록을 추가한다."""
    entry = {
        "step": step,
        "status": status,
        "summary": summary,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    if details:
        entry["details"] = details

    state.setdefault("trace_log", []).append(entry)
    logger.info("Pipeline  [%s] %s  %s", step, status, summary[:60])
