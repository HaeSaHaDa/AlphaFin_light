"""삼성전자(005930) 샘플 수집 실행 스크립트."""
from __future__ import annotations

import logging
import sys

from collector import fetch_ohlcv, save_price_csv

SAMPLE_TICKER = "005930"
SAMPLE_START = "20240101"
SAMPLE_END = "20240131"


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== pykrx 샘플 수집 시작 ===")
    logger.info("종목: %s  기간: %s ~ %s", SAMPLE_TICKER, SAMPLE_START, SAMPLE_END)

    df = fetch_ohlcv(SAMPLE_TICKER, SAMPLE_START, SAMPLE_END)

    if df.empty:
        logger.error("수집 실패: 데이터 없음")
        return 1

    logger.info("수집 결과 미리보기:\n%s", df.head())
    logger.info("컬럼: %s", list(df.columns))
    logger.info("행 수: %d", len(df))

    filepath = save_price_csv(df, SAMPLE_TICKER, SAMPLE_START, SAMPLE_END)

    if filepath is None:
        logger.error("CSV 저장 실패")
        return 1

    logger.info("저장 경로: %s", filepath)
    logger.info("=== 샘플 수집 완료 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
