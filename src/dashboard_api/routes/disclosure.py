"""Disclosure API routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Query

from ..schemas.disclosure_schema import (
    DisclosureCollectRequest,
    DisclosureEvidenceResponse,
    DisclosureListResponse,
    DisclosureSearchResponse,
    DisclosureTimelineResponse,
)
from ..services.disclosure_service import (
    collect_disclosure_store,
    fetch_disclosure_evidence,
    fetch_disclosure_timeline,
    fetch_disclosures,
    search_disclosures,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/disclosure", tags=["disclosure"])


@router.post("/collect")
def post_collect(req: DisclosureCollectRequest) -> dict:
    out = collect_disclosure_store(
        req.ticker,
        force=req.force,
        days=req.days,
        body_limit=req.body_limit,
    )
    logger.info("POST /api/disclosure/collect  ticker=%s  status=%s", req.ticker, out.get("status"))
    return out


@router.get("/search", response_model=DisclosureSearchResponse)
def get_search(
    ticker: str = Query(..., min_length=6),
    q: str = Query(..., min_length=1),
    top_k: int = Query(8, ge=1, le=30),
) -> DisclosureSearchResponse:
    return DisclosureSearchResponse(**search_disclosures(ticker, q, top_k=top_k))


@router.get("/timeline/{ticker}", response_model=DisclosureTimelineResponse)
def get_timeline(ticker: str) -> DisclosureTimelineResponse:
    return DisclosureTimelineResponse(**fetch_disclosure_timeline(ticker))


@router.get("/evidence/{trace_id}", response_model=DisclosureEvidenceResponse)
def get_evidence(trace_id: str) -> DisclosureEvidenceResponse:
    data = fetch_disclosure_evidence(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    return DisclosureEvidenceResponse(**data)


@router.get("/{ticker}", response_model=DisclosureListResponse)
def get_disclosure_by_ticker(ticker: str) -> DisclosureListResponse:
    data = fetch_disclosures(ticker)
    if data.get("document_count", 0) <= 0:
        raise HTTPException(status_code=404, detail=f"ticker={ticker} 공시 없음")
    return DisclosureListResponse(**data)
