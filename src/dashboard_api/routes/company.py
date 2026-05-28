"""Company Search API."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Query

from ..schemas.company_schema import (
    CompanyResolveResponse,
    CompanySearchItem,
    SearchIngestRequest,
    SearchIngestResponse,
)
from ..schemas.engine_schema import IngestionRunSummary
from ..services.company_service import get_company_by_ticker, resolve_company_query, search_company
from ..services.search_service import search_and_ingest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/company", tags=["company"])


@router.get("/search", response_model=list[CompanySearchItem])
def get_company_search(q: str = Query("", min_length=1)) -> list[CompanySearchItem]:
    items = search_company(q)
    logger.info("GET /api/company/search  q=%s  hits=%d", q, len(items))
    return [CompanySearchItem(**item) for item in items]


@router.get("/resolve", response_model=CompanyResolveResponse)
def get_company_resolve(
    q: str = Query(..., min_length=1),
    prefetch: bool = Query(False, description="공시가 없으면 DART 수집 시도"),
) -> CompanyResolveResponse:
    data = resolve_company_query(q, prefetch=prefetch)
    if not data:
        raise HTTPException(status_code=404, detail="회사를 식별할 수 없습니다")
    logger.info(
        "GET /api/company/resolve  ticker=%s  disclosures=%d",
        data["ticker"], data["stats"]["disclosure_count"],
    )
    return CompanyResolveResponse(**data)


@router.post("/search-ingest", response_model=SearchIngestResponse)
def post_search_ingest(req: SearchIngestRequest) -> SearchIngestResponse:
    """검색어 → 종목 식별 → 뉴스·공시·embedding 수집 → (선택) AI 분석."""
    logger.info("POST /api/company/search-ingest  query=%s", req.query)
    result = search_and_ingest(
        req.query,
        run_engine=req.run_engine,
        force=req.force,
    )
    if result.get("status") == "failed":
        raise HTTPException(status_code=400, detail=result.get("error", "검색 실패"))

    company = result.get("company")
    ingestion_raw = result.get("ingestion")
    ingestion = (
        IngestionRunSummary(**ingestion_raw) if ingestion_raw else None
    )

    return SearchIngestResponse(
        status=result.get("engine_status") or result.get("status", ""),
        query=result.get("query", req.query),
        company=CompanyResolveResponse(**company) if company else None,
        ingestion=ingestion.model_dump() if ingestion else None,
        trace_id=result.get("trace_id", ""),
        engine_status=result.get("engine_status", ""),
        error=result.get("error"),
    )


@router.get("/{ticker}", response_model=CompanySearchItem)
def get_company_by_ticker_api(ticker: str) -> CompanySearchItem:
    row = get_company_by_ticker(ticker)
    if not row:
        raise HTTPException(status_code=404, detail=f"ticker={ticker} 없음")
    return CompanySearchItem(**row)
