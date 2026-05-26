"""OpenAI Embedding API 기반 벡터 생성 모듈."""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "text-embedding-3-small"
REQUEST_DELAY_SEC = 0.5


def _load_api_key() -> str:
    env_path = Path(__file__).resolve().parents[3] / ".env"
    load_dotenv(env_path)
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise ValueError("OPENAI_API_KEY가 .env에 설정되지 않았습니다.")
    return key


_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=_load_api_key())
        logger.info("OpenAI 클라이언트 초기화 완료")
    return _client


def generate_embedding(
    text: str,
    model: str = DEFAULT_MODEL,
) -> list[float]:
    """단일 텍스트에 대한 Embedding 벡터를 생성한다.

    Args:
        text: 입력 텍스트.
        model: Embedding 모델명.

    Returns:
        float 리스트 (벡터).
    """
    if not text or not text.strip():
        logger.warning("빈 텍스트 — Embedding 생성 건너뜀")
        return []

    client = _get_client()
    try:
        resp = client.embeddings.create(input=text, model=model)
        vector = resp.data[0].embedding
        logger.debug(
            "Embedding 생성  model=%s  dim=%d  text_len=%d",
            model, len(vector), len(text),
        )
        return vector
    except Exception:
        logger.exception("Embedding 생성 실패  model=%s", model)
        return []


def generate_embeddings(
    chunks: list[dict],
    model: str = DEFAULT_MODEL,
) -> list[dict]:
    """여러 Chunk에 대한 Embedding을 생성한다.

    Args:
        chunks: [{"chunk_id", "chunk_text", ...}, ...]
        model: Embedding 모델명.

    Returns:
        [{"chunk_id", "embedding_model", "embedding_dimension",
          "embedding_vector"}, ...]
    """
    logger.info(
        "generate_embeddings  chunks=%d  model=%s", len(chunks), model,
    )
    results: list[dict] = []

    for i, chunk in enumerate(chunks):
        text = chunk.get("chunk_text", "")
        vector = generate_embedding(text, model)

        if not vector:
            logger.warning(
                "Embedding 실패/빈 벡터  chunk_id=%s  index=%d",
                chunk.get("chunk_id"), i,
            )
            continue

        results.append({
            "chunk_id": chunk["chunk_id"],
            "embedding_model": model,
            "embedding_dimension": len(vector),
            "embedding_vector": vector,
        })

        if i < len(chunks) - 1:
            time.sleep(REQUEST_DELAY_SEC)

    logger.info(
        "Embedding 생성 완료  성공=%d / %d", len(results), len(chunks),
    )
    return results
