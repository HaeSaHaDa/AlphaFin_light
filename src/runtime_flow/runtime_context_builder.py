"""Runtime 실행 컨텍스트."""
from __future__ import annotations

from dataclasses import dataclass, field

from src.company_resolver.company_resolver import ResolvedCompany


@dataclass
class RuntimeContext:
    query: str
    persona: str = "growth_investor"
    company: ResolvedCompany | None = None
    ticker: str = ""
    ingestion: dict = field(default_factory=dict)
    retrieval_chunks: list[dict] = field(default_factory=list)
    engine_result: dict = field(default_factory=dict)
    trace_id: str = ""
    runtime_logs: list[str] = field(default_factory=list)
