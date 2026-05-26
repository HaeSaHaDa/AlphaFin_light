"""고정 길이 기반 문서 Chunking 모듈."""
from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 800
DEFAULT_OVERLAP = 100
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?。\n])\s*")


def split_text_into_chunks(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[str]:
    """긴 텍스트를 고정 길이 기준으로 Chunk 리스트로 분할한다.

    문장 경계를 최대한 유지하면서 chunk_size 이내로 분할한다.

    Args:
        text: 원본 텍스트.
        chunk_size: Chunk 최대 문자 수 (500~1000 권장).
        overlap: Chunk 간 겹침 문자 수.

    Returns:
        Chunk 문자열 리스트.
    """
    if not text or not text.strip():
        return []

    text = text.strip()

    if len(text) <= chunk_size:
        return [text]

    sentences = SENTENCE_SPLIT_RE.split(text)
    sentences = [s for s in sentences if s.strip()]

    chunks: list[str] = []
    current = ""

    for sent in sentences:
        if len(current) + len(sent) + 1 <= chunk_size:
            current = f"{current} {sent}".strip() if current else sent
        else:
            if current:
                chunks.append(current)
            if len(sent) > chunk_size:
                for sub in _hard_split(sent, chunk_size):
                    chunks.append(sub)
                current = ""
            else:
                if overlap > 0 and current:
                    tail = current[-overlap:] if len(current) > overlap else current
                    current = f"{tail} {sent}".strip()
                else:
                    current = sent

    if current:
        chunks.append(current)

    logger.info(
        "split_text_into_chunks  text_len=%d  chunks=%d  chunk_size=%d",
        len(text), len(chunks), chunk_size,
    )
    return chunks


def _hard_split(text: str, chunk_size: int) -> list[str]:
    """문장 경계를 찾을 수 없을 때 강제 분할한다."""
    parts: list[str] = []
    for i in range(0, len(text), chunk_size):
        parts.append(text[i:i + chunk_size])
    return parts


def create_document_chunks(
    document: dict,
    document_type: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[dict]:
    """문서 dict에서 Chunk 리스트를 생성한다.

    Args:
        document: 문서 dict (content/body 필드 포함).
        document_type: 문서 유형 ("news_article" 또는 "disclosure").
        chunk_size: Chunk 최대 문자 수.
        overlap: Chunk 간 겹침 문자 수.

    Returns:
        [{"chunk_index", "chunk_text", "chunk_length"}, ...]
    """
    text = document.get("content") or document.get("body") or ""

    if document_type == "news_article" and document.get("title"):
        text = f"{document['title']}\n\n{text}"

    chunks_text = split_text_into_chunks(text, chunk_size, overlap)

    result: list[dict] = []
    for idx, chunk in enumerate(chunks_text):
        result.append({
            "chunk_index": idx,
            "chunk_text": chunk,
            "chunk_length": len(chunk),
        })

    return result
