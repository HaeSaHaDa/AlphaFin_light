"""Ingestion cache 상태 (vector_index_manager 래핑)."""
from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = PROJECT_ROOT / "data" / "ingestion_cache"


def list_cached_tickers() -> list[dict]:
    if not CACHE_DIR.exists():
        return []
    out: list[dict] = []
    for fp in CACHE_DIR.glob("*.json"):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            out.append(data)
        except (json.JSONDecodeError, OSError):
            continue
    return out


def get_cache_status() -> dict:
    tickers = list_cached_tickers()
    return {
        "count": len(tickers),
        "tickers": tickers,
    }
