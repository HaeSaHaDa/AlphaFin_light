"""document_chunks → document_embeddings (중복 방지)."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EMBED_DIR = PROJECT_ROOT / "src" / "rag" / "embedding"
DB_DIR = PROJECT_ROOT / "src" / "common" / "db"

DEFAULT_MODEL = "text-embedding-3-small"


def _chunks_without_embedding(ticker: str) -> list[dict]:
    from src.common.db.connection import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT dc.id AS chunk_id, dc.chunk_text
                FROM document_chunks dc
                LEFT JOIN document_embeddings de
                  ON de.chunk_id = dc.id AND de.embedding_model = %s
                WHERE dc.ticker = %s AND de.id IS NULL
                ORDER BY dc.id
                LIMIT 50
                """,
                (DEFAULT_MODEL, ticker),
            )
            return cur.fetchall()
    finally:
        conn.close()


def run_embedding(ticker: str) -> int:
    """미임베딩 chunk에 대해 embedding을 생성·저장한다."""
    if str(EMBED_DIR) not in sys.path:
        sys.path.insert(0, str(EMBED_DIR))
    if str(DB_DIR) not in sys.path:
        sys.path.insert(0, str(DB_DIR))

    from embedder import generate_embeddings  # type: ignore[import]
    from storage import save_embedding_to_db  # type: ignore[import]

    pending = _chunks_without_embedding(ticker)
    if not pending:
        logger.info("임베딩 대상 없음  ticker=%s", ticker)
        return 0

    try:
        vectors = generate_embeddings(pending, model=DEFAULT_MODEL)
    except Exception:
        logger.exception("Embedding API 실패  ticker=%s — 더미 벡터 미사용", ticker)
        return 0

    if not vectors:
        return 0

    inserted = save_embedding_to_db(vectors)
    logger.info("embedding 저장  ticker=%s  inserted=%d", ticker, inserted)
    return inserted
