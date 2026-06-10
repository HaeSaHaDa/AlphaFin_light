"""Signal History JSON 저장/조회."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SIGNAL_DIR = PROJECT_ROOT / "data" / "signal_evaluation"
HISTORY_DIR = SIGNAL_DIR / "history"


def ensure_dirs() -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def save_signal_record(record: dict) -> Path:
    """trace_id 기준 Signal 기록 저장."""
    ensure_dirs()
    trace_id = record.get("trace_id", "unknown")
    path = HISTORY_DIR / f"{trace_id}_signal.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    logger.info("Signal 저장  %s", path.name)
    return path


def load_signal_record(trace_id: str) -> dict | None:
    path = HISTORY_DIR / f"{trace_id}_signal.json"
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Signal 로드 실패  %s  %s", path, e)
        return None


def load_latest_signal() -> dict | None:
    if not HISTORY_DIR.exists():
        return None
    files = sorted(HISTORY_DIR.glob("*_signal.json"), reverse=True)
    if not files:
        return None
    try:
        with open(files[0], "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (json.JSONDecodeError, OSError):
        return None
