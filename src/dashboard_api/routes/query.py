"""Topic Query API — selectedTicker 기반 Runtime."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.runtime_flow.runtime_query_runner import run_runtime_query_selected

from ..schemas.company_schema import CompanyResolveResponse, TickerStats
from ..services.company_service import get_company_by_ticker, resolve_company_query

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/query", tags=["query"])


class QueryRunRequest(BaseModel):
    ticker: str
    company: str = ""
    keywords: list[str] = Field(default_factory=list)
    run_engine: bool = True


class QueryRunResponse(BaseModel):
    status: str
    trace_id: str = ""
    ticker: str = ""
    company_name: str = ""
    runtime_query: str = ""
    keywords: list[str] = Field(default_factory=list)
    runtime_logs: list[str] = Field(default_factory=list)
    disclosure_chunk_count: int = 0
    news_chunk_count: int = 0
    disclosure_collect_status: str = ""
    runtime_context: dict | None = None
    company: CompanyResolveResponse | None = None


@router.post("/run", response_model=QueryRunResponse)
def post_query_run(req: QueryRunRequest) -> QueryRunResponse:
    logger.info(
        "POST /api/query/run  ticker=%s  keywords=%s",
        req.ticker, req.keywords,
    )
    row = get_company_by_ticker(req.ticker)
    if not row:
        raise HTTPException(status_code=404, detail=f"ticker={req.ticker} 없음")

    company_name = req.company or row["company_name"]
    result = run_runtime_query_selected(
        ticker=req.ticker,
        company_name=company_name,
        keywords=req.keywords,
        corp_code=row.get("corp_code", ""),
        market=row.get("market", "KOSPI"),
        skip_ingestion=not req.run_engine,
        run_engine=req.run_engine,
    )

    if result.get("status") == "failed":
        raise HTTPException(status_code=400, detail=result.get("error", "실패"))

    resolve_data = resolve_company_query("", ticker=req.ticker)
    company_resp = None
    if resolve_data:
        company_resp = CompanyResolveResponse(
            **{**resolve_data, "stats": TickerStats(**resolve_data["stats"])},
        )

    return QueryRunResponse(
        status=result.get("status", ""),
        trace_id=result.get("trace_id", ""),
        ticker=req.ticker,
        company_name=company_name,
        runtime_query=result.get("runtime_query", ""),
        keywords=req.keywords,
        runtime_logs=result.get("runtime_logs", []),
        disclosure_chunk_count=int(result.get("disclosure_chunk_count", 0)),
        news_chunk_count=int(result.get("news_chunk_count", 0)),
        disclosure_collect_status=result.get("disclosure_collect_status", ""),
        runtime_context=result.get("runtime_context"),
        company=company_resp,
    )
