"""Stock Chain API Response Schema."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class StockChainResponse(BaseModel):
    trace_id: str = ""
    query: str = ""
    ticker: str = ""
    center_name: str = ""
    center_ticker: str = ""
    summary: dict[str, Any] = Field(default_factory=dict)
    chain: dict[str, Any] = Field(default_factory=dict)
