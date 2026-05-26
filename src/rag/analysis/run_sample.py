"""삼성전자 관련 샘플 Query 금융 분석 검증 스크립트."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
RETRIEVAL_MODULE = PROJECT_ROOT / "src" / "rag" / "retrieval"
CONTEXT_MODULE = PROJECT_ROOT / "src" / "rag" / "context"
EMBEDDING_MODULE = PROJECT_ROOT / "src" / "rag" / "embedding"
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(CONTEXT_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))

from analyzer import (  # noqa: E402
    analyze_financial_query,
    save_analysis_json,
)
from prompts import build_analysis_prompt  # noqa: E402

SAMPLE_QUERY = "삼성전자 반도체 전망 분석"


def test_prompt_build(logger: logging.Logger) -> bool:
    """Prompt 생성 검증."""
    logger.info("--- Prompt 생성 검증 ---")

    mock_context = """[QUERY]
삼성전자 반도체 전망 분석

[NEWS]
--- news #1 ---
- score: 0.92
- source: 연합뉴스
- date: 2025-05-20
- content:
삼성전자 반도체 사업이 호조를 보이고 있다.
"""

    messages = build_analysis_prompt(SAMPLE_QUERY, mock_context)

    has_system = any(m["role"] == "system" for m in messages)
    has_user = any(m["role"] == "user" for m in messages)
    has_query = any(SAMPLE_QUERY in m["content"] for m in messages)

    logger.info("system 메시지: %s", "OK" if has_system else "FAIL")
    logger.info("user 메시지: %s", "OK" if has_user else "FAIL")
    logger.info("query 포함: %s", "OK" if has_query else "FAIL")

    ok = has_system and has_user and has_query
    logger.info("Prompt 생성: %s", "OK" if ok else "FAIL")
    return ok


def test_full_analysis(logger: logging.Logger) -> bool:
    """전체 분석 Flow 검증 (Retrieval → Context → Prompt → Chat API)."""
    logger.info("--- 전체 분석 Flow 검증 ---")
    logger.info("Query: '%s'", SAMPLE_QUERY)

    result = analyze_financial_query(
        SAMPLE_QUERY,
        top_k=3,
        filters={"ticker": "005930"},
    )

    if result.get("error"):
        logger.error("분석 실패: %s", result["error"])
        return False

    checks = {
        "query": bool(result.get("query")),
        "bullish_factors": isinstance(result.get("bullish_factors"), list),
        "bearish_factors": isinstance(result.get("bearish_factors"), list),
        "risks": isinstance(result.get("risks"), list),
        "summary": bool(result.get("summary")),
        "referenced_chunks": isinstance(result.get("referenced_chunks"), list)
        and len(result["referenced_chunks"]) > 0,
    }

    for field, ok in checks.items():
        logger.info("  %-20s : %s", field, "OK" if ok else "FAIL")

    logger.info("--- 분석 결과 상세 ---")
    logger.info("bullish_factors (%d):", len(result.get("bullish_factors", [])))
    for f in result.get("bullish_factors", []):
        logger.info("  + %s", f)

    logger.info("bearish_factors (%d):", len(result.get("bearish_factors", [])))
    for f in result.get("bearish_factors", []):
        logger.info("  - %s", f)

    logger.info("risks (%d):", len(result.get("risks", [])))
    for r in result.get("risks", []):
        logger.info("  ! %s", r)

    logger.info("summary: %s", result.get("summary", "")[:200])

    logger.info("referenced_chunks (%d):", len(result.get("referenced_chunks", [])))
    for ref in result.get("referenced_chunks", []):
        logger.info(
            "  chunk_id=%s  type=%s  score=%s",
            ref.get("chunk_id"), ref.get("document_type"), ref.get("score"),
        )

    json_path = save_analysis_json(
        result, filename="samsung_financial_analysis.json",
    )
    logger.info("JSON 저장: %s", json_path)

    all_ok = all(checks.values()) and json_path is not None
    logger.info("전체 분석 Flow: %s", "OK" if all_ok else "FAIL")
    return all_ok


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== 금융 분석 샘플 검증 시작 ===")

    results = {}
    results["prompt"] = test_prompt_build(logger)
    results["full_analysis"] = test_full_analysis(logger)

    logger.info("=== 검증 결과 요약 ===")
    for name, ok in results.items():
        status = "OK" if ok else "SKIP/FAIL"
        logger.info("  %-20s : %s", name, status)

    all_ok = all(results.values())
    logger.info("최종: %s", "OK" if all_ok else "FAIL")
    logger.info("=== 금융 분석 샘플 검증 완료 ===")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
