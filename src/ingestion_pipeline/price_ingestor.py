"""pykrx 주가 수집 → DB 저장."""
from __future__ import annotations

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYKRX_DIR = PROJECT_ROOT / "src" / "collectors" / "pykrx"
DB_DIR = PROJECT_ROOT / "src" / "common" / "db"


def ingest_prices(ticker: str, days: int = 60) -> int:
    """최근 주가를 stock_prices에 저장한다."""
    if str(PYKRX_DIR) not in sys.path:
        sys.path.insert(0, str(PYKRX_DIR))
    if str(DB_DIR) not in sys.path:
        sys.path.insert(0, str(DB_DIR))

    from collector import fetch_ohlcv  # type: ignore[import]
    from store import insert_stock_prices  # type: ignore[import]

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
