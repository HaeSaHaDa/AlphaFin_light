"""Company API Schema."""
from __future__ import annotations

from pydantic import BaseModel


class CompanySearchItem(BaseModel):
    company_name: str
    ticker: str
    corp_code: str = ""
    market: str = ""
    sector: str = ""
    industry: str = ""


class TickerStats(BaseModel):
    news_count: int = 0
    disclosure_count: int = 0
    price_count: int = 0
    chunk_count: int = 0
    embedding_count: int = 0
    pending_embedding_count: int = 0


class DisclosurePreview(BaseModel):
    report_name: str = ""
    receipt_date: str = ""
    receipt_no: str = ""
    disclosure_type: str = ""


class CompanyResolveResponse(BaseModel):
    company_name: str
    ticker: str
    corp_code: str = ""
    market: str = ""
    stats: TickerStats
    recent_disclosures: list[DisclosurePreview] = []
    cache_ready: bool = False


class SearchIngestRequest(BaseModel):
    query: str
    run_engine: bool = True
    force: bool = False


class SearchIngestResponse(BaseModel):
    status: str
    query: str = ""
    company: CompanyResolveResponse | None = None
    ingestion: dict | None = None
    trace_id: str = ""
    engine_status: str = ""
    error: str | None = None
