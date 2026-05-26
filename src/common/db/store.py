"""각 테이블에 대한 DB 저장 함수 모음."""
from __future__ import annotations

import json
import logging
from datetime import datetime

import pymysql

from connection import get_connection

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# collection_logs
# ------------------------------------------------------------------

def insert_collection_log(
    collector_name: str,
    target: str,
    status: str = "started",
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
    row_count: int | None = None,
    error_message: str | None = None,
    conn: pymysql.Connection | None = None,
) -> int | None:
    """collection_logs 테이블에 한 건 INSERT 한다.

    Returns:
        생성된 row의 id. 실패 시 None.
    """
    sql = """
        INSERT INTO collection_logs
            (collector_name, target, status, started_at, finished_at,
             row_count, error_message)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    own_conn = conn is None
    if own_conn:
        conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (
                collector_name, target, status,
                started_at or datetime.now(),
                finished_at, row_count, error_message,
            ))
            log_id = cur.lastrowid
        if own_conn:
            conn.commit()
        logger.info(
            "collection_log INSERT  id=%s  collector=%s  status=%s",
            log_id, collector_name, status,
        )
        return log_id
    except Exception:
        if own_conn:
            conn.rollback()
        logger.exception("collection_log INSERT 실패")
        return None
    finally:
        if own_conn:
            conn.close()


def update_collection_log(
    log_id: int,
    status: str,
    finished_at: datetime | None = None,
    row_count: int | None = None,
    error_message: str | None = None,
    conn: pymysql.Connection | None = None,
) -> bool:
    """collection_logs의 기존 로그를 UPDATE 한다."""
    sql = """
        UPDATE collection_logs
        SET status = %s, finished_at = %s,
            row_count = %s, error_message = %s
        WHERE id = %s
    """
    own_conn = conn is None
    if own_conn:
        conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (
                status, finished_at or datetime.now(),
                row_count, error_message, log_id,
            ))
        if own_conn:
            conn.commit()
        return True
    except Exception:
        if own_conn:
            conn.rollback()
        logger.exception("collection_log UPDATE 실패  id=%s", log_id)
        return False
    finally:
        if own_conn:
            conn.close()


# ------------------------------------------------------------------
# companies
# ------------------------------------------------------------------

def upsert_company(
    ticker: str,
    company_name: str,
    corp_code: str | None = None,
    market: str | None = None,
    conn: pymysql.Connection | None = None,
) -> bool:
    """companies 테이블에 INSERT 또는 UPDATE 한다."""
    sql = """
        INSERT INTO companies (ticker, company_name, corp_code, market)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            company_name = VALUES(company_name),
            corp_code    = COALESCE(VALUES(corp_code), corp_code),
            market       = COALESCE(VALUES(market), market)
    """
    own_conn = conn is None
    if own_conn:
        conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (ticker, company_name, corp_code, market))
        if own_conn:
            conn.commit()
        logger.info("company UPSERT  ticker=%s  name=%s", ticker, company_name)
        return True
    except Exception:
        if own_conn:
            conn.rollback()
        logger.exception("company UPSERT 실패  ticker=%s", ticker)
        return False
    finally:
        if own_conn:
            conn.close()


# ------------------------------------------------------------------
# stock_prices
# ------------------------------------------------------------------

def insert_stock_prices(
    rows: list[dict],
    conn: pymysql.Connection | None = None,
) -> int:
    """stock_prices 테이블에 여러 행을 INSERT 한다.

    중복 키(ticker + trade_date)가 있으면 무시한다.

    Args:
        rows: [{"ticker", "trade_date", "open_price", "high_price",
                "low_price", "close_price", "volume", "change_rate"}, ...]

    Returns:
        INSERT 성공 건수.
    """
    sql = """
        INSERT IGNORE INTO stock_prices
            (ticker, trade_date, open_price, high_price,
             low_price, close_price, volume, change_rate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    own_conn = conn is None
    if own_conn:
        conn = get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            for r in rows:
                cur.execute(sql, (
                    r["ticker"], r["trade_date"],
                    r.get("open_price"), r.get("high_price"),
                    r.get("low_price"), r.get("close_price"),
                    r.get("volume"), r.get("change_rate"),
                ))
                inserted += cur.rowcount
        if own_conn:
            conn.commit()
        logger.info("stock_prices INSERT  총 %d / %d건", inserted, len(rows))
        return inserted
    except Exception:
        if own_conn:
            conn.rollback()
        logger.exception("stock_prices INSERT 실패")
        return 0
    finally:
        if own_conn:
            conn.close()


# ------------------------------------------------------------------
# dart_disclosures
# ------------------------------------------------------------------

def insert_dart_disclosures(
    disclosures: list[dict],
    raw_file_path: str | None = None,
    conn: pymysql.Connection | None = None,
) -> int:
    """dart_disclosures 테이블에 여러 건 INSERT 한다.

    중복 receipt_no는 무시한다.

    Args:
        disclosures: OpenDART API list 항목들.
        raw_file_path: 원본 JSON 파일 경로.

    Returns:
        INSERT 성공 건수.
    """
    sql = """
        INSERT IGNORE INTO dart_disclosures
            (corp_code, ticker, report_name, receipt_no,
             receipt_date, disclosure_type, raw_json, raw_file_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    own_conn = conn is None
    if own_conn:
        conn = get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            for d in disclosures:
                rcpt_dt = d.get("rcept_dt", "")
                date_val = (
                    f"{rcpt_dt[:4]}-{rcpt_dt[4:6]}-{rcpt_dt[6:8]}"
                    if len(rcpt_dt) == 8 else None
                )
                cur.execute(sql, (
                    d.get("corp_code"),
                    d.get("stock_code"),
                    d.get("report_nm"),
                    d.get("rcept_no"),
                    date_val,
                    d.get("corp_cls"),
                    json.dumps(d, ensure_ascii=False),
                    raw_file_path,
                ))
                inserted += cur.rowcount
        if own_conn:
            conn.commit()
        logger.info("dart_disclosures INSERT  총 %d / %d건", inserted, len(disclosures))
        return inserted
    except Exception:
        if own_conn:
            conn.rollback()
        logger.exception("dart_disclosures INSERT 실패")
        return 0
    finally:
        if own_conn:
            conn.close()


# ------------------------------------------------------------------
# news_articles
# ------------------------------------------------------------------

def insert_news_articles(
    articles: list[dict],
    keyword: str | None = None,
    ticker: str | None = None,
    raw_file_path: str | None = None,
    conn: pymysql.Connection | None = None,
) -> int:
    """news_articles 테이블에 여러 건 INSERT 한다.

    중복 url은 무시한다.

    Args:
        articles: 뉴스 기사 dict 목록.
        keyword: 검색 키워드.
        ticker: 관련 종목코드.
        raw_file_path: 원본 JSON 파일 경로.

    Returns:
        INSERT 성공 건수.
    """
    sql = """
        INSERT IGNORE INTO news_articles
            (ticker, keyword, title, content, source,
             url, published_at, raw_file_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    own_conn = conn is None
    if own_conn:
        conn = get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            for a in articles:
                published = a.get("date") or None
                cur.execute(sql, (
                    ticker,
                    keyword,
                    a.get("title"),
                    a.get("body") or a.get("content"),
                    a.get("press") or a.get("source"),
                    a.get("url"),
                    published,
                    raw_file_path,
                ))
                inserted += cur.rowcount
        if own_conn:
            conn.commit()
        logger.info("news_articles INSERT  총 %d / %d건", inserted, len(articles))
        return inserted
    except Exception:
        if own_conn:
            conn.rollback()
        logger.exception("news_articles INSERT 실패")
        return 0
    finally:
        if own_conn:
            conn.close()


# ------------------------------------------------------------------
# document_chunks
# ------------------------------------------------------------------

def insert_document_chunks(
    chunks: list[dict],
    conn: pymysql.Connection | None = None,
) -> int:
    """document_chunks 테이블에 여러 건 INSERT 한다.

    중복 (source_table, source_id, chunk_index)는 무시한다.

    Args:
        chunks: [{"document_type", "source_table", "source_id",
                  "ticker", "chunk_index", "chunk_text",
                  "chunk_length", "metadata_json"}, ...]

    Returns:
        INSERT 성공 건수.
    """
    sql = """
        INSERT IGNORE INTO document_chunks
            (document_type, source_table, source_id, ticker,
             chunk_index, chunk_text, chunk_length, metadata_json)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    own_conn = conn is None
    if own_conn:
        conn = get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            for c in chunks:
                meta = c.get("metadata_json")
                if isinstance(meta, dict):
                    meta = json.dumps(meta, ensure_ascii=False)
                cur.execute(sql, (
                    c["document_type"],
                    c["source_table"],
                    c["source_id"],
                    c.get("ticker"),
                    c["chunk_index"],
                    c["chunk_text"],
                    c["chunk_length"],
                    meta,
                ))
                inserted += cur.rowcount
        if own_conn:
            conn.commit()
        logger.info("document_chunks INSERT  총 %d / %d건", inserted, len(chunks))
        return inserted
    except Exception:
        if own_conn:
            conn.rollback()
        logger.exception("document_chunks INSERT 실패")
        return 0
    finally:
        if own_conn:
            conn.close()
