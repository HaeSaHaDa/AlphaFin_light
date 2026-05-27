"""Company Search API."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Query

from ..schemas.company_schema import CompanySearchItem
from ..services.company_service import search_company

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/company", tags=["company"])


@router.get("/search", response_model=list[CompanySearchItem])
def get_company_search(q: str = Query("", min_length=1)) -> list[CompanySearchItem]:
    items = search_company(q)
    logger.info("GET /api/company/search  q=%s  hits=%d", q, len(items))
    return [CompanySearchItem(**item) for item in items]
