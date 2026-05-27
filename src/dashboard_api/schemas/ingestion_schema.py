"""Ingestion API Schema."""
from __future__ import annotations

from pydantic import BaseModel, Field


class IngestionRunRequest(BaseModel):
    company: str = Field(..., description="회사명 또는 질문 텍스트")
    force: bool = False


class IngestionRunResponse(BaseModel):
    ticker: str
    company_name: str = ""
    corp_code: str = ""
    status: str
    documents: int = 0
    chunks: int = 0
    embeddings: int = 0
    error: str | None = None
