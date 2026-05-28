"""DB 문서 → document_chunks."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from src.cost_guard.limits import MAX_CHUNK_ROWS, MAX_NEWS_DB_ROWS

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHUNK_DIR = PROJECT_ROOT / "src" / "preprocess" / "chunking"
DB_DIR = PROJECT_ROOT / "src" / "common" / "db"


def _fetch_news(ticker: str) -> list[dict]:
    from src.common.db.connection import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, ticker, title, content, source, url, published_at "
                "FROM news_articles WHERE ticker = %s ORDER BY id DESC LIMIT %s",
                (ticker, MAX_NEWS_DB_ROWS),
            )
            return cur.fetchall()
    finally:
        conn.close()


def _fetch_disclosures(ticker: str) -> list[dict]:
    from src.common.db.connection import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, corp_code, ticker, report_name, receipt_no, "
                "receipt_date, raw_json FROM dart_disclosures "
                "WHERE ticker = %s ORDER BY id DESC LIMIT 20",
                (ticker,),
            )
            return cur.fetchall()
    finally:
        conn.close()


def run_chunking(ticker: str) -> int:
    """ticker 기준 뉴스·공시를 chunking하여 DB에 저장한다."""
    if str(CHUNK_DIR) not in sys.path:
        sys.path.insert(0, str(CHUNK_DIR))
    if str(DB_DIR) not in sys.path:
        sys.path.insert(0, str(DB_DIR))

    from chunker import create_document_chunks  # type: ignore[import]
    from metadata import build_disclosure_metadata, build_news_metadata  # type: ignore[import]
    from store import insert_document_chunks  # type: ignore[import]

    db_rows: list[dict] = []

    for article in _fetch_news(ticker):
        doc = {
            "title": article.get("title") or "",
            "content": article.get("content") or "",
        }
        chunks = create_document_chunks(doc, "news_article")
        for chunk in chunks:
            meta = build_news_metadata(article, chunk["chunk_index"])
            db_rows.append({
                "document_type": "news_article",
                "source_table": "news_articles",
                "source_id": article["id"],
                "ticker": ticker,
                "chunk_index": chunk["chunk_index"],
                "chunk_text": chunk["chunk_text"],
                "chunk_length": chunk["chunk_length"],
                "metadata_json": meta,
            })

    for disc in _fetch_disclosures(ticker):
        raw = disc.get("raw_json") or "{}"
        if isinstance(raw, str):
            import json
            try:
                raw_obj = json.loads(raw)
            except json.JSONDecodeError:
                raw_obj = {}
        else:
            raw_obj = raw
        text = f"{disc.get('report_name', '')} {raw_obj.get('report_nm', '')}"
        doc = {"title": disc.get("report_name") or "", "content": text}
        chunks = create_document_chunks(doc, "disclosure")
        for chunk in chunks:
            meta = build_disclosure_metadata(disc, chunk["chunk_index"])
            db_rows.append({
                "document_type": "disclosure",
                "source_table": "dart_disclosures",
                "source_id": disc["id"],
                "ticker": ticker,
                "chunk_index": chunk["chunk_index"],
                "chunk_text": chunk["chunk_text"],
                "chunk_length": chunk["chunk_length"],
                "metadata_json": meta,
            })

    if not db_rows:
        return 0

    if len(db_rows) > MAX_CHUNK_ROWS:
        db_rows = db_rows[:MAX_CHUNK_ROWS]
        logger.info("chunk 상한 적용  max=%d", MAX_CHUNK_ROWS)

    inserted = insert_document_chunks(db_rows)
    logger.info("chunking 완료  ticker=%s  rows=%d inserted=%d", ticker, len(db_rows), inserted)
    return inserted
