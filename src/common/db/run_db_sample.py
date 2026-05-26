"""기존 Raw 데이터를 읽어 MariaDB에 저장하는 통합 검증 스크립트."""
from __future__ import annotations

import csv
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from connection import get_connection
from init_schema import initialize_database
from store import (
    insert_collection_log,
    insert_dart_disclosures,
    insert_news_articles,
    insert_stock_prices,
    update_collection_log,
    upsert_company,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PRICE_CSV = PROJECT_ROOT / "data" / "raw" / "price" / "005930_20240101_20240131.csv"
DART_JSON = PROJECT_ROOT / "data" / "raw" / "dart" / "samsung_electronics_disclosures.json"
NEWS_JSON = PROJECT_ROOT / "data" / "raw" / "news" / "samsung_news_sample.json"


def store_price_data(logger: logging.Logger) -> int:
    """pykrx CSV 데이터를 stock_prices 테이블에 저장한다."""
    if not PRICE_CSV.exists():
        logger.warning("주가 CSV 없음: %s", PRICE_CSV)
        return 0

    log_id = insert_collection_log("pykrx", "005930", "started")
    started = datetime.now()

    rows: list[dict] = []
    with open(PRICE_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "ticker": "005930",
                "trade_date": row["날짜"],
                "open_price": row["시가"],
                "high_price": row["고가"],
                "low_price": row["저가"],
                "close_price": row["종가"],
                "volume": row["거래량"],
                "change_rate": row["등락률"],
            })

    inserted = insert_stock_prices(rows)

    if log_id:
        status = "success" if inserted > 0 else "failed"
        update_collection_log(log_id, status, datetime.now(), inserted)

    logger.info("주가 저장 완료  %d / %d건", inserted, len(rows))
    return inserted


def store_dart_data(logger: logging.Logger) -> int:
    """OpenDART JSON 데이터를 dart_disclosures 테이블에 저장한다."""
    if not DART_JSON.exists():
        logger.warning("공시 JSON 없음: %s", DART_JSON)
        return 0

    log_id = insert_collection_log("opendart", "00126380", "started")

    with open(DART_JSON, encoding="utf-8") as f:
        data = json.load(f)

    disclosures = data.get("list", [])
    inserted = insert_dart_disclosures(
        disclosures, raw_file_path=str(DART_JSON),
    )

    if log_id:
        status = "success" if inserted > 0 else "failed"
        update_collection_log(log_id, status, datetime.now(), inserted)

    logger.info("공시 저장 완료  %d / %d건", inserted, len(disclosures))
    return inserted


def store_news_data(logger: logging.Logger) -> int:
    """뉴스 JSON 데이터를 news_articles 테이블에 저장한다."""
    if not NEWS_JSON.exists():
        logger.warning("뉴스 JSON 없음: %s", NEWS_JSON)
        return 0

    log_id = insert_collection_log("news", "삼성전자", "started")

    with open(NEWS_JSON, encoding="utf-8") as f:
        articles = json.load(f)

    inserted = insert_news_articles(
        articles,
        keyword="삼성전자",
        ticker="005930",
        raw_file_path=str(NEWS_JSON),
    )

    if log_id:
        status = "success" if inserted > 0 else "failed"
        update_collection_log(log_id, status, datetime.now(), inserted)

    logger.info("뉴스 저장 완료  %d / %d건", inserted, len(articles))
    return inserted


def verify_counts(logger: logging.Logger) -> bool:
    """각 테이블의 행 수를 확인한다."""
    conn = get_connection()
    tables = ["companies", "stock_prices", "dart_disclosures",
              "news_articles", "collection_logs"]
    all_ok = True
    try:
        with conn.cursor() as cur:
            for table in tables:
                cur.execute(f"SELECT COUNT(*) AS cnt FROM {table}")
                result = cur.fetchone()
                cnt = result["cnt"] if result else 0
                logger.info("검증  %-20s  rows=%d", table, cnt)
                if table != "companies" and cnt == 0:
                    all_ok = False
    finally:
        conn.close()
    return all_ok


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== DB 통합 검증 시작 ===")

    # 1. 스키마 초기화
    logger.info("--- 1. 스키마 초기화 ---")
    if not initialize_database():
        logger.error("스키마 초기화 실패")
        return 1

    # 2. 기업 정보 등록
    logger.info("--- 2. 기업 정보 등록 ---")
    upsert_company("005930", "삼성전자", corp_code="00126380", market="KOSPI")

    # 3. 주가 데이터 저장
    logger.info("--- 3. 주가 데이터 저장 ---")
    price_cnt = store_price_data(logger)

    # 4. 공시 데이터 저장
    logger.info("--- 4. 공시 데이터 저장 ---")
    dart_cnt = store_dart_data(logger)

    # 5. 뉴스 데이터 저장
    logger.info("--- 5. 뉴스 데이터 저장 ---")
    news_cnt = store_news_data(logger)

    # 6. 검증
    logger.info("--- 6. 테이블 행 수 검증 ---")
    ok = verify_counts(logger)

    logger.info(
        "=== 저장 요약  주가=%d  공시=%d  뉴스=%d  검증=%s ===",
        price_cnt, dart_cnt, news_cnt, "OK" if ok else "FAIL",
    )

    if not ok:
        logger.error("일부 테이블에 데이터 없음")
        return 1

    logger.info("=== DB 통합 검증 완료 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
