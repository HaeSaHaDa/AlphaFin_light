"""Engine Run API Route — POST /api/engine/run."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.runtime_flow.runtime_query_runner import run_runtime_query

from ..schemas.company_schema import CompanyResolveResponse, DisclosurePreview, TickerStats
from ..schemas.engine_schema import EngineRunResponse, IngestionRunSummary
from ..services.company_service import resolve_company_query

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/engine", tags=["engine"])


class EngineRunRequest(BaseModel):
    query: str
    persona: str = "growth_investor"
    ticker: str | None = None
    skip_ingestion: bool = False


@router.post("/run", response_model=EngineRunResponse)
def run_engine(req: EngineRunRequest) -> EngineRunResponse:
    """Runtime Query: Resolver → Ingestion → Retrieval → Engine → Trace."""
    logger.info("POST /api/engine/run  query=%s", req.query)

    rt = run_runtime_query(
        req.query,
        persona=req.persona,
        skip_ingestion=req.skip_ingestion,
    )
    if rt.get("status") == "failed":
        raise HTTPException(status_code=400, detail=rt.get("error", "실행 실패"))

    trace_id = rt.get("trace_id", "")
    if not trace_id:
        raise HTTPException(status_code=500, detail="trace_id 생성 실패")

    company_resp: CompanyResolveResponse | None = None
    resolve_data = resolve_company_query(req.query, prefetch=False)
    if resolve_data:
        if rt.get("stats"):
            resolve_data["stats"] = rt["stats"]
        company_resp = CompanyResolveResponse(**resolve_data)

    ing = rt.get("ingestion") or {}
    ingestion_summary = IngestionRunSummary(
        status=ing.get("status", ""),
        documents=int(ing.get("documents", 0)),
        chunks=int(ing.get("chunks", 0)),
        embeddings=int(ing.get("embeddings", 0)),
        embeddings_created=int(ing.get("embeddings_created", 0)),
        embeddings_skipped=int(ing.get("embeddings_skipped", 0)),
        skipped_collectors=ing.get("skipped_collectors", []),
    )

    for line in rt.get("runtime_logs", []):
        logger.info("runtime  %s", line)

    return EngineRunResponse(
        trace_id=trace_id,
        status=rt.get("status", "completed"),
        query=req.query,
        ticker=rt.get("ticker", ""),
        company=company_resp,
        ingestion=ingestion_summary,
    )
