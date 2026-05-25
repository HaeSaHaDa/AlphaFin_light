"""pykrx 기반 단일 종목 OHLCV 수집기."""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from pykrx import stock

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[3] / "data" / "raw" / "price"


def fetch_ohlcv(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """단일 종목의 OHLCV 일봉 데이터를 수집한다.

    Args:
        ticker: 종목코드 (예: "005930")
        start_date: 시작일 (예: "20240101")
        end_date: 종료일 (예: "20240131")

    Returns:
        OHLCV DataFrame. 실패 시 빈 DataFrame.
    """
    logger.info("fetch_ohlcv  ticker=%s  %s ~ %s", ticker, start_date, end_date)

    try:
        df = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)
    except Exception:
        logger.exception("pykrx 수집 실패  ticker=%s", ticker)
        return pd.DataFrame()

    if df.empty:
        logger.warning("수집 결과 없음  ticker=%s  %s ~ %s", ticker, start_date, end_date)
        return df

    logger.info("수집 완료  ticker=%s  rows=%d", ticker, len(df))
    return df


def save_price_csv(
    df: pd.DataFrame,
    ticker: str,
    start_date: str,
    end_date: str,
    output_dir: Path | str | None = None,
) -> Path | None:
    """OHLCV DataFrame을 CSV로 저장한다.

    Args:
        df: OHLCV DataFrame
        ticker: 종목코드
        start_date: 시작일
        end_date: 종료일
        output_dir: 저장 디렉토리. None이면 data/raw/price/ 사용.

    Returns:
        저장된 파일 경로. 빈 DataFrame이면 None.
    """
    if df.empty:
        logger.warning("저장 생략 (빈 데이터)  ticker=%s", ticker)
        return None

    out = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    filename = f"{ticker}_{start_date}_{end_date}.csv"
    filepath = out / filename

    df.to_csv(filepath, encoding="utf-8-sig")
    logger.info("CSV 저장 완료  %s  rows=%d", filepath, len(df))
    return filepath
