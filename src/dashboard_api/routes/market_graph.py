"""Market Relationship Graph API."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.market_graph_schema import (
    MarketGraphResponse,
    MarketInsightResponse,
    RelationExplanationResponse,
    RiskExposureResponse,
    RuntimeStatusResponse,
)
from ..services.market_graph_service import (
    build_market_graph_by_trace,
    fetch_market_insight,
    fetch_relation_explanation,
    fetch_risk_exposure,
    fetch_runtime_status,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["market-graph"])


@router.get("/market-graph/{trace_id}", response_model=MarketGraphResponse)
def get_market_graph(trace_id: str) -> MarketGraphResponse:
    data = build_market_graph_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info(
        "GET /api/market-graph/%s  nodes=%d  edges=%d",
        trace_id,
        len(data.get("nodes", [])),
        len(data.get("edges", [])),
    )
    return MarketGraphResponse(**data)


@router.get("/runtime-status/{trace_id}", response_model=RuntimeStatusResponse)
def get_runtime_status(trace_id: str) -> RuntimeStatusResponse:
    data = fetch_runtime_status(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/runtime-status/%s  phase=%s", trace_id, data.get("phase"))
    return RuntimeStatusResponse(**data)


@router.get("/relation-explanation/{trace_id}", response_model=RelationExplanationResponse)
def get_relation_explanation(trace_id: str) -> RelationExplanationResponse:
    data = fetch_relation_explanation(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info(
        "GET /api/relation-explanation/%s  relations=%d",
        trace_id,
        len(data.get("relations", [])),
    )
    return RelationExplanationResponse(**data)


@router.get("/risk-exposure/{trace_id}", response_model=RiskExposureResponse)
def get_risk_exposure(trace_id: str) -> RiskExposureResponse:
    data = fetch_risk_exposure(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/risk-exposure/%s  risks=%d", trace_id, len(data.get("risks", [])))
    return RiskExposureResponse(**data)


@router.get("/market-insight/{trace_id}", response_model=MarketInsightResponse)
def get_market_insight(trace_id: str) -> MarketInsightResponse:
    data = fetch_market_insight(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/market-insight/%s", trace_id)
    return MarketInsightResponse(**data)
