"""삼성전자 Chunk 기반 Embedding 생성 및 저장 검증 스크립트."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
sys.path.insert(0, str(DB_MODULE))

from connection import get_connection  # noqa: E402
from init_schema import initialize_database  # noqa: E402

from embedder import generate_embeddings  # noqa: E402
from storage import save_embedding_json, save_embedding_to_db  # noqa: E402

SAMPLE_LIMIT = 3


def fetch_sample_chunks() -> list[dict]:
    """DB에서 삼성전자 Chunk 샘플을 조회한다."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id AS chunk_id, document_type, source_table, "
                "source_id, ticker, chunk_index, chunk_text, chunk_length "
                "FROM document_chunks "
                "WHERE ticker = %s "
                "ORDER BY id "
                "LIMIT %s",
                ("005930", SAMPLE_LIMIT),
            )
            return cur.fetchall()
    finally:
        conn.close()


def verify_db(logger: logging.Logger) -> bool:
    """document_embeddings 테이블 행 수를 확인한다."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS cnt FROM document_embeddings")
            result = cur.fetchone()
            cnt = result["cnt"] if result else 0
            logger.info("검증  document_embeddings  rows=%d", cnt)

            if cnt > 0:
                cur.execute(
                    "SELECT chunk_id, embedding_model, embedding_dimension "
                    "FROM document_embeddings LIMIT 3"
                )
                for row in cur.fetchall():
                    logger.info(
                        "  chunk_id=%s  model=%s  dim=%s",
                        row["chunk_id"],
                        row["embedding_model"],
                        row["embedding_dimension"],
                    )
            return cnt > 0
    finally:
        conn.close()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Embedding 샘플 검증 시작 ===")

    # 1. 스키마 초기화
    logger.info("--- 1. 스키마 초기화 ---")
    if not initialize_database():
        logger.error("스키마 초기화 실패")
        return 1

    # 2. Chunk 샘플 조회
    logger.info("--- 2. Chunk 샘플 조회 ---")
    chunks = fetch_sample_chunks()
    logger.info("조회된 Chunk: %d건", len(chunks))

    if not chunks:
        logger.error("Chunk 데이터 없음 (TASK-007 실행 필요)")
        return 1

    for c in chunks:
        logger.info(
            "  chunk_id=%s  type=%s  len=%s",
            c["chunk_id"], c["document_type"], c["chunk_length"],
        )

    # 3. Embedding 생성
    logger.info("--- 3. Embedding 생성 ---")
    embeddings = generate_embeddings(chunks)

    if not embeddings:
        logger.error("Embedding 생성 실패")
        return 1

    for emb in embeddings:
        logger.info(
            "  chunk_id=%s  model=%s  dim=%d  vector_preview=%s",
            emb["chunk_id"],
            emb["embedding_model"],
            emb["embedding_dimension"],
            emb["embedding_vector"][:3],
        )

    # 4. JSON 저장
    logger.info("--- 4. JSON 저장 ---")
    json_path = save_embedding_json(
        embeddings, filename="samsung_sample_embeddings.json",
    )
    if json_path:
        logger.info("JSON 저장 완료: %s", json_path)

    # 5. DB 저장
    logger.info("--- 5. DB 저장 ---")
    inserted = save_embedding_to_db(embeddings)
    logger.info("DB INSERT: %d건", inserted)

    # 6. 검증
    logger.info("--- 6. 검증 ---")
    ok = verify_db(logger)

    logger.info(
        "=== 요약  chunks=%d  embeddings=%d  DB=%d  검증=%s ===",
        len(chunks), len(embeddings), inserted, "OK" if ok else "FAIL",
    )

    if not ok:
        logger.error("document_embeddings 테이블에 데이터 없음")
        return 1

    logger.info("=== Embedding 샘플 검증 완료 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
