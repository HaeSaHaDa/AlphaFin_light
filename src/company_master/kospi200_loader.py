"""KOSPI200 종목 마스터 로딩 (pykrx 시도 → seed fallback)."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from .company_master_repository import ensure_table, upsert_master_row

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SEED_PATH = PROJECT_ROOT / "data" / "kospi200" / "kospi200_seed.json"


def _load_from_pykrx() -> list[dict] | None:
    try:
        from pykrx import stock
    except ImportError:
        return None

    try:
        # KOSPI200 구성종목 (지수코드 1028)
        tickers = stock.get_index_portfolio_deposit_file("1028")
        if tickers is None or len(tickers) == 0:
            return None
        rows: list[dict] = []
        for ticker in tickers:
            name = stock.get_market_ticker_name(ticker)
            rows.append({
                "ticker": str(ticker).zfill(6),
                "company_name": name,
                "market": "KOSPI",
                "corp_code": None,
                "sector": None,
                "industry": None,
                "aliases": [],
            })
        logger.info("pykrx KOSPI200 로드  count=%d", len(rows))
        return rows
    except Exception:
        logger.exception("pykrx KOSPI200 로드 실패 — seed 사용")
        return None


def _load_from_seed() -> list[dict]:
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info("seed KOSPI200 로드  count=%d", len(data))
    return data


def load_kospi200_companies(*, sync_companies_table: bool = True) -> int:
    """company_master 테이블에 KOSPI200 종목을 적재한다."""
    ensure_table()
    rows = _load_from_pykrx() or _load_from_seed()

    upsert_company = None
    if sync_companies_table:
        from src.common.db.store import upsert_company  # noqa: PLC0415

    count = 0
    for row in rows:
        upsert_master_row(row)
        if upsert_company and row.get("corp_code"):
            upsert_company(
                row["ticker"],
                row["company_name"],
                corp_code=row.get("corp_code"),
                market=row.get("market", "KOSPI"),
            )
        count += 1

    logger.info("company_master 적재 완료  rows=%d", count)
    return count


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    n = load_kospi200_companies()
    print(f"loaded {n} companies")
