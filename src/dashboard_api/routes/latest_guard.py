"""Dashboard API — /latest 엔드포인트 비활성 (trace_id 필수)."""
from __future__ import annotations

from fastapi import HTTPException

LATEST_DISABLED_MSG = (
    "GET /latest 비활성화 — trace_id 기반 엔드포인트를 사용하세요. "
    "예: GET /api/retrieval/{trace_id}"
)


def reject_latest_usage() -> None:
    raise HTTPException(status_code=400, detail=LATEST_DISABLED_MSG)
