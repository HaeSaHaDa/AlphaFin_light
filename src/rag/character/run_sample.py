"""Persona별 금융 분석 샘플 검증 스크립트."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
RETRIEVAL_MODULE = PROJECT_ROOT / "src" / "rag" / "retrieval"
CONTEXT_MODULE = PROJECT_ROOT / "src" / "rag" / "context"
EMBEDDING_MODULE = PROJECT_ROOT / "src" / "rag" / "embedding"
EVALUATION_MODULE = PROJECT_ROOT / "src" / "rag" / "evaluation"
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(CONTEXT_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))
sys.path.insert(0, str(EVALUATION_MODULE))

from personas import list_available_personas  # noqa: E402
from analyzer import (  # noqa: E402
    run_all_personas,
    compare_persona_results,
    save_character_json,
)

SAMPLE_QUERY = "삼성전자 반도체 전망 분석"


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Character Layer 검증 시작 ===")

    # 1. Persona 목록 확인
    personas = list_available_personas()
    logger.info("--- 1. Persona 목록 ---")
    for p in personas:
        logger.info("  %s", p)

    # 2. 전체 Persona 분석 실행
    logger.info("--- 2. 전체 Persona 분석 ---")
    results = run_all_personas(
        SAMPLE_QUERY, top_k=5, filters={"ticker": "005930"},
    )

    # 3. 개별 결과 출력 및 저장
    logger.info("--- 3. Persona별 결과 ---")
    saved_files: list[Path] = []

    for r in results:
        persona = r.get("persona", "unknown")
        if r.get("error"):
            logger.error("  %s: 실패 — %s", persona, r["error"])
            continue

        logger.info("  [%s] %s", persona, r.get("persona_name", ""))
        logger.info("    bullish: %d  bearish: %d  risks: %d",
            len(r.get("bullish_factors", [])),
            len(r.get("bearish_factors", [])),
            len(r.get("risks", [])),
        )
        logger.info("    summary: %s", r.get("summary", "")[:80])

        eval_data = r.get("evaluation", {})
        hr = eval_data.get("hallucination_risk", {})
        logger.info("    hallucination: %s", hr.get("risk_level", "?"))

        path = save_character_json(r)
        if path:
            saved_files.append(path)
            logger.info("    saved: %s", path.name)

    # 4. Persona 비교
    logger.info("--- 4. Persona 비교 ---")
    comparison = compare_persona_results(results)

    for p_info in comparison["personas"]:
        if p_info.get("error"):
            logger.info("  %-25s : ERROR", p_info["persona"])
            continue
        logger.info(
            "  %-25s : bull=%d  bear=%d  risk=%d  halluc=%s",
            p_info["persona"],
            p_info["bullish_count"],
            p_info["bearish_count"],
            p_info["risks_count"],
            p_info["hallucination_risk"],
        )
        logger.info("    -> %s", p_info["summary_preview"])

    # 5. 비교 결과 저장
    comparison_path = save_character_json(
        comparison, filename="samsung_comparison.json",
    )
    logger.info("비교 JSON: %s", comparison_path)

    # 6. 최종 검증
    logger.info("=== 검증 결과 요약 ===")
    success_count = sum(1 for r in results if not r.get("error"))
    checks = {
        "persona_load": len(personas) == 4,
        "analysis_success": success_count == len(personas),
        "json_saved": len(saved_files) == len(personas),
        "comparison_saved": comparison_path is not None,
    }

    for name, ok in checks.items():
        logger.info("  %-25s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Character Layer 검증 완료 ===")

    return 0


if __name__ == "__main__":
    sys.exit(main())
