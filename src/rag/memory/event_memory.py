"""Market Event Memory 저장 및 관리 모듈."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EVENT_DIR = PROJECT_ROOT / "data" / "memory" / "market_events"

IMPACT_TYPES = ["positive", "negative", "neutral", "mixed"]


def extract_market_events(analysis_result: dict) -> list[dict]:
    """분석 결과에서 주요 시장 이벤트를 추출한다.

    bullish/bearish/risks 항목을 이벤트로 변환한다.

    Args:
        analysis_result: Character/Financial Analysis 결과.

    Returns:
        추출된 이벤트 목록.
    """
    events: list[dict] = []
    query = analysis_result.get("query", "")
    refs = analysis_result.get("referenced_chunks", [])

    ticker = "unknown"
    for ref in refs:
        t = ref.get("ticker")
        if t:
            ticker = t
            break

    news_refs = [r for r in refs if r.get("document_type") == "news_article"]
    disc_refs = [r for r in refs if r.get("document_type") == "disclosure"]

    for factor in analysis_result.get("bullish_factors", []):
        events.append(build_event_memory({
            "ticker": ticker,
            "event_name": factor[:50],
            "event_summary": factor,
            "related_news": [r.get("chunk_id") for r in news_refs],
            "related_disclosures": [r.get("chunk_id") for r in disc_refs],
            "impact_type": "positive",
            "source_query": query,
        }))

    for factor in analysis_result.get("bearish_factors", []):
        events.append(build_event_memory({
            "ticker": ticker,
            "event_name": factor[:50],
            "event_summary": factor,
            "related_news": [r.get("chunk_id") for r in news_refs],
            "related_disclosures": [r.get("chunk_id") for r in disc_refs],
            "impact_type": "negative",
            "source_query": query,
        }))

    for risk in analysis_result.get("risks", []):
        events.append(build_event_memory({
            "ticker": ticker,
            "event_name": risk[:50],
            "event_summary": risk,
            "related_news": [r.get("chunk_id") for r in news_refs],
            "related_disclosures": [r.get("chunk_id") for r in disc_refs],
            "impact_type": "negative",
            "source_query": query,
        }))

    logger.info(
        "Market Event 추출  query='%s'  이벤트=%d건",
        query[:30], len(events),
    )
    return events


def build_event_memory(event_data: dict) -> dict:
    """Event Memory dict를 생성한다."""
    return {
        "memory_type": "market_event",
        "ticker": event_data.get("ticker", "unknown"),
        "event_name": event_data.get("event_name", ""),
        "event_summary": event_data.get("event_summary", ""),
        "related_news": event_data.get("related_news", []),
        "related_disclosures": event_data.get("related_disclosures", []),
        "event_date": datetime.now().strftime("%Y-%m-%d"),
        "impact_type": event_data.get("impact_type", "neutral"),
        "source_query": event_data.get("source_query", ""),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def save_market_event_memory(
    events: list[dict],
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path | None:
    """Market Event Memory를 JSON 파일에 추가 저장한다."""
    out = Path(output_dir) if output_dir else DEFAULT_EVENT_DIR
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        ticker = events[0].get("ticker", "unknown") if events else "unknown"
        filename = f"{ticker}_events.json"

    filepath = out / filename

    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, Exception):
            logger.warning("기존 Event 파일 파싱 실패, 새로 생성  %s", filepath)
            existing = []

    existing.extend(events)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    logger.info(
        "Market Event 저장  %s  추가=%d  총=%d건",
        filepath.name, len(events), len(existing),
    )
    return filepath


def load_market_events(
    ticker: str | None = None,
    output_dir: Path | str | None = None,
) -> list[dict]:
    """저장된 Market Event Memory를 로드한다.

    Args:
        ticker: 특정 종목의 Event만 로드. None이면 전체.
        output_dir: Event 저장 디렉토리.

    Returns:
        Event dict 목록.
    """
    out = Path(output_dir) if output_dir else DEFAULT_EVENT_DIR
    if not out.exists():
        return []

    all_events: list[dict] = []

    if ticker:
        filepath = out / f"{ticker}_events.json"
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    all_events = json.load(f)
            except (json.JSONDecodeError, Exception):
                logger.warning("Event 파일 파싱 실패  %s", filepath)
    else:
        for fp in out.glob("*_events.json"):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_events.extend(data)
            except (json.JSONDecodeError, Exception):
                logger.warning("Event 파일 파싱 실패  %s", fp)

    logger.info(
        "Market Event 로드  ticker=%s  총=%d건",
        ticker or "all", len(all_events),
    )
    return all_events
