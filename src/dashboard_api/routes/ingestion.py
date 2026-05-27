"""Ingestion API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.ingestion_schema import IngestionRunRequest, IngestionRunResponse
from ..services.ingestion_service import run_ingestion_api

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ingestion", tags=["ingestion"])


@router.post("/run", response_model=IngestionRunResponse)
def post_ingestion_run(req: IngestionRunRequest) -> IngestionRunResponse:
    logger.info("POST /api/ingestion/run  company=%s", req.company)
    result = run_ingestion_api(req.company, force=req.force)
    if result.get("status") == "failed":
        raise HTTPException(status_code=400, detail=result.get("error", "ingestion 실패"))
    return IngestionRunResponse(
        ticker=result.get("ticker", ""),
        company_name=result.get("company_name", ""),
        corp_code=result.get("corp_code", ""),
        status=result.get("status", ""),
        documents=int(result.get("documents", 0)),
        chunks=int(result.get("chunks", 0)),
        embeddings=int(result.get("embeddings", 0)),
    )
