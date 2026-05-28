"""Engine API Schema."""
from __future__ import annotations

from pydantic import BaseModel, Field

from .company_schema import CompanyResolveResponse, DisclosurePreview, TickerStats


class IngestionRunSummary(BaseModel):
    status: str
    documents: int = 0
    chunks: int = 0
    embeddings: int = 0
    embeddings_created: int = 0
    embeddings_skipped: int = 0
    skipped_collectors: list[str] = Field(default_factory=list)


class EngineRunResponse(BaseModel):
    trace_id: str
    status: str = "completed"
    query: str = ""
    ticker: str = ""
    company: CompanyResolveResponse | None = None
    ingestion: IngestionRunSummary | None = None
    recent_disclosures: list[DisclosurePreview] = Field(default_factory=list)
