"""document_embeddings 상태 점검 및 품질 검증 스크립트."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
sys.path.insert(0, str(DB_MODULE))

from connection import get_connection  # noqa: E402

logger = logging.getLogger(__name__)

EXPECTED_DIM = 1536


def load_embeddings() -> list[dict]:
    """document_embeddings + document_chunks 전체 조회."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    de.id AS emb_id,
                    de.chunk_id,
                    de.embedding_model,
                    de.embedding_dimension,
                    de.embedding_vector,
                    dc.chunk_text,
                    dc.chunk_length,
                    dc.ticker,
                    dc.document_type
                FROM document_embeddings de
                JOIN document_chunks dc ON de.chunk_id = dc.id
                ORDER BY de.chunk_id
            """)
            return cur.fetchall()
    finally:
        conn.close()


def parse_embedding_vector(vector_raw) -> list[float] | None:
    """embedding_vector 필드를 float 리스트로 파싱한다."""
    if isinstance(vector_raw, list):
        return vector_raw
    if isinstance(vector_raw, str):
        try:
            parsed = json.loads(vector_raw)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
    return None


def is_dummy_vector(vec: list[float]) -> bool:
    """더미(시퀀스/상수) 벡터인지 판별한다.

    판별 기준:
    - 모든 값이 동일
    - 0.001 단위 순차 증가 (TASK-008 더미 패턴)
    - 모든 값이 0
    """
    if not vec:
        return True

    if len(set(vec)) <= 2:
        return True

    expected_seq = [round(0.001 * i, 4) for i in range(min(10, len(vec)))]
    actual_head = [round(v, 4) for v in vec[:min(10, len(vec))]]
    if actual_head == expected_seq:
        return True

    return False


def inspect_embedding_rows() -> dict:
    """모든 Embedding 행을 점검하고 결과를 반환한다."""
    rows = load_embeddings()
    logger.info("document_embeddings 총 행: %d", len(rows))

    results = {
        "total": len(rows),
        "valid": [],
        "invalid": [],
        "dummy": [],
        "parse_fail": [],
        "dim_mismatch": [],
    }

    for row in rows:
        chunk_id = row["chunk_id"]
        model = row["embedding_model"]
        dim_stored = row["embedding_dimension"]
        vec_raw = row["embedding_vector"]

        vec = parse_embedding_vector(vec_raw)

        if vec is None:
            logger.warning("  chunk_id=%d  파싱 실패", chunk_id)
            results["parse_fail"].append(chunk_id)
            results["invalid"].append(chunk_id)
            continue

        if len(vec) != dim_stored:
            logger.warning(
                "  chunk_id=%d  dim 불일치  stored=%d  actual=%d",
                chunk_id, dim_stored, len(vec),
            )
            results["dim_mismatch"].append(chunk_id)
            results["invalid"].append(chunk_id)
            continue

        if len(vec) != EXPECTED_DIM:
            logger.warning(
                "  chunk_id=%d  dim 비정상  expected=%d  actual=%d",
                chunk_id, EXPECTED_DIM, len(vec),
            )
            results["invalid"].append(chunk_id)
            continue

        if is_dummy_vector(vec):
            logger.warning("  chunk_id=%d  더미 벡터 감지", chunk_id)
            results["dummy"].append(chunk_id)
            results["invalid"].append(chunk_id)
            continue

        results["valid"].append(chunk_id)
        logger.info(
            "  chunk_id=%d  model=%s  dim=%d  OK",
            chunk_id, model, len(vec),
        )

    return results


def detect_missing_embeddings() -> list[int]:
    """document_chunks에 존재하지만 document_embeddings에 없는 chunk_id."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT dc.id AS chunk_id
                FROM document_chunks dc
                LEFT JOIN document_embeddings de ON dc.id = de.chunk_id
                WHERE de.id IS NULL
                ORDER BY dc.id
            """)
            return [r["chunk_id"] for r in cur.fetchall()]
    finally:
        conn.close()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

    logger.info("=== Embedding 품질 점검 시작 ===")

    results = inspect_embedding_rows()

    logger.info("--- 점검 결과 요약 ---")
    logger.info("  총 행: %d", results["total"])
    logger.info("  정상: %d", len(results["valid"]))
    logger.info("  비정상: %d", len(results["invalid"]))
    logger.info("    - 더미 벡터: %d  chunk_ids=%s", len(results["dummy"]), results["dummy"])
    logger.info("    - 파싱 실패: %d  chunk_ids=%s", len(results["parse_fail"]), results["parse_fail"])
    logger.info("    - dim 불일치: %d  chunk_ids=%s", len(results["dim_mismatch"]), results["dim_mismatch"])

    missing = detect_missing_embeddings()
    logger.info("  Embedding 미존재 chunk: %d  chunk_ids=%s", len(missing), missing)

    all_problem_ids = list(set(results["invalid"] + missing))
    logger.info("재생성 필요 chunk_ids: %s", sorted(all_problem_ids))

    logger.info("=== Embedding 품질 점검 완료 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
