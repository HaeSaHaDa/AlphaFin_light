"""Memory API Response Schema."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MemoryResponse(BaseModel):
    trace_id: str = ""
    query: str = ""
    ticker: str = ""
    memory_updates: dict[str, Any] = Field(default_factory=dict)
    temporal_result: dict[str, Any] = Field(default_factory=dict)
    layered_memory: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)
    layer_counts: dict[str, int] = Field(default_factory=dict)


class MemoryLayerResponse(BaseModel):
    layer: str = ""
    memory_count: int = 0
    memories: list[dict[str, Any]] = Field(default_factory=list)
