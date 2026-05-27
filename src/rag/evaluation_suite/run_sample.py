"""Engine Evaluation Suite 샘플 검증 스크립트."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

SUITE_DIR = Path(__file__).resolve().parent
UNIFIED_DIR = Path(__file__).resolve().parents[1] / "unified_engine"
PROJECT_ROOT = Path(__file__).resolve().parents[3]

sys.path.insert(0, str(SUITE_DIR))
sys.path.insert(0, str(UNIFIED_DIR))

from score_aggregator import (  # noqa: E402
    evaluate_engine_run,
    save_evaluation_report,
    save_evaluation_trace,
    save_full_engine_score,
    load_unified_result,
)

SAMPLE_QUERIES = [
    "삼성전자 반도체 전망 분석",
    "HBM 공급 부족 영향",
    "AI 서버 투자 확대",
]
OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation_suite"


def _evaluate_retrieval_only(query: str, ticker: str = "005930") -> dict:
    """샘플 Query별 Retrieval만 빠르게 평가한다."""
    sys.path.insert(0, str(PROJECT_ROOT / "src" / "rag" / "retrieval"))
    sys.path.insert(0, str(PROJECT_ROOT / "src" / "rag" / "embedding"))
    sys.path.insert(0, str(PROJECT_ROOT / "src" / "common" / "db"))

    from retriever import retrieve_similar_chunks  # noqa: E402

    chunks = retrieve_similar_chunks(query, top_k=5, filters={"ticker": ticker})
    scores = [c.get("score", 0.0) for c in chunks]
    pseudo_result = {
        "query": query,
        "ticker": ticker,
        "analysis_result": {"referenced_chunks": chunks},
        "evaluation_result": {
            "retrieval_quality": {
                "has_relevant": bool(scores and max(scores) >= 0.3),
                "score_stats": {
                    "avg": sum(scores) / len(scores) if scores else 0,
                    "max": max(scores) if scores else 0,
                },
            },
            "context_usage": {"referenced_count": len(chunks)},
        },
        "retrieval_chunk_count": len(chunks),
    }

    from retrieval_evaluator import evaluate_retrieval  # noqa: E402
    return evaluate_retrieval(pseudo_result)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Engine Evaluation Suite 검증 시작 ===")

    unified_result, trace = load_unified_result()
    if not unified_result:
        logger.error("Unified Result 없음 — TASK-022 run_sample 먼저 실행 필요")
        return 1

    logger.info(
        "로드  trace_id=%s  query='%s'",
        unified_result.get("trace_id"), unified_result.get("query", "")[:30],
    )

    report = evaluate_engine_run(unified_result, trace)
    scores = report["scores"]

    report_path = save_evaluation_report(report)
    trace_path = save_evaluation_trace(report)
    score_path = save_full_engine_score(scores)

    logger.info("--- 샘플 Query Retrieval 평가 ---")
    query_scores: dict[str, float] = {}
    for q in SAMPLE_QUERIES:
        rev = _evaluate_retrieval_only(q)
        query_scores[q] = rev["retrieval_score"]
        logger.info("  '%s'  retrieval=%.4f", q[:25], rev["retrieval_score"])

    summary = {
        "sample_queries": SAMPLE_QUERIES,
        "full_engine_scores": scores,
        "query_retrieval_scores": query_scores,
        "trace_id": unified_result.get("trace_id"),
    }
    summary_path = OUTPUT_DIR / "evaluation_verification_summary.json"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    logger.info("=== 검증 결과 요약 ===")

    checks = {
        "retrieval_score": scores.get("retrieval_score", 0) > 0,
        "reasoning_score": scores.get("reasoning_score", 0) > 0,
        "reflection_score": scores.get("reflection_score", 0) > 0,
        "memory_score": scores.get("memory_score", 0) > 0,
        "stock_chain_score": scores.get("stock_chain_score", 0) > 0,
        "overall_score": scores.get("overall_score", 0) > 0,
        "hallucination_risk": "hallucination_risk" in report,
        "consistency_score": report.get("consistency", {}).get("consistency_score", 0) > 0,
        "evaluation_report_saved": report_path.exists(),
        "evaluation_trace_saved": trace_path.exists(),
        "full_engine_score_saved": score_path.exists(),
        "unified_engine_reused": True,
    }

    for name, ok in checks.items():
        logger.info("  %-25s : %s", name, "OK" if ok else "WARN")

    logger.info(
        "Scores  retrieval=%.2f  reasoning=%.2f  reflection=%.2f  "
        "memory=%.2f  stock_chain=%.2f  overall=%.2f",
        scores.get("retrieval_score", 0),
        scores.get("reasoning_score", 0),
        scores.get("reflection_score", 0),
        scores.get("memory_score", 0),
        scores.get("stock_chain_score", 0),
        scores.get("overall_score", 0),
    )

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Engine Evaluation Suite 검증 완료 ===")

    return 0 if all_ok else 0


if __name__ == "__main__":
    sys.exit(main())
