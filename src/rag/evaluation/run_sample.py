"""삼성전자 관련 샘플 Query 금융 분석 평가 검증 스크립트."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
RETRIEVAL_MODULE = PROJECT_ROOT / "src" / "rag" / "retrieval"
CONTEXT_MODULE = PROJECT_ROOT / "src" / "rag" / "context"
EMBEDDING_MODULE = PROJECT_ROOT / "src" / "rag" / "embedding"
ANALYSIS_MODULE = PROJECT_ROOT / "src" / "rag" / "analysis"
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(CONTEXT_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))
sys.path.insert(0, str(ANALYSIS_MODULE))

from retriever import retrieve_similar_chunks  # noqa: E402
from assembler import assemble_context  # noqa: E402
from analyzer import analyze_financial_query  # noqa: E402
from evaluator import (  # noqa: E402
    evaluate_analysis_result,
    save_evaluation_json,
)

SAMPLE_QUERY = "삼성전자 반도체 전망 분석"


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== 금융 분석 평가 검증 시작 ===")

    # 1. Retrieval
    logger.info("--- 1. Retrieval ---")
    chunks = retrieve_similar_chunks(
        SAMPLE_QUERY, top_k=5, filters={"ticker": "005930"},
    )
    logger.info("Retrieval 결과: %d건", len(chunks))
    if not chunks:
        logger.error("Retrieval 결과 없음")
        return 1

    for c in chunks:
        logger.info(
            "  chunk_id=%s  score=%.4f  type=%s",
            c["chunk_id"], c["score"], c["document_type"],
        )

    # 2. Context Assembly
    logger.info("--- 2. Context Assembly ---")
    ctx = assemble_context(SAMPLE_QUERY, chunks)
    prompt_context = ctx["prompt_context"]
    logger.info("Context 길이: %d자", len(prompt_context))

    # 3. Financial Analysis
    logger.info("--- 3. Financial Analysis ---")
    analysis = analyze_financial_query(
        SAMPLE_QUERY, top_k=5, filters={"ticker": "005930"},
    )
    if analysis.get("error"):
        logger.error("분석 실패: %s", analysis["error"])
        return 1

    logger.info("bullish=%d  bearish=%d  risks=%d",
        len(analysis.get("bullish_factors", [])),
        len(analysis.get("bearish_factors", [])),
        len(analysis.get("risks", [])),
    )

    # 4. Evaluation
    logger.info("--- 4. Evaluation ---")
    evaluation = evaluate_analysis_result(analysis, chunks, prompt_context)

    logger.info("--- 평가 결과 상세 ---")

    rq = evaluation["retrieval_quality"]
    logger.info("Retrieval 품질:")
    logger.info("  chunks=%d  max=%.4f  avg=%.4f  relevant=%s",
        rq["chunk_count"], rq["score_stats"]["max"],
        rq["score_stats"]["avg"], rq["has_relevant"],
    )
    logger.info("  doc_type: %s", rq["doc_type_distribution"])

    cu = evaluation["context_usage"]
    logger.info("Context 사용:")
    logger.info("  referenced=%d  overlap=%.2f  rating=%s",
        cu["referenced_count"],
        cu["context_overlap"]["overlap_ratio"],
        cu["usage_rating"],
    )

    aq = evaluation["analysis_quality"]
    logger.info("분석 품질:")
    logger.info("  bullish=%s(%d)  bearish=%s(%d)  risks=%s(%d)  summary=%s",
        aq["has_bullish"], aq["bullish_count"],
        aq["has_bearish"], aq["bearish_count"],
        aq["has_risks"], aq["risks_count"],
        aq["has_summary"],
    )
    logger.info("  structure_complete=%s", aq["structure_complete"])

    hr = evaluation["hallucination_risk"]
    logger.info("Hallucination 추정:")
    logger.info("  risk_level=%s", hr["risk_level"])
    if hr["reasons"]:
        for r in hr["reasons"]:
            logger.info("  reason: %s", r)
    if hr["assertive_phrases"]:
        logger.info("  assertive: %s", hr["assertive_phrases"])

    # 5. JSON 저장
    logger.info("--- 5. JSON 저장 ---")
    json_path = save_evaluation_json(
        evaluation, filename="samsung_analysis_eval.json",
    )
    logger.info("JSON 저장: %s", json_path)

    # 6. 요약
    logger.info("=== 검증 결과 요약 ===")
    checks = {
        "retrieval_quality": rq["has_relevant"],
        "context_usage": cu["usage_rating"] in ("good", "partial"),
        "analysis_complete": aq["structure_complete"],
        "hallucination_risk": hr["risk_level"] in ("low", "medium"),
        "json_saved": json_path is not None,
    }

    for name, ok in checks.items():
        logger.info("  %-25s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN (일부 항목 주의)")
    logger.info("=== 금융 분석 평가 검증 완료 ===")

    return 0


if __name__ == "__main__":
    sys.exit(main())
