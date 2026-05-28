"""pykrx 주가 수집 → DB 저장."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path

from ._import_helpers import load_collector_module, load_db_store

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYKRX_DIR = PROJECT_ROOT / "src" / "collectors" / "pykrx"


def ingest_prices(ticker: str, days: int = 60) -> int:
    """최근 주가를 stock_prices에 저장한다."""
    pykrx_collector = load_collector_module(PYKRX_DIR, "pykrx")
    store = load_db_store()
    fetch_ohlcv = pykrx_collector.fetch_ohlcv
    insert_stock_prices = store.insert_stock_prices

    end = datetime.now()
    start = end - timedelta(days=days)
    start_s = start.strftime("%Y%m%d")
    end_s = end.strftime("%Y%m%d")

    try:
        df = fetch_ohlcv(ticker, start_s, end_s)
    except Exception:
        logger.exception("주가 수집 실패  ticker=%s", ticker)
        return 0

    if df is None or df.empty:
        return 0

    rows: list[dict] = []
    for idx, row in df.iterrows():
        trade_date = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)
        rows.append({
            "ticker": ticker,
            "trade_date": trade_date,
            "open_price": float(row.get("시가", 0)),
            "high_price": float(row.get("고가", 0)),
            "low_price": float(row.get("저가", 0)),
            "close_price": float(row.get("종가", 0)),
            "volume": int(row.get("거래량", 0)),
            "change_rate": float(row.get("등락률", 0)) if "등락률" in row else None,
        })

    inserted = insert_stock_prices(rows)
    logger.info("주가 DB 저장  ticker=%s  inserted=%d", ticker, inserted)
    return inserted
