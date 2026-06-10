"""Vector index 상태 · ingestion cache."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = PROJECT_ROOT / "data" / "ingestion_cache"
LOG_DIR = PROJECT_ROOT / "data" / "ingestion_logs"
NEWS_CACHE_TTL_HOURS = 12


def _db_embedding_count(ticker: str) -> int:
    from src.common.db.connection import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*) AS cnt
                FROM document_embeddings de
                JOIN document_chunks dc ON de.chunk_id = dc.id
                WHERE dc.ticker = %s
                """,
                (ticker,),
            )
            row = cur.fetchone()
            return int(row["cnt"]) if row else 0
    finally:
        conn.close()


def cache_path(ticker: str) -> Path:
    return CACHE_DIR / f"{ticker}.json"


def load_cache(ticker: str) -> dict | None:
    path = cache_path(ticker)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def get_news_cache_status(
    ticker: str,
    *,
    ttl_hours: int = NEWS_CACHE_TTL_HOURS,
) -> dict:
    payload = load_cache(ticker)
    completed_at = (payload or {}).get("completed_at", "")
    fresh = False
    age_hours: float | None = None
    if completed_at:
        try:
            completed = datetime.fromisoformat(completed_at)
            age = datetime.now() - completed
            age_hours = max(0.0, age.total_seconds() / 3600)
            fresh = age <= timedelta(hours=ttl_hours)
        except ValueError:
            pass

    if not payload:
        usage = "MISS"
    elif fresh:
        usage = "HIT"
    else:
        usage = "STALE"
    return {
        "cache_status": usage,
        "cache_fresh": fresh,
        "cache_updated_at": completed_at,
        "cache_age_hours": round(age_hours, 2) if age_hours is not None else None,
        "cache_ttl_hours": ttl_hours,
    }


def is_ticker_ready(ticker: str, min_embeddings: int = 3) -> bool:
    """TTL 안에 ingestion이 완료된 종목인지 확인한다."""
    data = load_cache(ticker)
    if not data or data.get("status") != "completed":
        return False
    status = get_news_cache_status(ticker)
    return bool(status["cache_fresh"]) and _db_embedding_count(ticker) >= min_embeddings


def save_cache(
    ticker: str,
    company_name: str,
    *,
    status: str,
    documents: int,
    chunks: int,
    embeddings: int,
) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "ticker": ticker,
        "company_name": company_name,
        "status": status,
        "documents": documents,
        "chunks": chunks,
        "embeddings": embeddings,
        "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    path = cache_path(ticker)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    logger.info("ingestion cache 저장  %s", path.name)
    return path


def append_log(ticker: str, payload: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = LOG_DIR / f"{ticker}_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
