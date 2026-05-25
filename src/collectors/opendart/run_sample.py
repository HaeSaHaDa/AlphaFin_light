"""삼성전자(00126380) OpenDART 공시 목록 샘플 수집 스크립트."""
from __future__ import annotations

import logging
import sys

from collector import fetch_disclosures, save_disclosures_json

SAMPLE_CORP_CODE = "00126380"
SAMPLE_CORP_NAME = "삼성전자"
SAMPLE_BEGIN = "20240101"
SAMPLE_END = "20240131"
SAMPLE_FILENAME = "samsung_electronics_disclosures.json"


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== OpenDART 샘플 수집 시작 ===")
    logger.info(
        "기업: %s (%s)  기간: %s ~ %s",
        SAMPLE_CORP_NAME, SAMPLE_CORP_CODE, SAMPLE_BEGIN, SAMPLE_END,
    )

    data = fetch_disclosures(SAMPLE_CORP_CODE, SAMPLE_BEGIN, SAMPLE_END)

    if not data:
        logger.error("수집 실패: 응답 없음")
        return 1

    status = data.get("status", "")
    if status != "000":
        logger.error(
            "API 오류  status=%s  message=%s",
            status, data.get("message", ""),
        )
        return 1

    disclosures = data.get("list", [])
    logger.info("수집된 공시 건수: %d", len(disclosures))

    if disclosures:
        first = disclosures[0]
        logger.info(
            "첫 번째 공시 예시:  제목=%s  날짜=%s",
            first.get("report_nm", "N/A"),
            first.get("rcept_dt", "N/A"),
        )

    filepath = save_disclosures_json(data, filename=SAMPLE_FILENAME)

    if filepath is None:
        logger.error("JSON 저장 실패")
        return 1

    logger.info("저장 경로: %s", filepath)
    logger.info("=== 샘플 수집 완료 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
