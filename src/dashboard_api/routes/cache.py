"""Cache status API."""
from __future__ import annotations

import logging

from fastapi import APIRouter

from src.cost_guard.ingestion_cache_manager import get_cache_status
from src.cost_guard.presentation_mode import is_presentation_mode

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/cache", tags=["cache"])


@router.get("/status")
def get_cache_status_api() -> dict:
    status = get_cache_status()
    status["presentation_mode"] = is_presentation_mode()
    return status
