"""Stock Chain API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.stock_chain_schema import StockChainResponse
from ..services.stock_chain_service import (
    fetch_latest_stock_chain,
    fetch_stock_chain_by_trace,
    fetch_stock_chain_by_ticker,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/stock-chain", tags=["stock-chain"])


@router.get("/latest")
def get_latest_stock_chain_disabled() -> None:
    from .latest_guard import reject_latest_usage

    reject_latest_usage()


@router.get("/ticker/{ticker}")
def get_stock_chain_by_ticker(ticker: str) -> dict:
    data = fetch_stock_chain_by_ticker(ticker)
    if not data:
        raise HTTPException(status_code=404, detail=f"ticker={ticker} 없음")
    logger.info("GET /api/stock-chain/ticker/%s", ticker)
    return data


@router.get("/{trace_id}", response_model=StockChainResponse)
def get_stock_chain_by_trace(trace_id: str) -> StockChainResponse:
    data = fetch_stock_chain_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/stock-chain/%s", trace_id)
    return StockChainResponse(**data)
