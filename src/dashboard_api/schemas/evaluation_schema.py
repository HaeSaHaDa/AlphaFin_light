"""Evaluation API Response Schema."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EvaluationResponse(BaseModel):
    trace_id: str = ""
    query: str = ""
    retrieval_score: float | None = None
    reasoning_score: float | None = None
    reflection_score: float | None = None
    memory_score: float | None = None
    stock_chain_score: float | None = None
    overall_score: float | None = None
    consistency: dict[str, Any] = Field(default_factory=dict)
    hallucination_risk: dict[str, Any] = Field(default_factory=dict)
    evaluated_at: str = ""
