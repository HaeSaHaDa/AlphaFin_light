"""Reflection API Response Schema."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ReflectionResponse(BaseModel):
    trace_id: str = ""
    query: str = ""
    persona: str = ""
    reflection_summary: str = ""
    missing_risks: list[str] = Field(default_factory=list)
    overconfidence_detected: bool = False
    overconfidence_reasons: list[str] = Field(default_factory=list)
    context_gaps: list[str] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)
    timestamp: str = ""
