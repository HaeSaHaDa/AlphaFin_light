"""Disclosure Document Store repository."""
from __future__ import annotations

import json
from datetime import datetime

from src.common.db.connection import get_connection


def ensure_disclosure_tables() -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS disclosure_documents (
                    document_id BIGINT NOT NULL AUTO_INCREMENT,
                    ticker VARCHAR(20) NOT NULL,
                    corp_code VARCHAR(20) DEFAULT NULL,
                    company_name VARCHAR(100) DEFAULT NULL,
                    report_name VARCHAR(500) NOT NULL,
                    report_type VARCHAR(40) NOT NULL,
                    report_date DATE DEFAULT NULL,
                    source_type VARCHAR(30) NOT NULL,
                    document_url VARCHAR(1000) DEFAULT NULL,
                    summary TEXT DEFAULT NULL,
                    raw_text LONGTEXT DEFAULT NULL,
                    receipt_no VARCHAR(30) DEFAULT NULL,
                    metadata_json LONGTEXT DEFAULT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (document_id),
                    UNIQUE KEY uq_disclosure_doc_receipt (receipt_no),
                    KEY idx_disclosure_doc_ticker_date (ticker, report_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS disclosure_chunks (
                    chunk_id BIGINT NOT NULL AUTO_INCREMENT,
                    document_id BIGINT NOT NULL,
                    chunk_index INT NOT NULL,
                    chunk_text LONGTEXT NOT NULL,
                    section_name VARCHAR(120) DEFAULT NULL,
                    importance_score DECIMAL(6,4) DEFAULT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (chunk_id),
                    UNIQUE KEY uq_disclosure_chunk (document_id, chunk_index),
                    KEY idx_disclosure_chunk_doc (document_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS disclosure_embeddings (
                    embedding_id BIGINT NOT NULL AUTO_INCREMENT,
                    chunk_id BIGINT NOT NULL,
                    embedding_vector LONGTEXT NOT NULL,
                    embedding_model VARCHAR(80) NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (embedding_id),
                    UNIQUE KEY uq_disclosure_emb (chunk_id, embedding_model),
                    KEY idx_disclosure_emb_chunk (chunk_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS disclosure_events (
                    event_id BIGINT NOT NULL AUTO_INCREMENT,
                    ticker VARCHAR(20) NOT NULL,
                    report_type VARCHAR(40) NOT NULL,
                    title VARCHAR(500) NOT NULL,
                    report_date DATE DEFAULT NULL,
                    evidence_text TEXT DEFAULT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (event_id),
                    KEY idx_disclosure_event_ticker_date (ticker, report_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,
            )
        conn.commit()
    finally:
        conn.close()


def upsert_disclosure_documents(rows: list[dict]) -> int:
    if not rows:
        return 0
    ensure_disclosure_tables()
    sql = """
        INSERT INTO disclosure_documents
            (ticker, corp_code, company_name, report_name, report_type, report_date,
             source_type, document_url, summary, raw_text, receipt_no, metadata_json)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            report_name = VALUES(report_name),
            report_type = VALUES(report_type),
            report_date = VALUES(report_date),
            source_type = VALUES(source_type),
            document_url = VALUES(document_url),
            summary = COALESCE(VALUES(summary), summary),
            raw_text = COALESCE(VALUES(raw_text), raw_text),
            metadata_json = COALESCE(VALUES(metadata_json), metadata_json)
    """
    conn = get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            for r in rows:
                meta = r.get("metadata_json")
                if isinstance(meta, dict):
                    meta = json.dumps(meta, ensure_ascii=False)
                cur.execute(
                    sql,
                    (
                        r.get("ticker", ""),
                        r.get("corp_code"),
                        r.get("company_name"),
                        r.get("report_name", ""),
                        r.get("report_type", "UNKNOWN"),
                        r.get("report_date"),
                        r.get("source_type", "MAJOR_ISSUE"),
                        r.get("document_url"),
                        r.get("summary"),
                        r.get("raw_text"),
                        r.get("receipt_no"),
                        meta,
                    ),
                )
                inserted += cur.rowcount
        conn.commit()
        return inserted
    finally:
        conn.close()


def list_disclosures_by_ticker(ticker: str, limit: int = 50) -> list[dict]:
    ensure_disclosure_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT document_id, ticker, corp_code, company_name, report_name,
                       report_type, report_date, source_type, document_url,
                       summary, receipt_no, created_at
                FROM disclosure_documents
                WHERE ticker = %s
                ORDER BY report_date DESC, document_id DESC
                LIMIT %s
                """,
                (ticker, limit),
            )
            return cur.fetchall()
    finally:
        conn.close()


def get_latest_disclosure_report_date(ticker: str) -> str:
    ensure_disclosure_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT MAX(report_date) AS latest FROM disclosure_documents WHERE ticker = %s",
                (ticker,),
            )
            row = cur.fetchone()
    finally:
        conn.close()
    return str(row["latest"]) if row and row.get("latest") else ""


def list_disclosures_for_chunking(ticker: str, limit: int = 120) -> list[dict]:
    ensure_disclosure_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT document_id, ticker, report_name, report_type, report_date,
                       raw_text, summary, receipt_no
                FROM disclosure_documents
                WHERE ticker = %s
                ORDER BY report_date DESC, document_id DESC
                LIMIT %s
                """,
                (ticker, limit),
            )
            return cur.fetchall()
    finally:
        conn.close()


def insert_disclosure_chunks(rows: list[dict]) -> int:
    if not rows:
        return 0
    ensure_disclosure_tables()
    conn = get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            for r in rows:
                cur.execute(
                    """
                    INSERT INTO disclosure_chunks
                        (document_id, chunk_index, chunk_text, section_name, importance_score)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        chunk_text = VALUES(chunk_text),
                        section_name = VALUES(section_name),
                        importance_score = VALUES(importance_score)
                    """,
                    (
                        r["document_id"],
                        r["chunk_index"],
                        r["chunk_text"],
                        r.get("section_name"),
                        r.get("importance_score"),
                    ),
                )
                inserted += cur.rowcount
        conn.commit()
        return inserted
    finally:
        conn.close()


def sync_disclosure_document_chunks(document_id: int, rows: list[dict]) -> int:
    ensure_disclosure_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT chunk_index, chunk_text, section_name, importance_score
                FROM disclosure_chunks
                WHERE document_id = %s
                ORDER BY chunk_index
                """,
                (document_id,),
            )
            existing = cur.fetchall()
            comparable = [
                {
                    "chunk_index": row["chunk_index"],
                    "chunk_text": row["chunk_text"],
                    "section_name": row.get("section_name"),
                    "importance_score": float(row.get("importance_score") or 0),
                }
                for row in rows
            ]
            existing_comparable = [
                {
                    "chunk_index": row["chunk_index"],
                    "chunk_text": row["chunk_text"],
                    "section_name": row.get("section_name"),
                    "importance_score": float(row.get("importance_score") or 0),
                }
                for row in existing
            ]
            if existing_comparable == comparable:
                return 0

            cur.execute(
                """
                DELETE e FROM disclosure_embeddings e
                JOIN disclosure_chunks c ON c.chunk_id = e.chunk_id
                WHERE c.document_id = %s
                """,
                (document_id,),
            )
            for row in rows:
                cur.execute(
                    """
                    INSERT INTO disclosure_chunks
                        (document_id, chunk_index, chunk_text, section_name, importance_score)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        chunk_text = VALUES(chunk_text),
                        section_name = VALUES(section_name),
                        importance_score = VALUES(importance_score)
                    """,
                    (
                        document_id,
                        row["chunk_index"],
                        row["chunk_text"],
                        row.get("section_name"),
                        row.get("importance_score"),
                    ),
                )
            cur.execute(
                "DELETE FROM disclosure_chunks WHERE document_id = %s AND chunk_index >= %s",
                (document_id, len(rows)),
            )
        conn.commit()
        return len(rows)
    finally:
        conn.close()


def list_disclosure_chunks(ticker: str, limit: int = 300) -> list[dict]:
    ensure_disclosure_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.chunk_id, c.document_id, c.chunk_index, c.chunk_text,
                       c.section_name, c.importance_score,
                       d.ticker, d.report_name, d.report_type, d.report_date
                FROM disclosure_chunks c
                JOIN disclosure_documents d ON d.document_id = c.document_id
                WHERE d.ticker = %s
                ORDER BY d.report_date DESC, c.chunk_index ASC
                LIMIT %s
                """,
                (ticker, limit),
            )
            return cur.fetchall()
    finally:
        conn.close()


def list_disclosure_chunks_without_embedding(
    ticker: str,
    model: str,
    limit: int = 300,
) -> list[dict]:
    ensure_disclosure_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.chunk_id, c.document_id, c.chunk_index, c.chunk_text,
                       c.section_name, c.importance_score,
                       d.ticker, d.report_name, d.report_type, d.report_date
                FROM disclosure_chunks c
                JOIN disclosure_documents d ON d.document_id = c.document_id
                LEFT JOIN disclosure_embeddings e
                    ON e.chunk_id = c.chunk_id
                   AND e.embedding_model = %s
                WHERE d.ticker = %s
                  AND e.embedding_id IS NULL
                ORDER BY d.report_date DESC, c.chunk_index ASC
                LIMIT %s
                """,
                (model, ticker, limit),
            )
            return cur.fetchall()
    finally:
        conn.close()


def insert_disclosure_embeddings(rows: list[dict]) -> int:
    if not rows:
        return 0
    ensure_disclosure_tables()
    conn = get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            for r in rows:
                cur.execute(
                    """
                    INSERT INTO disclosure_embeddings
                        (chunk_id, embedding_vector, embedding_model)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        embedding_vector = VALUES(embedding_vector),
                        embedding_model = VALUES(embedding_model),
                        created_at = CURRENT_TIMESTAMP
                    """,
                    (
                        r["chunk_id"],
                        json.dumps(r["embedding_vector"], ensure_ascii=False),
                        r.get("embedding_model", "text-embedding-3-small"),
                    ),
                )
                inserted += cur.rowcount
        conn.commit()
        return inserted
    finally:
        conn.close()


def list_timeline_events(ticker: str, limit: int = 30) -> list[dict]:
    ensure_disclosure_tables()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT report_date, report_type, report_name, summary
                FROM disclosure_documents
                WHERE ticker = %s
                ORDER BY report_date DESC
                LIMIT %s
                """,
                (ticker, limit),
            )
            return cur.fetchall()
    finally:
        conn.close()
