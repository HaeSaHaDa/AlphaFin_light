"""Evaluation API Routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.evaluation_schema import EvaluationResponse
from ..services.evaluation_service import fetch_latest_evaluation, fetch_evaluation_by_trace

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/evaluation", tags=["evaluation"])


@router.get("/latest", response_model=EvaluationResponse)
def get_latest_evaluation() -> EvaluationResponse:
    data = fetch_latest_evaluation()
    if not data:
        raise HTTPException(status_code=404, detail="Evaluation 데이터 없음")
    logger.info(
        "GET /api/evaluation/latest  overall=%s",
        data.get("overall_score"),
    )
    return EvaluationResponse(**{k: v for k, v in data.items() if k != "full_report"})


@router.get("/{trace_id}", response_model=EvaluationResponse)
def get_evaluation_by_trace(trace_id: str) -> EvaluationResponse:
    data = fetch_evaluation_by_trace(trace_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"trace_id={trace_id} 없음")
    logger.info("GET /api/evaluation/%s", trace_id)
    return EvaluationResponse(**{k: v for k, v in data.items() if k != "full_report"})
