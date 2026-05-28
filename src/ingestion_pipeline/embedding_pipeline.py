"""document_chunks → document_embeddings (중복·비용 방지)."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from src.cost_guard.budget_guard import require_budget
from src.cost_guard.cost_estimator import estimate_embedding_cost
from src.cost_guard.embedding_cache_manager import (
    chunk_already_embedded,
    chunk_hash,
    mark_hash_cached,
)
from src.cost_guard.limits import MAX_EMBED_BATCH
from src.cost_guard.presentation_mode import is_presentation_mode
from src.cost_guard.token_usage_logger import log_usage

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EMBED_DIR = PROJECT_ROOT / "src" / "rag" / "embedding"
DB_DIR = PROJECT_ROOT / "src" / "common" / "db"

DEFAULT_MODEL = "text-embedding-3-small"


def _chunks_without_embedding(ticker: str, limit: int = MAX_EMBED_BATCH) -> list[dict]:
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
                LIMIT %s
                """,
                (DEFAULT_MODEL, ticker, limit),
            )
            return cur.fetchall()
    finally:
        conn.close()


def _estimate_tokens(chunks: list[dict]) -> int:
    return sum(max(1, len(c.get("chunk_text", "")) // 4) for c in chunks)


def _ticker_embedding_count(ticker: str) -> int:
    from src.ingestion_pipeline.vector_index_manager import _db_embedding_count

    return _db_embedding_count(ticker)


def run_embedding(ticker: str, *, dry_run: bool = False) -> dict:
    """미임베딩 chunk에 대해 embedding을 생성·저장한다.

    Returns:
        inserted, skipped, pending — 기존 embedding은 skipped로 집계.
    """
    must_embed = _ticker_embedding_count(ticker) < 1
    pending = _chunks_without_embedding(ticker)
    to_embed: list[dict] = []
    for c in pending:
        if chunk_already_embedded(c["chunk_id"], c["chunk_text"], DEFAULT_MODEL):
            continue
        to_embed.append(c)

    skipped = len(pending) - len(to_embed)

    if not to_embed:
        logger.info(
            "임베딩 생략  ticker=%s  pending=%d  skipped=%d",
            ticker, len(pending), skipped,
        )
        return {
            "inserted": 0,
            "skipped": len(pending),
            "pending": len(pending),
        }

    if dry_run or (is_presentation_mode() and not must_embed):
        logger.info(
            "embedding skip (dry-run/presentation)  ticker=%s  would_embed=%d",
            ticker, len(to_embed),
        )
        return {
            "inserted": 0,
            "skipped": len(pending),
            "pending": len(pending),
        }

    est_tokens = _estimate_tokens(to_embed)
    require_budget(estimate_embedding_cost(est_tokens))

    if str(EMBED_DIR) not in sys.path:
        sys.path.insert(0, str(EMBED_DIR))
    if str(DB_DIR) not in sys.path:
        sys.path.insert(0, str(DB_DIR))

    from embedder import generate_embeddings  # type: ignore[import]
    from storage import save_embedding_to_db  # type: ignore[import]

    try:
        vectors = generate_embeddings(to_embed, model=DEFAULT_MODEL)
    except RuntimeError:
        raise
    except Exception:
        logger.exception("Embedding API 실패  ticker=%s — 더미 벡터 미사용", ticker)
        return {"inserted": 0, "skipped": skipped, "pending": len(pending)}

    if not vectors:
        return {"inserted": 0, "skipped": skipped + len(to_embed), "pending": len(pending)}

    inserted = save_embedding_to_db(vectors)
    for row in vectors:
        chunk_id = row["chunk_id"]
        text = next(
            (c["chunk_text"] for c in to_embed if c["chunk_id"] == chunk_id),
            "",
        )
        h = chunk_hash(text, DEFAULT_MODEL)
        mark_hash_cached(h, chunk_id)

    log_usage(
        operation="embedding_batch",
        model=DEFAULT_MODEL,
        embedding_tokens=est_tokens,
        meta={"ticker": ticker, "count": inserted},
    )
    skipped += len(to_embed) - inserted
    logger.info(
        "embedding 저장  ticker=%s  inserted=%d  skipped=%d",
        ticker, inserted, skipped,
    )
    return {
        "inserted": inserted,
        "skipped": skipped,
        "pending": len(pending),
    }
