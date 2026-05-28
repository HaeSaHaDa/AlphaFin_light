"""Ingestion Pipeline 오케스트레이션."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.company_resolver.company_resolver import ResolvedCompany, resolve_company
from src.cost_guard.limits import MAX_NEWS_PAGES
from src.cost_guard.presentation_mode import is_presentation_mode

from .chunk_pipeline import run_chunking
from .dart_ingestor import ingest_dart
from .embedding_pipeline import run_embedding
from .news_ingestor import ingest_news
from .price_ingestor import ingest_prices
from .ticker_stats import fetch_recent_disclosures, get_ticker_stats
from .vector_index_manager import (
    append_log,
    is_ticker_ready,
    save_cache,
    _db_embedding_count,
)

logger = logging.getLogger(__name__)

MIN_DISCLOSURES = 3
_DB_DIR = Path(__file__).resolve().parents[2] / "src" / "common" / "db"


def _upsert_company_record(
    ticker: str,
    name: str,
    corp_code: str,
    market: str,
) -> None:
    db_path = str(_DB_DIR)
    if db_path not in sys.path:
        sys.path.insert(0, db_path)
    from store import upsert_company  # type: ignore[import]

    upsert_company(ticker, name, corp_code=corp_code, market=market)


def _enrich_result(company: ResolvedCompany, result: dict) -> dict:
    stats = get_ticker_stats(company.ticker)
    result["stats"] = stats
    result["recent_disclosures"] = fetch_recent_disclosures(company.ticker, 5)
    result["market"] = company.market
    return result


def run_ingestion(
    company_text: str,
    *,
    force: bool = False,
    skip_news: bool = False,
    dry_run: bool = False,
) -> dict:
    """회사명/질문 → 수집 → chunk → embedding."""
    resolved = resolve_company(company_text)
    if not resolved:
        return {
            "status": "failed",
            "error": f"회사를 식별할 수 없습니다: {company_text}",
        }

    return run_ingestion_for_company(
        resolved, force=force, skip_news=skip_news, dry_run=dry_run,
    )


def run_ingestion_for_company(
    company: ResolvedCompany,
    *,
    force: bool = False,
    skip_news: bool = False,
    dry_run: bool = False,
) -> dict:
    ticker = company.ticker
    name = company.company_name
    stats = get_ticker_stats(ticker)
    cache_ready = is_ticker_ready(ticker)

    if dry_run:
        return _enrich_result(company, {
            "ticker": ticker,
            "company_name": name,
            "corp_code": company.corp_code,
            "status": "dry_run",
            "cache_ready": cache_ready,
            "embeddings": stats["embedding_count"],
            "presentation_mode": is_presentation_mode(),
            "would_skip_ingestion": cache_ready and not force,
        })

    if not force and cache_ready:
        logger.info(
            "cache 재사용  ticker=%s  embeddings=%d",
            ticker, stats["embedding_count"],
        )
        return _enrich_result(company, {
            "ticker": ticker,
            "company_name": name,
            "corp_code": company.corp_code,
            "status": "cached",
            "documents": 0,
            "chunks": 0,
            "embeddings": stats["embedding_count"],
            "embeddings_created": 0,
            "embeddings_skipped": stats["embedding_count"],
            "skipped_collectors": ["news", "dart", "price", "chunk", "embedding"],
        })

    _upsert_company_record(
        ticker, name, company.corp_code, company.market,
    )

    skipped_collectors: list[str] = []
    news_n = 0
    if not skip_news and (force or stats["news_count"] == 0):
        try:
            news_n = ingest_news(name, ticker, max_pages=MAX_NEWS_PAGES)
        except Exception:
            logger.exception("뉴스 ingestion 실패")
    else:
        skipped_collectors.append("news")
        logger.info("뉴스 스킵  existing=%d", stats["news_count"])

    dart_n = 0
    if force or stats["disclosure_count"] < MIN_DISCLOSURES:
        try:
            dart_n = ingest_dart(company.corp_code, ticker)
        except Exception:
            logger.exception("공시 ingestion 실패")
    else:
        skipped_collectors.append("dart")
        logger.info("공시 스킵  existing=%d", stats["disclosure_count"])

    price_n = 0
    if force or stats["price_count"] == 0:
        try:
            price_n = ingest_prices(ticker)
        except Exception:
            logger.exception("주가 ingestion 실패")
    else:
        skipped_collectors.append("price")
        logger.info("주가 스킵  existing=%d", stats["price_count"])

    documents = news_n + dart_n + price_n

    chunks = 0
    if documents > 0 or stats["pending_embedding_count"] > 0:
        chunks = run_chunking(ticker)
    else:
        skipped_collectors.append("chunk")
        logger.info("chunking 스킵  신규 문서 없음")

    emb_result = run_embedding(ticker, dry_run=False)
    embeddings_created = int(emb_result.get("inserted", 0))
    embeddings_skipped = int(emb_result.get("skipped", 0))
    emb_total = _db_embedding_count(ticker)

    if embeddings_created == 0 and emb_total > 0:
        skipped_collectors.append("embedding")

    status = "completed" if emb_total >= 1 else "partial"
    result = {
        "ticker": ticker,
        "company_name": name,
        "corp_code": company.corp_code,
        "status": status,
        "documents": documents,
        "chunks": chunks,
        "embeddings": emb_total,
        "embeddings_created": embeddings_created,
        "embeddings_skipped": embeddings_skipped,
        "skipped_collectors": skipped_collectors,
        "presentation_mode": is_presentation_mode(),
    }

    save_cache(
        ticker,
        name,
        status=status,
        documents=documents,
        chunks=chunks,
        embeddings=emb_total,
    )
    append_log(ticker, result)
    logger.info("ingestion 완료  %s", result)
    return _enrich_result(company, result)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    parser = argparse.ArgumentParser(description="Company ingestion runner")
    parser.add_argument("company", help="회사명 또는 질문")
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제 embedding/API 호출 없이 파이프라인 상태만 확인",
    )
    args = parser.parse_args()

    out = run_ingestion(args.company, force=args.force, dry_run=args.dry_run)
    print(out)
    ok_statuses = ("completed", "cached", "partial", "dry_run")
    return 0 if out.get("status") in ok_statuses else 1


if __name__ == "__main__":
    raise SystemExit(main())
