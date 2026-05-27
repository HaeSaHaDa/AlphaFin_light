"""Ingestion API 서비스."""
from __future__ import annotations

from src.ingestion_pipeline.ingestion_runner import run_ingestion


def run_ingestion_api(company: str, force: bool = False) -> dict:
    return run_ingestion(company, force=force)
