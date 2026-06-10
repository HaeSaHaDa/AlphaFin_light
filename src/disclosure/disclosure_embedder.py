"""Disclosure embeddings."""
from __future__ import annotations

from src.rag.embedding.embedder import generate_embeddings

from .disclosure_repository import (
    insert_disclosure_embeddings,
    list_disclosure_chunks_without_embedding,
)


def embed_disclosure_chunks(ticker: str, model: str = "text-embedding-3-small") -> dict:
    chunks = list_disclosure_chunks_without_embedding(ticker, model, limit=250)
    to_embed = [{"chunk_id": c["chunk_id"], "chunk_text": c["chunk_text"]} for c in chunks]
    vectors = generate_embeddings(to_embed, model=model)
    inserted = insert_disclosure_embeddings(vectors)
    return {
        "status": "completed",
        "ticker": ticker,
        "requested": len(to_embed),
        "embedded": len(vectors),
        "inserted": inserted,
        "model": model,
    }
