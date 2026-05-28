"""OpenAI Token Usage 로깅."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
USAGE_DIR = PROJECT_ROOT / "data" / "cost_guard" / "usage"


def _today_key() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _usage_path(day: str | None = None) -> Path:
    day = day or _today_key()
    return USAGE_DIR / f"usage_{day}.json"


def log_usage(
    *,
    operation: str,
    model: str,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    embedding_tokens: int = 0,
    meta: dict | None = None,
) -> None:
    """일별 token usage를 누적 저장한다."""
    USAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = _usage_path()
    entries: list[dict] = []
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            entries = data.get("entries", [])
        except (json.JSONDecodeError, OSError):
            entries = []

    entries.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operation": operation,
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "embedding_tokens": embedding_tokens,
        "meta": meta or {},
    })

    payload = {
        "date": _today_key(),
        "entries": entries,
        "totals": summarize_day(entries),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    logger.info(
        "token usage  op=%s  embed=%d  prompt=%d",
        operation, embedding_tokens, prompt_tokens,
    )


def summarize_day(entries: list[dict]) -> dict:
    return {
        "prompt_tokens": sum(e.get("prompt_tokens", 0) for e in entries),
        "completion_tokens": sum(e.get("completion_tokens", 0) for e in entries),
        "embedding_tokens": sum(e.get("embedding_tokens", 0) for e in entries),
        "call_count": len(entries),
    }


def get_today_usage() -> dict:
    path = _usage_path()
    if not path.exists():
        return {"date": _today_key(), "entries": [], "totals": summarize_day([])}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
