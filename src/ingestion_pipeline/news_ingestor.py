"""뉴스 수집 → DB 저장."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
NEWS_DIR = PROJECT_ROOT / "src" / "collectors" / "news"
DB_DIR = PROJECT_ROOT / "src" / "common" / "db"


def ingest_news(company_name: str, ticker: str, max_pages: int = 1) -> int:
    """네이버 뉴스 검색 후 news_articles에 저장한다."""
    if str(NEWS_DIR) not in sys.path:
        sys.path.insert(0, str(NEWS_DIR))
    if str(DB_DIR) not in sys.path:
        sys.path.insert(0, str(DB_DIR))

    from collector import search_news, save_news_json  # type: ignore[import]
    from store import insert_news_articles  # type: ignore[import]

    articles = search_news(company_name, max_pages=max_pages)
    if not articles:
        logger.warning("뉴스 수집 0건  company=%s", company_name)
        return 0

    raw_dir = PROJECT_ROOT / "data" / "raw" / "news"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = save_news_json(
        articles,
        output_dir=raw_dir,
        filename=f"{ticker}_news.json",
    )

    inserted = insert_news_articles(
        articles,
        keyword=company_name,
        ticker=ticker,
        raw_file_path=str(raw_path) if raw_path else None,
    )
    logger.info("뉴스 DB 저장  ticker=%s  inserted=%d", ticker, inserted)
    return inserted
