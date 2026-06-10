"""Canonical market events API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class EventEvidenceItem(BaseModel):
    evidence_id: int | None = None
    event_id: str | None = None
    source_type: str = "CHUNK"
    source_id: str | None = None
    title: str | None = None
    url: str | None = None
    published_at: str | None = None
    relevance_score: float | None = None


class CanonicalEventItem(BaseModel):
    event_id: str
    trace_id: str | None = None
    ticker: str = ""
    company_name: str | None = None
    canonical_title: str
    event_summary: str | None = None
    event_type: str = "market_news"
    event_date: str | None = None
    confidence_score: float = 0.0
    importance_score: float = 0.0
    impact_direction: str = "neutral"
    evidence_count: int = 0
    evidence: list[EventEvidenceItem] = Field(default_factory=list)


class EventsTraceResponse(BaseModel):
    trace_id: str
    ticker: str = ""
    query: str = ""
    event_count: int = 0
    events: list[CanonicalEventItem] = Field(default_factory=list)
    memory_layers: list[dict] = Field(default_factory=list)
    dedup_stats: dict | None = None


class EventsTickerResponse(BaseModel):
    ticker: str
    event_count: int = 0
    events: list[CanonicalEventItem] = Field(default_factory=list)


class EventEvidenceResponse(BaseModel):
    event_id: str
    evidence_count: int = 0
    evidence: list[EventEvidenceItem] = Field(default_factory=list)


class MemoryEventsResponse(BaseModel):
    trace_id: str
    ticker: str = ""
    event_count: int = 0
    events: list[CanonicalEventItem] = Field(default_factory=list)
    memory_layers: list[dict] = Field(default_factory=list)
