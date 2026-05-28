"""Market Graph API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class MarketGraphNode(BaseModel):
    id: str
    label: str
    category: str
    ticker: str | None = None
    is_center: bool = False
    relevance: float = 0.5
    description: str = ""


class MarketGraphEdge(BaseModel):
    id: str
    source: str
    target: str
    edge_type: str
    direction: str = "outbound"
    confidence: float = 0.5
    relevance: float = 0.5
    impact: str = "neutral"
    reason: str = ""
    evidence: list[str] = Field(default_factory=list)


class MarketGraphResponse(BaseModel):
    trace_id: str = ""
    query: str = ""
    center_ticker: str = ""
    center_company: str = ""
    nodes: list[MarketGraphNode] = Field(default_factory=list)
    edges: list[MarketGraphEdge] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)


class RuntimeStatusResponse(BaseModel):
    trace_id: str = ""
    ticker: str = ""
    company_name: str = ""
    query: str = ""
    phase: str = "idle"
    label: str = "Idle"
    step_count: int = 0
    last_step: str = ""


class RelationExplanation(BaseModel):
    source: str
    target: str
    relation: str
    direction: str
    confidence: float
    impact: str
    explanation: str
    evidence: list[str] = Field(default_factory=list)


class RelationExplanationResponse(BaseModel):
    trace_id: str = ""
    center_ticker: str = ""
    center_company: str = ""
    relations: list[RelationExplanation] = Field(default_factory=list)


class RiskExposureItem(BaseModel):
    risk: str
    exposure_level: str
    confidence: float
    impact: str
    evidence: list[str] = Field(default_factory=list)


class RiskExposureResponse(BaseModel):
    trace_id: str = ""
    center_ticker: str = ""
    center_company: str = ""
    risks: list[RiskExposureItem] = Field(default_factory=list)


class MarketInsightResponse(BaseModel):
    trace_id: str = ""
    center_ticker: str = ""
    center_company: str = ""
    market_story: str = ""
    bullish: list[str] = Field(default_factory=list)
    bearish: list[str] = Field(default_factory=list)
    key_relations: list[RelationExplanation] = Field(default_factory=list)
