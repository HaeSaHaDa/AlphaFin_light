"""Chunk Metadata 생성 모듈."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def build_news_metadata(article: dict, chunk_index: int) -> dict:
    """뉴스 기사에 대한 Chunk Metadata를 생성한다.

    Args:
        article: DB에서 조회한 뉴스 기사 dict.
        chunk_index: 현재 Chunk 순번.

    Returns:
        Metadata dict.
    """
    return {
        "ticker": article.get("ticker") or "",
        "source": article.get("source") or "",
        "published_at": str(article.get("published_at") or ""),
        "chunk_index": chunk_index,
        "document_type": "news_article",
        "title": article.get("title") or "",
        "url": article.get("url") or "",
    }


def build_disclosure_metadata(disclosure: dict, chunk_index: int) -> dict:
    """공시 데이터에 대한 Chunk Metadata를 생성한다.

    Args:
        disclosure: DB에서 조회한 공시 dict.
        chunk_index: 현재 Chunk 순번.

    Returns:
        Metadata dict.
    """
    return {
        "ticker": disclosure.get("ticker") or "",
        "source": "opendart",
        "published_at": str(disclosure.get("receipt_date") or ""),
        "chunk_index": chunk_index,
        "document_type": "disclosure",
        "report_name": disclosure.get("report_name") or "",
        "receipt_no": disclosure.get("receipt_no") or "",
        "corp_code": disclosure.get("corp_code") or "",
    }
