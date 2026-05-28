"""Runtime API — trace_id 기반 Dashboard 번들."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.runtime_flow.dashboard_response_builder import build_dashboard_bundle
from src.runtime_flow.runtime_query_runner import run_runtime_query
from src.runtime_flow.trace_manager import trace_exists

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/runtime", tags=["runtime"])


class RuntimeRunRequest(BaseModel):
    query: str
    persona: str = "growth_investor"
    skip_ingestion: bool = False


@router.post("/run")
def post_runtime_run(req: RuntimeRunRequest) -> dict:
    logger.info("POST /api/runtime/run  query=%s", req.query)
    result = run_runtime_query(
        req.query,
        persona=req.persona,
        skip_ingestion=req.skip_ingestion,
    )
    if result.get("status") == "failed":
        raise HTTPException(status_code=400, detail=result.get("error", "실패"))
    return result


@router.get("/dashboard/{trace_id}")
def get_runtime_dashboard(trace_id: str) -> dict:
    if not trace_exists(trace_id):
        raise HTTPException(
            status_code=404,
            detail=f"trace_id={trace_id} 없음 — sample/latest fallback 없음",
        )
    bundle = build_dashboard_bundle(trace_id)
    if not bundle:
        raise HTTPException(status_code=404, detail="Dashboard 데이터 없음")
    logger.info("GET /api/runtime/dashboard/%s  ticker=%s", trace_id, bundle.get("ticker"))
    return bundle


@router.get("/context")
def get_runtime_context(trace_id: str = Query("", description="현재 trace_id")) -> dict:
    """Persistent shell용 최소 runtime context."""
    tid = trace_id.strip()
    if not tid:
        return {
            "trace_id": "",
            "ticker": "",
            "company_name": "",
            "status": "idle",
        }
    from ..services.market_graph_service import fetch_runtime_status  # noqa: PLC0415

    status = fetch_runtime_status(tid)
    if not status:
        raise HTTPException(status_code=404, detail=f"trace_id={tid} 없음")
    return {
        "trace_id": tid,
        "ticker": status.get("ticker", ""),
        "company_name": status.get("company_name", ""),
        "status": status.get("phase", "runtime_active"),
        "label": status.get("label", "Runtime Active"),
    }
