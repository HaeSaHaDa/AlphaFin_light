"""Company API Schema."""
from __future__ import annotations

from pydantic import BaseModel


class CompanySearchItem(BaseModel):
    company_name: str
    ticker: str
    corp_code: str = ""
    market: str = ""
