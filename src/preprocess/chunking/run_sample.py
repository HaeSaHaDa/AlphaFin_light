"""삼성전자 뉴스/공시 Chunk 생성 및 저장 검증 스크립트."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
sys.path.insert(0, str(DB_MODULE))

from connection import get_connection  # noqa: E402
from init_schema import initialize_database  # noqa: E402
from store import insert_document_chunks  # noqa: E402

from chunker import create_document_chunks  # noqa: E402
from metadata import build_news_metadata, build_disclosure_metadata  # noqa: E402

CHUNKS_NEWS_DIR = PROJECT_ROOT / "data" / "chunks" / "news"
CHUNKS_DISC_DIR = PROJECT_ROOT / "data" / "chunks" / "disclosures"


def fetch_news_articles() -> list[dict]:
    """DB에서 뉴스 기사를 조회한다."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, ticker, title, content, source, url, published_at "
                "FROM news_articles WHERE ticker = %s LIMIT 10",
                ("005930",),
            )
            return cur.fetchall()
    finally:
        conn.close()


def fetch_disclosures() -> list[dict]:
    """DB에서 공시 데이터를 조회한다."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, corp_code, ticker, report_name, receipt_no, "
                "receipt_date, raw_json "
                "FROM dart_disclosures WHERE ticker = %s LIMIT 10",
                ("005930",),
            )
            return cur.fetchall()
    finally:
        conn.close()


def process_news(articles: list[dict], logger: logging.Logger) -> tuple[int, int]:
    """뉴스 기사를 Chunk로 분할하고 JSON + DB에 저장한다."""
    CHUNKS_NEWS_DIR.mkdir(parents=True, exist_ok=True)
    total_chunks = 0
    db_rows: list[dict] = []
    all_json_chunks: list[dict] = []

    for article in articles:
        doc = {
            "title": article.get("title") or "",
            "content": article.get("content") or "",
        }
        chunks = create_document_chunks(doc, "news_article")

        for chunk in chunks:
            meta = build_news_metadata(article, chunk["chunk_index"])
            chunk["metadata"] = meta

            db_rows.append({
                "document_type": "news_article",
                "source_table": "news_articles",
                "source_id": article["id"],
                "ticker": article.get("ticker"),
                "chunk_index": chunk["chunk_index"],
                "chunk_text": chunk["chunk_text"],
                "chunk_length": chunk["chunk_length"],
                "metadata_json": meta,
            })

            all_json_chunks.append({
                "source_id": article["id"],
                "chunk_index": chunk["chunk_index"],
                "chunk_text": chunk["chunk_text"],
                "chunk_length": chunk["chunk_length"],
                "metadata": meta,
            })

        total_chunks += len(chunks)

    json_path = CHUNKS_NEWS_DIR / "samsung_news_chunks.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_json_chunks, f, ensure_ascii=False, indent=2, default=str)
    logger.info("뉴스 Chunk JSON 저장  %s  (%d chunks)", json_path, len(all_json_chunks))

    inserted = insert_document_chunks(db_rows)
    return total_chunks, inserted


def process_disclosures(disclosures: list[dict], logger: logging.Logger) -> tuple[int, int]:
    """공시 데이터를 Chunk로 분할하고 JSON + DB에 저장한다."""
    CHUNKS_DISC_DIR.mkdir(parents=True, exist_ok=True)
    total_chunks = 0
    db_rows: list[dict] = []
    all_json_chunks: list[dict] = []

    for disc in disclosures:
        raw = disc.get("raw_json") or ""
        if isinstance(raw, str):
            text = raw
        else:
            text = json.dumps(raw, ensure_ascii=False)

        report_name = disc.get("report_name") or ""
        if report_name:
            text = f"{report_name}\n\n{text}"

        doc = {"content": text}
        chunks = create_document_chunks(doc, "disclosure")

        for chunk in chunks:
            meta = build_disclosure_metadata(disc, chunk["chunk_index"])
            chunk["metadata"] = meta

            db_rows.append({
                "document_type": "disclosure",
                "source_table": "dart_disclosures",
                "source_id": disc["id"],
                "ticker": disc.get("ticker"),
                "chunk_index": chunk["chunk_index"],
                "chunk_text": chunk["chunk_text"],
                "chunk_length": chunk["chunk_length"],
                "metadata_json": meta,
            })

            all_json_chunks.append({
                "source_id": disc["id"],
                "chunk_index": chunk["chunk_index"],
                "chunk_text": chunk["chunk_text"],
                "chunk_length": chunk["chunk_length"],
                "metadata": meta,
            })

        total_chunks += len(chunks)

    json_path = CHUNKS_DISC_DIR / "samsung_disclosure_chunks.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_json_chunks, f, ensure_ascii=False, indent=2, default=str)
    logger.info("공시 Chunk JSON 저장  %s  (%d chunks)", json_path, len(all_json_chunks))

    inserted = insert_document_chunks(db_rows)
    return total_chunks, inserted


def verify_db(logger: logging.Logger) -> bool:
    """document_chunks 테이블 행 수를 확인한다."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT document_type, COUNT(*) AS cnt "
                "FROM document_chunks GROUP BY document_type"
            )
            rows = cur.fetchall()
            for r in rows:
                logger.info(
                    "검증  document_chunks  type=%-15s  rows=%d",
                    r["document_type"], r["cnt"],
                )
            return len(rows) > 0
    finally:
        conn.close()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Chunking 샘플 검증 시작 ===")

    # 1. 스키마 초기화 (document_chunks 테이블 추가)
    logger.info("--- 1. 스키마 초기화 ---")
    if not initialize_database():
        logger.error("스키마 초기화 실패")
        return 1

    # 2. 뉴스 Chunk 생성
    logger.info("--- 2. 뉴스 Chunk 생성 ---")
    articles = fetch_news_articles()
    logger.info("뉴스 원문 조회: %d건", len(articles))

    if articles:
        news_chunks, news_inserted = process_news(articles, logger)
        logger.info("뉴스 Chunk 생성=%d  DB 저장=%d", news_chunks, news_inserted)
    else:
        logger.warning("뉴스 데이터 없음 (DB에 데이터 필요)")
        news_chunks = news_inserted = 0

    # 3. 공시 Chunk 생성
    logger.info("--- 3. 공시 Chunk 생성 ---")
    disclosures = fetch_disclosures()
    logger.info("공시 원문 조회: %d건", len(disclosures))

    if disclosures:
        disc_chunks, disc_inserted = process_disclosures(disclosures, logger)
        logger.info("공시 Chunk 생성=%d  DB 저장=%d", disc_chunks, disc_inserted)
    else:
        logger.warning("공시 데이터 없음 (DB에 데이터 필요)")
        disc_chunks = disc_inserted = 0

    # 4. DB 검증
    logger.info("--- 4. DB 검증 ---")
    ok = verify_db(logger)

    logger.info(
        "=== 요약  뉴스 chunks=%d  공시 chunks=%d  검증=%s ===",
        news_chunks, disc_chunks, "OK" if ok else "FAIL",
    )

    if not ok:
        logger.error("document_chunks 테이블에 데이터 없음")
        return 1

    logger.info("=== Chunking 샘플 검증 완료 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
