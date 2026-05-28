"""종목별 DB 수집·임베딩 현황."""
from __future__ import annotations

from src.common.db.connection import get_connection


def get_ticker_stats(ticker: str) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM news_articles WHERE ticker = %s",
                (ticker,),
            )
            news_count = int(cur.fetchone()["cnt"])

            cur.execute(
                "SELECT COUNT(*) AS cnt FROM dart_disclosures WHERE ticker = %s",
                (ticker,),
            )
            disclosure_count = int(cur.fetchone()["cnt"])

            cur.execute(
                "SELECT COUNT(*) AS cnt FROM stock_prices WHERE ticker = %s",
                (ticker,),
            )
            price_count = int(cur.fetchone()["cnt"])

            cur.execute(
                "SELECT COUNT(*) AS cnt FROM document_chunks WHERE ticker = %s",
                (ticker,),
            )
            chunk_count = int(cur.fetchone()["cnt"])

            cur.execute(
                """
                SELECT COUNT(*) AS cnt
                FROM document_embeddings de
                JOIN document_chunks dc ON de.chunk_id = dc.id
                WHERE dc.ticker = %s
                """,
                (ticker,),
            )
            embedding_count = int(cur.fetchone()["cnt"])

            cur.execute(
                """
                SELECT COUNT(*) AS cnt
                FROM document_chunks dc
                LEFT JOIN document_embeddings de
                  ON de.chunk_id = dc.id AND de.embedding_model = %s
                WHERE dc.ticker = %s AND de.id IS NULL
                """,
                ("text-embedding-3-small", ticker),
            )
            pending_embedding_count = int(cur.fetchone()["cnt"])
    finally:
        conn.close()

    return {
        "news_count": news_count,
        "disclosure_count": disclosure_count,
        "price_count": price_count,
        "chunk_count": chunk_count,
        "embedding_count": embedding_count,
        "pending_embedding_count": pending_embedding_count,
    }


def fetch_recent_disclosures(ticker: str, limit: int = 5) -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT report_name, receipt_date, receipt_no, disclosure_type
                FROM dart_disclosures
                WHERE ticker = %s
                ORDER BY receipt_date DESC, id DESC
                LIMIT %s
                """,
                (ticker, limit),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    return [
        {
            "report_name": r.get("report_name") or "",
            "receipt_date": str(r["receipt_date"]) if r.get("receipt_date") else "",
            "receipt_no": r.get("receipt_no") or "",
            "disclosure_type": r.get("disclosure_type") or "",
        }
        for r in rows
    ]
