"""Cost Guard API."""
from __future__ import annotations

import logging

from fastapi import APIRouter

from src.cost_guard.budget_guard import MAX_DAILY_COST_USD, get_today_cost_usd
from src.cost_guard.cost_estimator import estimate_usage_cost
from src.cost_guard.token_usage_logger import get_today_usage

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/cost", tags=["cost"])


@router.get("/today")
def get_cost_today() -> dict:
    usage = get_today_usage()
    totals = usage.get("totals", {})
    cost = estimate_usage_cost(totals)
    return {
        "date": usage.get("date"),
        "totals": totals,
        "estimated_cost_usd": cost,
        "limit_usd": MAX_DAILY_COST_USD,
        "remaining_usd": round(max(0.0, MAX_DAILY_COST_USD - cost), 6),
    }
