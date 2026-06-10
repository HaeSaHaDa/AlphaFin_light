"""Disclosure ingestion cache."""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / "data" / "disclosure_cache"
DISCLOSURE_BODY_CACHE_VERSION = 1
DISCLOSURE_CACHE_TTL_HOURS = 12


def cache_path(ticker: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{ticker}.json"


def load_cache(ticker: str) -> dict | None:
    path = cache_path(ticker)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_cache(ticker: str, payload: dict) -> dict:
    path = cache_path(ticker)
    data = {**payload, "updated_at": datetime.now().isoformat()}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def has_current_body_cache(payload: dict | None) -> bool:
    return bool(
        payload
        and payload.get("body_cache_version") == DISCLOSURE_BODY_CACHE_VERSION
        and payload.get("status") not in {"failed", "timeout", "partial"}
        and (
            int(payload.get("fetched") or 0) > 0
            or int(payload.get("chunks") or 0) > 0
        )
    )


def get_disclosure_cache_status(
    payload: dict | None,
    *,
    ttl_hours: int = DISCLOSURE_CACHE_TTL_HOURS,
) -> dict:
    updated_at = (payload or {}).get("updated_at", "")
    fresh = False
    age_hours: float | None = None
    if has_current_body_cache(payload) and updated_at:
        try:
            updated = datetime.fromisoformat(updated_at)
            age = datetime.now() - updated
            age_hours = max(0.0, age.total_seconds() / 3600)
            fresh = age <= timedelta(hours=ttl_hours)
        except ValueError:
            pass
    if not payload:
        usage = "MISS"
    elif fresh:
        usage = "HIT"
    else:
        usage = "STALE"
    return {
        "cache_status": usage,
        "cache_fresh": fresh,
        "cache_updated_at": updated_at,
        "cache_age_hours": round(age_hours, 2) if age_hours is not None else None,
        "cache_ttl_hours": ttl_hours,
    }


def has_fresh_body_cache(payload: dict | None) -> bool:
    return bool(get_disclosure_cache_status(payload)["cache_fresh"])
