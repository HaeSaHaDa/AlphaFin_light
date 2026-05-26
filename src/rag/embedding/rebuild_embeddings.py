"""문제 있는 Embedding을 재생성하고 DB를 갱신하는 스크립트."""
from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
sys.path.insert(0, str(DB_MODULE))

from connection import get_connection  # noqa: E402
from embedder import generate_embedding, DEFAULT_MODEL  # noqa: E402
from inspect_embeddings import (  # noqa: E402
    inspect_embedding_rows,
    detect_missing_embeddings,
)

logger = logging.getLogger(__name__)

REQUEST_DELAY_SEC = 0.5


def load_chunks_by_ids(chunk_ids: list[int]) -> list[dict]:
    """지정된 chunk_id 목록에 해당하는 Chunk 데이터를 조회한다."""
    if not chunk_ids:
        return []
    conn = get_connection()
    try:
        placeholders = ", ".join(["%s"] * len(chunk_ids))
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT id AS chunk_id, chunk_text, document_type, ticker "
                f"FROM document_chunks WHERE id IN ({placeholders}) "
                f"ORDER BY id",
                chunk_ids,
            )
            return cur.fetchall()
    finally:
        conn.close()


def delete_embeddings_by_chunk_ids(chunk_ids: list[int]) -> int:
    """기존 더미/비정상 Embedding을 삭제한다."""
    if not chunk_ids:
        return 0
    conn = get_connection()
    try:
        placeholders = ", ".join(["%s"] * len(chunk_ids))
        with conn.cursor() as cur:
            cur.execute(
                f"DELETE FROM document_embeddings "
                f"WHERE chunk_id IN ({placeholders})",
                chunk_ids,
            )
            deleted = cur.rowcount
        conn.commit()
        logger.info("기존 Embedding 삭제: %d건  chunk_ids=%s", deleted, chunk_ids)
        return deleted
    except Exception:
        conn.rollback()
        logger.exception("Embedding 삭제 실패")
        return 0
    finally:
        conn.close()


def rebuild_and_save(
    chunks: list[dict],
    model: str = DEFAULT_MODEL,
) -> int:
    """Chunk 목록에 대해 Embedding을 재생성하고 DB에 저장한다."""
    if not chunks:
        return 0

    conn = get_connection()
    inserted = 0
    sql = """
        INSERT IGNORE INTO document_embeddings
            (chunk_id, embedding_model, embedding_dimension, embedding_vector)
        VALUES (%s, %s, %s, %s)
    """

    try:
        with conn.cursor() as cur:
            for i, chunk in enumerate(chunks):
                chunk_id = chunk["chunk_id"]
                text = chunk.get("chunk_text", "")

                logger.info(
                    "Embedding 생성 중  chunk_id=%d  (%d/%d)",
                    chunk_id, i + 1, len(chunks),
                )

                vec = generate_embedding(text, model)
                if not vec:
                    logger.warning("  chunk_id=%d  Embedding 생성 실패", chunk_id)
                    continue

                vec_json = json.dumps(vec)
                cur.execute(sql, (chunk_id, model, len(vec), vec_json))
                inserted += cur.rowcount

                logger.info("  chunk_id=%d  dim=%d  OK", chunk_id, len(vec))

                if i < len(chunks) - 1:
                    time.sleep(REQUEST_DELAY_SEC)

        conn.commit()
        logger.info("Embedding 재생성 INSERT: %d / %d건", inserted, len(chunks))
        return inserted
    except Exception:
        conn.rollback()
        logger.exception("Embedding 재생성 실패")
        return 0
    finally:
        conn.close()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

    logger.info("=== Embedding 재생성 시작 ===")

    # 1. 점검
    logger.info("--- 1. 현재 상태 점검 ---")
    results = inspect_embedding_rows()
    invalid_ids = results["invalid"]
    missing_ids = detect_missing_embeddings()
    all_problem_ids = sorted(set(invalid_ids + missing_ids))

    logger.info("재생성 대상: %d건  chunk_ids=%s", len(all_problem_ids), all_problem_ids)

    if not all_problem_ids:
        logger.info("재생성 대상 없음 — 종료")
        return 0

    # 2. 기존 더미 삭제
    dummy_to_delete = [cid for cid in invalid_ids if cid not in missing_ids]
    if dummy_to_delete:
        logger.info("--- 2. 기존 더미 Embedding 삭제 ---")
        delete_embeddings_by_chunk_ids(dummy_to_delete)

    # 3. Chunk 조회
    logger.info("--- 3. 대상 Chunk 조회 ---")
    chunks = load_chunks_by_ids(all_problem_ids)
    logger.info("조회된 Chunk: %d건", len(chunks))

    # 4. 재생성
    logger.info("--- 4. OpenAI Embedding 재생성 ---")
    inserted = rebuild_and_save(chunks)
    logger.info("재생성 완료: %d건", inserted)

    # 5. 재점검
    logger.info("--- 5. 재점검 ---")
    results_after = inspect_embedding_rows()
    logger.info(
        "재점검  총=%d  정상=%d  비정상=%d",
        results_after["total"],
        len(results_after["valid"]),
        len(results_after["invalid"]),
    )

    missing_after = detect_missing_embeddings()
    logger.info("Embedding 미존재 chunk: %d", len(missing_after))

    logger.info("=== Embedding 재생성 완료 ===")
    return 0 if len(results_after["invalid"]) == 0 and len(missing_after) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
