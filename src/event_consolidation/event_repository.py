"""Market events DB repository."""
from __future__ import annotations

import json
import logging
from datetime import datetime

from src.common.db.connection import get_connection

logger = logging.getLogger(__name__)


def ensure_event_tables() -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS market_events (
                    event_id VARCHAR(32) NOT NULL,
                    trace_id VARCHAR(40) DEFAULT NULL,
                    ticker VARCHAR(20) NOT NULL,
                    company_name VARCHAR(100) DEFAULT NULL,
                    canonical_title VARCHAR(500) NOT NULL,
                    event_summary TEXT DEFAULT NULL,
                    event_type VARCHAR(40) DEFAULT 'market_news',
                    event_date DATE DEFAULT NULL,
                    confidence_score DECIMAL(6,4) DEFAULT NULL,
                    importance_score DECIMAL(6,4) DEFAULT NULL,
                    impact_direction VARCHAR(20) DEFAULT 'neutral',
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (event_id),
                    KEY idx_market_events_ticker (ticker),
                    KEY idx_market_events_trace (trace_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS event_evidence (
                    evidence_id BIGINT NOT NULL AUTO_INCREMENT,
                    event_id VARCHAR(32) NOT NULL,
                    source_type VARCHAR(20) NOT NULL,
                    source_id VARCHAR(80) DEFAULT NULL,
                    title VARCHAR(500) DEFAULT NULL,
                    url VARCHAR(1000) DEFAULT NULL,
                    published_at DATETIME DEFAULT NULL,
                    relevance_score DECIMAL(6,4) DEFAULT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (evidence_id),
                    KEY idx_event_evidence_event (event_id),
                    UNIQUE KEY uq_event_evidence_src (event_id, source_type, source_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS event_memory_layers (
                    event_id VARCHAR(32) NOT NULL,
                    memory_layer VARCHAR(10) NOT NULL,
                    entered_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    promoted_from VARCHAR(10) DEFAULT NULL,
                    importance_score DECIMAL(6,4) DEFAULT NULL,
                    is_active TINYINT(1) NOT NULL DEFAULT 1,
                    PRIMARY KEY (event_id, memory_layer),
                    KEY idx_event_memory_active (event_id, is_active)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,
            )
        conn.commit()
    finally:
        conn.close()


def upsert_market_event(event: dict, evidence: list[dict]) -> None:
    ensure_event_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO market_events
                    (event_id, trace_id, ticker, company_name, canonical_title, event_summary,
                     event_type, event_date, confidence_score, importance_score, impact_direction)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    trace_id = COALESCE(VALUES(trace_id), trace_id),
                    canonical_title = VALUES(canonical_title),
                    event_summary = VALUES(event_summary),
                    confidence_score = VALUES(confidence_score),
                    importance_score = VALUES(importance_score),
                    impact_direction = VALUES(impact_direction),
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    event["event_id"],
                    event.get("trace_id"),
                    event.get("ticker", ""),
                    event.get("company_name"),
                    event.get("canonical_title", ""),
                    event.get("event_summary"),
                    event.get("event_type", "market_news"),
                    event.get("event_date"),
                    event.get("confidence_score"),
                    event.get("importance_score"),
                    event.get("impact_direction", "neutral"),
                ),
            )
            for ev in evidence:
                cur.execute(
                    """
                    INSERT INTO event_evidence
                        (event_id, source_type, source_id, title, url, published_at, relevance_score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        title = VALUES(title),
                        relevance_score = VALUES(relevance_score)
                    """,
                    (
                        event["event_id"],
                        ev.get("source_type", "CHUNK"),
                        str(ev.get("source_id", ""))[:80],
                        ev.get("title"),
                        ev.get("url"),
                        ev.get("published_at"),
                        ev.get("relevance_score"),
                    ),
                )
        conn.commit()
    except Exception:
        logger.exception("market_events upsert 실패  event_id=%s", event.get("event_id"))
        raise
    finally:
        conn.close()


def list_events_by_trace(trace_id: str) -> list[dict]:
    ensure_event_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT event_id, trace_id, ticker, company_name, canonical_title, event_summary,
                       event_type, event_date, confidence_score, importance_score, impact_direction,
                       created_at, updated_at
                FROM market_events
                WHERE trace_id = %s
                ORDER BY confidence_score DESC, updated_at DESC
                """,
                (trace_id,),
            )
            return list(cur.fetchall() or [])
    finally:
        conn.close()


def list_events_by_ticker(ticker: str, limit: int = 40) -> list[dict]:
    ensure_event_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT event_id, trace_id, ticker, company_name, canonical_title, event_summary,
                       event_type, event_date, confidence_score, importance_score, impact_direction,
                       created_at, updated_at
                FROM market_events
                WHERE ticker = %s
                ORDER BY updated_at DESC
                LIMIT %s
                """,
                (ticker, limit),
            )
            return list(cur.fetchall() or [])
    finally:
        conn.close()


def list_evidence_by_event(event_id: str) -> list[dict]:
    ensure_event_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT evidence_id, event_id, source_type, source_id, title, url,
                       published_at, relevance_score, created_at
                FROM event_evidence
                WHERE event_id = %s
                ORDER BY relevance_score DESC
                """,
                (event_id,),
            )
            return list(cur.fetchall() or [])
    finally:
        conn.close()


def list_memory_layers(event_id: str | None = None, trace_ticker: str | None = None) -> list[dict]:
    ensure_event_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if event_id:
                cur.execute(
                    """
                    SELECT eml.event_id, eml.memory_layer, eml.entered_at, eml.promoted_from,
                           eml.importance_score, eml.is_active, me.ticker, me.canonical_title
                    FROM event_memory_layers eml
                    JOIN market_events me ON me.event_id = eml.event_id
                    WHERE eml.event_id = %s
                    ORDER BY eml.is_active DESC, eml.entered_at DESC
                    """,
                    (event_id,),
                )
            else:
                cur.execute(
                    """
                    SELECT eml.event_id, eml.memory_layer, eml.entered_at, eml.promoted_from,
                           eml.importance_score, eml.is_active, me.ticker, me.canonical_title
                    FROM event_memory_layers eml
                    JOIN market_events me ON me.event_id = eml.event_id
                    WHERE me.ticker = %s
                    ORDER BY eml.is_active DESC, eml.entered_at DESC
                    """,
                    (trace_ticker or "",),
                )
            return list(cur.fetchall() or [])
    finally:
        conn.close()


def set_memory_layer(
    event_id: str,
    memory_layer: str,
    *,
    promoted_from: str | None = None,
    importance_score: float | None = None,
    deactivate_others: bool = True,
) -> None:
    ensure_event_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if deactivate_others:
                cur.execute(
                    "UPDATE event_memory_layers SET is_active = 0 WHERE event_id = %s",
                    (event_id,),
                )
            cur.execute(
                """
                INSERT INTO event_memory_layers
                    (event_id, memory_layer, promoted_from, importance_score, is_active)
                VALUES (%s, %s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE
                    promoted_from = COALESCE(VALUES(promoted_from), promoted_from),
                    importance_score = COALESCE(VALUES(importance_score), importance_score),
                    is_active = 1,
                    entered_at = CURRENT_TIMESTAMP
                """,
                (event_id, memory_layer, promoted_from, importance_score),
            )
        conn.commit()
    finally:
        conn.close()


def load_chunks_by_ids(chunk_ids: list[int]) -> dict[int, dict]:
    if not chunk_ids:
        return {}
    conn = get_connection()
    try:
        placeholders = ", ".join(["%s"] * len(chunk_ids))
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT id AS chunk_id, chunk_text, document_type, ticker
                FROM document_chunks
                WHERE id IN ({placeholders})
                """,
                chunk_ids,
            )
            rows = cur.fetchall() or []
        out: dict[int, dict] = {}
        for row in rows:
            cid = int(row["chunk_id"])
            text = row.get("chunk_text") or ""
            title = text.split("\n")[0][:120] if text else f"chunk #{cid}"
            out[cid] = {
                "chunk_id": cid,
                "title": title,
                "body": text[:500],
                "document_type": row.get("document_type", "news_article"),
                "ticker": row.get("ticker", ""),
            }
        return out
    except Exception:
        logger.warning("chunk metadata load 실패", exc_info=True)
        return {}
    finally:
        conn.close()
