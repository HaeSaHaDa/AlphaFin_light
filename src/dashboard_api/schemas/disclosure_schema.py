"""Disclosure API schemas."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class DisclosureCollectRequest(BaseModel):
    ticker: str
    force: bool = False
    days: int = 365
    body_limit: int = Field(10, ge=0, le=100)


class DisclosureDocumentItem(BaseModel):
    document_id: int
    ticker: str
    corp_code: str | None = None
    company_name: str | None = None
    report_name: str
    report_type: str
    report_date: str | None = None
    source_type: str
    document_url: str | None = None
    summary: str | None = None
    receipt_no: str | None = None


class DisclosureListResponse(BaseModel):
    ticker: str
    document_count: int = 0
    documents: list[DisclosureDocumentItem] = Field(default_factory=list)


class DisclosureSearchResponse(BaseModel):
    ticker: str
    query: str
    top_k: int
    chunks: list[dict[str, Any]] = Field(default_factory=list)


class DisclosureTimelineResponse(BaseModel):
    ticker: str
    timeline: list[dict[str, Any]] = Field(default_factory=list)


class DisclosureEvidenceResponse(BaseModel):
    trace_id: str
    ticker: str
    query: str
    evidence: list[dict[str, Any]] = Field(default_factory=list)
