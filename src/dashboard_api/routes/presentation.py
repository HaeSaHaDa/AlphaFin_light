"""Presentation mode API."""
from __future__ import annotations

import logging

from fastapi import APIRouter

from src.cost_guard.presentation_mode import (
    disable_presentation_mode,
    enable_presentation_mode,
    is_presentation_mode,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/presentation-mode", tags=["presentation"])


@router.post("/enable")
def post_enable_presentation_mode() -> dict:
    logger.info("POST /api/presentation-mode/enable")
    state = enable_presentation_mode()
    return {"status": "ok", **state, "active": is_presentation_mode()}


@router.post("/disable")
def post_disable_presentation_mode() -> dict:
    state = disable_presentation_mode()
    return {"status": "ok", **state, "active": is_presentation_mode()}
