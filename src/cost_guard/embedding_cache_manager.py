"""Embedding hash 기반 중복 생성 방지."""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
HASH_DIR = PROJECT_ROOT / "data" / "cost_guard" / "embedding_hashes"


def chunk_hash(chunk_text: str, model: str = "text-embedding-3-small") -> str:
    raw = f"{model}:{chunk_text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def is_hash_cached(text_hash: str) -> bool:
    return (HASH_DIR / f"{text_hash}.json").exists()


def mark_hash_cached(text_hash: str, chunk_id: int) -> None:
    HASH_DIR.mkdir(parents=True, exist_ok=True)
    path = HASH_DIR / f"{text_hash}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"chunk_id": chunk_id, "hash": text_hash}, f)


def chunk_already_embedded(chunk_id: int, chunk_text: str, model: str) -> bool:
    """DB 또는 hash cache에 이미 embedding이 있는지 확인."""
    h = chunk_hash(chunk_text, model)
    if is_hash_cached(h):
        return True
    from src.common.db.connection import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 1 FROM document_embeddings
                WHERE chunk_id = %s AND embedding_model = %s LIMIT 1
                """,
                (chunk_id, model),
            )
            return cur.fetchone() is not None
    finally:
        conn.close()
