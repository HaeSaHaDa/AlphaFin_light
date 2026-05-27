"""Stock Chain API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.stock_chain_schema import StockChainResponse
from ..services.stock_chain_service import fetch_latest_stock_chain, fetch_stock_chain_by_ticker

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/stock-chain", tags=["stock-chain"])


@router.get("/latest", response_model=StockChainResponse)
def get_latest_stock_chain() -> StockChainResponse:
    data = fetch_latest_stock_chain()
    if not data:
        raise HTTPException(status_code=404, detail="Stock Chain 데이터 없음")
    logger.info("GET /api/stock-chain/latest  trace_id=%s", data.get("trace_id"))
    return StockChainResponse(**data)


@router.get("/ticker/{ticker}")
def get_stock_chain_by_ticker(ticker: str) -> dict:
    data = fetch_stock_chain_by_ticker(ticker)
    if not data:
        raise HTTPException(status_code=404, detail=f"ticker={ticker} 없음")
    logger.info("GET /api/stock-chain/ticker/%s", ticker)
    return data
