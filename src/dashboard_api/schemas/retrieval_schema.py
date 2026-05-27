"""Retrieval API Response Schema."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RetrievalResponse(BaseModel):
    trace_id: str = ""
    query: str = ""
    ticker: str = ""
    chunk_count: int = 0
    chunks: list[dict[str, Any]] = Field(default_factory=list)
    retrieval_quality: dict[str, Any] = Field(default_factory=dict)
    context_usage: dict[str, Any] = Field(default_factory=dict)
    unified_context_length: int = 0
    retrieval_timestamp: str = ""
    analysis: dict[str, Any] = Field(default_factory=dict)
    context_layers: dict[str, Any] = Field(default_factory=dict)
