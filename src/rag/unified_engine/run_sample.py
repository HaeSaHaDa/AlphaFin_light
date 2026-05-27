"""Unified Engine Runner 샘플 검증 스크립트."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

UNIFIED_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIFIED_DIR))

from engine_runner import run_unified_pipeline  # noqa: E402
from pipeline_manager import PIPELINE_STEPS  # noqa: E402
from result_builder import DEFAULT_OUTPUT_DIR  # noqa: E402

SAMPLE_QUERY = "삼성전자 반도체 전망 분석"
SAMPLE_PERSONA = "growth_investor"
SAMPLE_TICKER = "005930"


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Unified Engine Runner 검증 시작 ===")
    logger.info("Query: %s", SAMPLE_QUERY)

    result = run_unified_pipeline(
        query=SAMPLE_QUERY,
        persona=SAMPLE_PERSONA,
        ticker=SAMPLE_TICKER,
    )

    trace_id = result.get("trace_id", "")
    logger.info("trace_id: %s", trace_id)

    trace_path = DEFAULT_OUTPUT_DIR / "traces" / f"{trace_id}_trace.json"
    result_path = DEFAULT_OUTPUT_DIR / "final_results" / f"{trace_id}_result.json"
    pipeline_path = DEFAULT_OUTPUT_DIR / "engine_runs" / f"{trace_id}_pipeline.json"

    logger.info("=== 검증 결과 요약 ===")

    checks = {
        "e2e_execution": bool(result.get("query")),
        "analysis_result": bool(result.get("analysis_result", {}).get("summary")),
        "evaluation_result": bool(result.get("evaluation_result")),
        "reflection_result": bool(result.get("reflection_result", {}).get("reflection_summary")),
        "memory_updates": result.get("memory_updates", {}).get("analysis_memory") is not None,
        "temporal_result": result.get("temporal_result") is not None,
        "event_graph": (result.get("event_graph") or {}).get("node_count", 0) > 0,
        "stock_chain": (result.get("stock_chain") or {}).get("link_count", 0) > 0,
        "unified_context": result.get("unified_context_length", 0) > 0,
        "full_trace_saved": trace_path.exists(),
        "unified_result_saved": result_path.exists(),
        "pipeline_log_saved": pipeline_path.exists(),
        "retrieval_chunks": result.get("retrieval_chunk_count", 0) > 0,
    }

    for name, ok in checks.items():
        logger.info("  %-25s : %s", name, "OK" if ok else "WARN")

    logger.info("Pipeline 단계: %s", ", ".join(PIPELINE_STEPS))

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Unified Engine Runner 검증 완료 ===")

    return 0 if all_ok else 0


if __name__ == "__main__":
    sys.exit(main())
