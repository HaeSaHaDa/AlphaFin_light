"""삼성전자 관련 샘플 Query 기준 Context 생성 검증 스크립트."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
RETRIEVAL_MODULE = PROJECT_ROOT / "src" / "rag" / "retrieval"
EMBEDDING_MODULE = PROJECT_ROOT / "src" / "rag" / "embedding"
sys.path.insert(0, str(DB_MODULE))
sys.path.insert(0, str(RETRIEVAL_MODULE))
sys.path.insert(0, str(EMBEDDING_MODULE))

from retriever import retrieve_similar_chunks  # noqa: E402
from assembler import (  # noqa: E402
    assemble_context,
    group_chunks_by_type,
    limit_context_length,
    save_context_json,
)
from formatter import (  # noqa: E402
    format_news_context,
    format_disclosure_context,
    build_prompt_context,
)

SAMPLE_QUERIES = [
    "삼성전자 반도체 실적 전망",
    "HBM 시장 성장",
    "AI 메모리 수요 증가",
]


def test_group_chunks(logger: logging.Logger) -> bool:
    """Chunk 그룹화 검증."""
    logger.info("--- group_chunks_by_type 검증 ---")

    mock_chunks = [
        {"chunk_id": 1, "document_type": "news_article", "chunk_text": "뉴스1"},
        {"chunk_id": 2, "document_type": "news_article", "chunk_text": "뉴스2"},
        {"chunk_id": 3, "document_type": "disclosure", "chunk_text": "공시1"},
    ]

    grouped = group_chunks_by_type(mock_chunks)
    news_count = len(grouped.get("news_article", []))
    disc_count = len(grouped.get("disclosure", []))

    logger.info("news_article=%d (기대: 2)  disclosure=%d (기대: 1)", news_count, disc_count)
    ok = news_count == 2 and disc_count == 1
    logger.info("group_chunks_by_type: %s", "OK" if ok else "FAIL")
    return ok


def test_limit_context(logger: logging.Logger) -> bool:
    """Context 길이 제한 검증."""
    logger.info("--- limit_context_length 검증 ---")

    mock_chunks = [
        {"chunk_id": i, "chunk_text": "A" * 200, "score": 1.0 - i * 0.1}
        for i in range(10)
    ]

    limited_by_count = limit_context_length(mock_chunks, max_chunks=3, max_chars=99999)
    logger.info("max_chunks=3: %d건 (기대: 3)", len(limited_by_count))

    limited_by_chars = limit_context_length(mock_chunks, max_chunks=10, max_chars=500)
    logger.info("max_chars=500: %d건 (기대: 2)", len(limited_by_chars))

    ok = len(limited_by_count) == 3 and len(limited_by_chars) == 2
    logger.info("limit_context_length: %s", "OK" if ok else "FAIL")
    return ok


def test_formatter(logger: logging.Logger) -> bool:
    """포맷터 검증."""
    logger.info("--- formatter 검증 ---")

    news_chunks = [
        {
            "chunk_id": 1,
            "score": 0.92,
            "chunk_text": "삼성전자 반도체 실적이 호조를 보이고 있다.",
            "metadata_json": json.dumps({
                "source": "연합뉴스",
                "published_at": "2025-05-20",
                "title": "삼성전자 반도체 호조",
            }),
        },
    ]

    disclosure_chunks = [
        {
            "chunk_id": 2,
            "score": 0.88,
            "chunk_text": "분기 매출 증가 공시 내용입니다.",
            "metadata_json": json.dumps({
                "source": "opendart",
                "published_at": "2025-05-15",
                "report_name": "분기보고서",
            }),
        },
    ]

    news_ctx = format_news_context(news_chunks)
    disc_ctx = format_disclosure_context(disclosure_chunks)

    logger.info("news context 길이: %d", len(news_ctx))
    logger.info("disclosure context 길이: %d", len(disc_ctx))

    has_news = "[NEWS]" in news_ctx and "연합뉴스" in news_ctx
    has_disc = "[DISCLOSURE]" in disc_ctx and "opendart" in disc_ctx
    logger.info("news 포맷: %s", "OK" if has_news else "FAIL")
    logger.info("disclosure 포맷: %s", "OK" if has_disc else "FAIL")

    grouped = {"news_article": news_chunks, "disclosure": disclosure_chunks}
    prompt = build_prompt_context("삼성전자 반도체 전망", grouped)
    has_query = "[QUERY]" in prompt
    logger.info("prompt context 길이: %d  [QUERY] 포함: %s", len(prompt), has_query)

    ok = has_news and has_disc and has_query
    logger.info("formatter: %s", "OK" if ok else "FAIL")
    return ok


def test_retrieval_context(logger: logging.Logger) -> bool:
    """Retrieval + Context 통합 검증."""
    logger.info("--- Retrieval + Context 통합 검증 ---")

    query = SAMPLE_QUERIES[0]
    logger.info("Query: '%s'", query)

    chunks = retrieve_similar_chunks(
        query, top_k=5, filters={"ticker": "005930"},
    )
    logger.info("Retrieval 결과: %d건", len(chunks))

    if not chunks:
        logger.warning("Retrieval 결과 없음 — 건너뜀")
        return False

    ctx = assemble_context(query, chunks, max_chunks=5, max_chars=5000)
    prompt = ctx["prompt_context"]

    logger.info("Context 생성 완료:")
    logger.info("  total_chunks=%d", ctx["total_chunks"])
    logger.info("  limited_chunks=%d", ctx["limited_chunks"])
    logger.info("  prompt_context 길이=%d", len(prompt))

    for doc_type, items in ctx["grouped"].items():
        logger.info("  %s: %d건", doc_type, len(items))

    logger.info("--- Prompt Context 미리보기 ---")
    preview = prompt[:500]
    logger.info("\n%s\n...(총 %d자)", preview, len(prompt))

    json_path = save_context_json(
        ctx, filename="samsung_analysis_context.json",
    )
    logger.info("JSON 저장: %s", json_path)

    ok = len(prompt) > 0 and "[QUERY]" in prompt and json_path is not None
    logger.info("Retrieval + Context 통합: %s", "OK" if ok else "FAIL")
    return ok


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Context Assembly 샘플 검증 시작 ===")

    results = {}

    results["group"] = test_group_chunks(logger)
    results["limit"] = test_limit_context(logger)
    results["formatter"] = test_formatter(logger)
    results["retrieval_context"] = test_retrieval_context(logger)

    logger.info("=== 검증 결과 요약 ===")
    for name, ok in results.items():
        status = "OK" if ok else "SKIP/FAIL"
        logger.info("  %-20s : %s", name, status)

    core_ok = results["group"] and results["limit"] and results["formatter"]
    logger.info(
        "핵심 검증: %s  |  Retrieval+Context: %s",
        "OK" if core_ok else "FAIL",
        "OK" if results["retrieval_context"] else "SKIP",
    )
    logger.info("=== Context Assembly 샘플 검증 완료 ===")

    return 0 if core_ok else 1


if __name__ == "__main__":
    sys.exit(main())
