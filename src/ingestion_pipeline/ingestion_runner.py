"""Ingestion Pipeline 오케스트레이션."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.company_resolver.company_resolver import ResolvedCompany, resolve_company

from .chunk_pipeline import run_chunking
from .dart_ingestor import ingest_dart
from .embedding_pipeline import run_embedding
from .news_ingestor import ingest_news
from .price_ingestor import ingest_prices
from .vector_index_manager import (
    append_log,
    is_ticker_ready,
    save_cache,
    _db_embedding_count,
)

logger = logging.getLogger(__name__)

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


def run_ingestion(
    company_text: str,
    *,
    force: bool = False,
    skip_news: bool = False,
) -> dict:
    """회사명/질문 → 수집 → chunk → embedding."""
    resolved = resolve_company(company_text)
    if not resolved:
        return {
            "status": "failed",
            "error": f"회사를 식별할 수 없습니다: {company_text}",
        }

    return run_ingestion_for_company(resolved, force=force, skip_news=skip_news)


def run_ingestion_for_company(
    company: ResolvedCompany,
    *,
    force: bool = False,
    skip_news: bool = False,
) -> dict:
    ticker = company.ticker
    name = company.company_name

    if not force and is_ticker_ready(ticker):
        emb = _db_embedding_count(ticker)
        logger.info("cache 재사용  ticker=%s  embeddings=%d", ticker, emb)
        return {
            "ticker": ticker,
            "company_name": name,
            "corp_code": company.corp_code,
            "status": "cached",
            "documents": 0,
            "chunks": 0,
            "embeddings": emb,
        }

    _upsert_company_record(
        ticker, name, company.corp_code, company.market,
    )

    news_n = 0
    if not skip_news:
        try:
            news_n = ingest_news(name, ticker, max_pages=1)
        except Exception:
            logger.exception("뉴스 ingestion 실패")

    dart_n = 0
    try:
        dart_n = ingest_dart(company.corp_code, ticker)
    except Exception:
        logger.exception("공시 ingestion 실패")

    price_n = 0
    try:
        price_n = ingest_prices(ticker)
    except Exception:
        logger.exception("주가 ingestion 실패")

    documents = news_n + dart_n + price_n
    chunks = run_chunking(ticker)
    embeddings = run_embedding(ticker)
    emb_total = _db_embedding_count(ticker)

    status = "completed" if emb_total >= 1 else "partial"
    result = {
        "ticker": ticker,
        "company_name": name,
        "corp_code": company.corp_code,
        "status": status,
        "documents": documents,
        "chunks": chunks,
        "embeddings": emb_total,
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
    return result


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    parser = argparse.ArgumentParser(description="Company ingestion runner")
    parser.add_argument("company", help="회사명 또는 질문")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    out = run_ingestion(args.company, force=args.force)
    print(out)
    return 0 if out.get("status") in ("completed", "cached", "partial") else 1


if __name__ == "__main__":
    raise SystemExit(main())
