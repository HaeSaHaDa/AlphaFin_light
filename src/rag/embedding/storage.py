"""Embedding 저장 모듈 (JSON + DB)."""
from __future__ import annotations

import json
import logging
from pathlib import Path

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_MODULE = PROJECT_ROOT / "src" / "common" / "db"
sys.path.insert(0, str(DB_MODULE))

import pymysql  # noqa: E402
from connection import get_connection  # noqa: E402

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "embeddings"


def save_embedding_json(
    data: list[dict],
    output_dir: Path | str | None = None,
    filename: str = "embeddings.json",
) -> Path | None:
    """Embedding 결과를 JSON으로 저장한다.

    벡터를 그대로 저장하면 파일이 매우 커지므로,
    벡터의 처음 5개 값과 차원만 저장한다.

    Args:
        data: Embedding 결과 dict 목록.
        output_dir: 저장 디렉토리.
        filename: 저장 파일명.

    Returns:
        저장된 파일 경로. 빈 데이터면 None.
    """
    if not data:
        logger.warning("저장 생략 (Embedding 데이터 없음)")
        return None

    out = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    compact: list[dict] = []
    for item in data:
        vec = item.get("embedding_vector", [])
        compact.append({
            "chunk_id": item["chunk_id"],
            "embedding_model": item["embedding_model"],
            "embedding_dimension": item["embedding_dimension"],
            "vector_preview": vec[:5] if vec else [],
        })

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(compact, f, ensure_ascii=False, indent=2)

    logger.info("Embedding JSON 저장  %s  (%d건)", filepath, len(compact))
    return filepath


def save_embedding_to_db(
    data: list[dict],
    conn: pymysql.Connection | None = None,
) -> int:
    """document_embeddings 테이블에 Embedding을 저장한다.

    중복 (chunk_id, embedding_model)은 무시한다.

    Args:
        data: [{"chunk_id", "embedding_model",
                "embedding_dimension", "embedding_vector"}, ...]

    Returns:
        INSERT 성공 건수.
    """
    sql = """
        INSERT IGNORE INTO document_embeddings
            (chunk_id, embedding_model, embedding_dimension, embedding_vector)
        VALUES (%s, %s, %s, %s)
    """
    own_conn = conn is None
    if own_conn:
        conn = get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            for item in data:
                vec = item["embedding_vector"]
                vec_json = json.dumps(vec) if isinstance(vec, list) else vec
                cur.execute(sql, (
                    item["chunk_id"],
                    item["embedding_model"],
                    item["embedding_dimension"],
                    vec_json,
                ))
                inserted += cur.rowcount
        if own_conn:
            conn.commit()
        logger.info("document_embeddings INSERT  총 %d / %d건", inserted, len(data))
        return inserted
    except Exception:
        if own_conn:
            conn.rollback()
        logger.exception("document_embeddings INSERT 실패")
        return 0
    finally:
        if own_conn:
            conn.close()
