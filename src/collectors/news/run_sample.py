"""삼성전자 뉴스 샘플 수집 실행 스크립트."""
from __future__ import annotations

import logging
import sys

from collector import search_news, save_news_json

SAMPLE_KEYWORD = "삼성전자"
SAMPLE_MAX_PAGES = 1
SAMPLE_FILENAME = "samsung_news_sample.json"


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== 뉴스 샘플 수집 시작 ===")
    logger.info("키워드: %s  max_pages: %d", SAMPLE_KEYWORD, SAMPLE_MAX_PAGES)

    articles = search_news(SAMPLE_KEYWORD, max_pages=SAMPLE_MAX_PAGES)

    if not articles:
        logger.error("수집 실패: 기사 없음")
        return 1

    logger.info("수집된 기사 수: %d", len(articles))

    for i, art in enumerate(articles[:3]):
        logger.info(
            "기사 %d:  제목=%s  날짜=%s  언론사=%s",
            i + 1,
            art.get("title", "")[:40],
            art.get("date", "N/A"),
            art.get("press", "N/A"),
        )

    has_title = sum(1 for a in articles if a.get("title"))
    has_body = sum(1 for a in articles if a.get("body"))
    has_date = sum(1 for a in articles if a.get("date"))
    has_url = sum(1 for a in articles if a.get("url"))
    logger.info(
        "데이터 검증:  제목=%d/%d  본문=%d/%d  날짜=%d/%d  URL=%d/%d",
        has_title, len(articles),
        has_body, len(articles),
        has_date, len(articles),
        has_url, len(articles),
    )

    filepath = save_news_json(articles, filename=SAMPLE_FILENAME)

    if filepath is None:
        logger.error("JSON 저장 실패")
        return 1

    logger.info("저장 경로: %s", filepath)
    logger.info("=== 샘플 수집 완료 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
