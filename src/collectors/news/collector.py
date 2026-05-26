"""네이버 뉴스 검색 기반 뉴스 수집기."""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[3] / "data" / "raw" / "news"
REQUEST_TIMEOUT_SEC = 15
REQUEST_DELAY_SEC = 1.0

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
}

NAVER_SEARCH_URL = "https://search.naver.com/search.naver"


def search_news(keyword: str, max_pages: int = 1) -> list[dict]:
    """네이버 뉴스 검색 후 기사 목록을 수집한다.

    Args:
        keyword: 검색 키워드 (예: "삼성전자")
        max_pages: 수집할 페이지 수 (1페이지 = 10건)

    Returns:
        수집된 기사 dict 목록.
    """
    logger.info("search_news  keyword=%s  max_pages=%d", keyword, max_pages)
    articles: list[dict] = []

    for page in range(max_pages):
        start = page * 10 + 1
        params = {
            "where": "news",
            "query": keyword,
            "start": start,
            "sort": "1",
        }

        try:
            resp = requests.get(
                NAVER_SEARCH_URL,
                params=params,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT_SEC,
            )
            resp.raise_for_status()
        except requests.RequestException:
            logger.exception("뉴스 검색 실패  keyword=%s  page=%d", keyword, page + 1)
            break

        links = extract_news_links(resp.text)
        logger.info("페이지 %d  네이버 뉴스 링크 %d개 추출", page + 1, len(links))

        for link_info in links:
            time.sleep(REQUEST_DELAY_SEC)
            article = fetch_article(link_info["url"])
            if article:
                article["search_title"] = link_info.get("title", "")
                article["press_from_search"] = link_info.get("press", "")
                articles.append(article)

        if page < max_pages - 1:
            time.sleep(REQUEST_DELAY_SEC)

    logger.info("총 수집 기사 수: %d", len(articles))
    return articles


def extract_news_links(html: str) -> list[dict]:
    """검색 결과 HTML에서 네이버 뉴스 기사 링크를 추출한다.

    Returns:
        [{"url": ..., "title": ..., "press": ...}, ...]
    """
    soup = BeautifulSoup(html, "html.parser")
    results: list[dict] = []
    seen_urls: set[str] = set()

    naver_anchors = [
        a for a in soup.find_all("a")
        if "n.news.naver.com/mnews/article" in a.get("href", "")
    ]

    for anchor in naver_anchors:
        url = anchor.get("href", "")
        if url in seen_urls:
            continue
        seen_urls.add(url)

        container = anchor
        for _ in range(6):
            if container.parent:
                container = container.parent

        title = ""
        press = ""

        for a_tag in container.find_all("a"):
            href = a_tag.get("href", "")
            text = a_tag.get_text(strip=True)
            if not title and len(text) > 10 and "n.news.naver.com" not in href and "media.naver.com" not in href and "keep.naver" not in href:
                title = text
            if not press and "media.naver.com/press" in href and text:
                press = text

        results.append({"url": url, "title": title, "press": press})

    return results


def fetch_article(url: str) -> dict | None:
    """네이버 뉴스 기사 페이지에서 본문을 수집한다.

    Args:
        url: 네이버 뉴스 기사 URL

    Returns:
        기사 dict 또는 None.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_SEC)
        resp.raise_for_status()
    except requests.RequestException:
        logger.exception("기사 수집 실패  url=%s", url)
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.select_one("#title_area span, h2#title_area")
    title = title_tag.get_text(strip=True) if title_tag else ""

    body_tag = soup.select_one("article#dic_area, div#newsct_article")
    body = body_tag.get_text(separator="\n", strip=True) if body_tag else ""

    date_tag = soup.select_one(
        "span.media_end_head_info_datestamp_time, "
        "span[data-date-time]"
    )
    date = ""
    if date_tag:
        date = date_tag.get("data-date-time", "") or date_tag.get_text(strip=True)

    press_tag = soup.select_one(
        "a.media_end_head_top_logo img, "
        "img.media_end_head_top_logo_img_light"
    )
    press = press_tag.get("alt", "") if press_tag else ""

    if not title and not body:
        logger.warning("기사 파싱 실패 (제목/본문 없음)  url=%s", url)
        return None

    logger.info("기사 수집 완료  title=%s", title[:40] if title else "(제목 없음)")
    return {
        "title": title,
        "body": body,
        "date": date,
        "press": press,
        "url": url,
    }


def save_news_json(
    data: list[dict],
    output_dir: Path | str | None = None,
    filename: str = "news.json",
) -> Path | None:
    """수집된 뉴스 목록을 JSON으로 저장한다.

    Args:
        data: 기사 dict 목록.
        output_dir: 저장 디렉토리. None이면 data/raw/news/ 사용.
        filename: 저장 파일명.

    Returns:
        저장된 파일 경로. 빈 데이터면 None.
    """
    if not data:
        logger.warning("저장 생략 (뉴스 데이터 없음)")
        return None

    out = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    filepath = out / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info("JSON 저장 완료  %s  기사 %d건", filepath, len(data))
    return filepath
