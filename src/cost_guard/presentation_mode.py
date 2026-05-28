"""발표용 Presentation Cache Mode."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = PROJECT_ROOT / "data" / "cost_guard" / "presentation_mode.json"

_presentation_enabled = False


def is_presentation_mode() -> bool:
    global _presentation_enabled
    if _presentation_enabled:
        return True
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return bool(data.get("enabled", False))
        except (json.JSONDecodeError, OSError):
            return False
    return False


def enable_presentation_mode() -> dict:
    global _presentation_enabled
    _presentation_enabled = True
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"enabled": True}
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    logger.info("Presentation mode 활성화")
    return payload


def disable_presentation_mode() -> dict:
    global _presentation_enabled
    _presentation_enabled = False
    payload = {"enabled": False}
    if STATE_PATH.exists():
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    return payload
