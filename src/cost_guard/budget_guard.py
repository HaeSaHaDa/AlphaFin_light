"""Daily Budget Guard."""
from __future__ import annotations

import logging

from .cost_estimator import estimate_usage_cost
from .token_usage_logger import get_today_usage

logger = logging.getLogger(__name__)

MAX_DAILY_COST_USD = 5.0


def get_today_cost_usd() -> float:
    data = get_today_usage()
    return estimate_usage_cost(data.get("totals", {}))


def check_budget(estimated_add_usd: float = 0.0) -> tuple[bool, float, float]:
    """(allowed, current_cost, limit) 반환."""
    current = get_today_cost_usd()
    projected = current + estimated_add_usd
    allowed = projected <= MAX_DAILY_COST_USD
    if not allowed:
        logger.warning(
            "budget exceeded  current=%.4f  projected=%.4f  limit=%.2f",
            current, projected, MAX_DAILY_COST_USD,
        )
    return allowed, current, MAX_DAILY_COST_USD


def require_budget(estimated_add_usd: float = 0.0) -> None:
    allowed, current, limit = check_budget(estimated_add_usd)
    if not allowed:
        raise RuntimeError(
            f"일일 예산 초과: ${current:.4f} + ${estimated_add_usd:.4f} > ${limit:.2f}"
        )
