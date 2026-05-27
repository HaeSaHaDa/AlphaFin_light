"""Signal Evaluation API Schema."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CurrentSignal(BaseModel):
    signal: str = "neutral"
    display_label: str = "중립"
    confidence: float = 0.5
    reason: list[str] = Field(default_factory=list)


class MarketComparison(BaseModel):
    price_change_pct: float = 0.0
    period_label: str = ""
    direction_correct: bool = False
    actual_direction: str = ""


class SignalMetrics(BaseModel):
    direction_accuracy: float = 0.0
    hit_ratio_pct: float = 0.0
    total_signals: int = 0
    correct_count: int = 0


class SignalResponse(BaseModel):
    trace_id: str = ""
    query: str = ""
    ticker: str = ""
    current_signal: CurrentSignal = Field(default_factory=CurrentSignal)
    market_comparison: MarketComparison = Field(default_factory=MarketComparison)
    confidence_evaluation: dict[str, Any] = Field(default_factory=dict)
    metrics: SignalMetrics = Field(default_factory=SignalMetrics)
    timeline: list[dict[str, Any]] = Field(default_factory=list)
    history: list[dict[str, Any]] = Field(default_factory=list)
    confidence_summary: dict[str, Any] = Field(default_factory=dict)
    summary_text: str = ""
