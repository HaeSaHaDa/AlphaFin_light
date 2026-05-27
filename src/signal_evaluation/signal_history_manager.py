"""Signal History JSON 저장/조회."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SIGNAL_DIR = PROJECT_ROOT / "data" / "signal_evaluation"
HISTORY_DIR = SIGNAL_DIR / "history"

# 발표용 샘플 시장 결과 (실거래 연동 없음)
DEMO_OUTCOMES: dict[str, dict] = {
    "20260527_123745": {
        "price_change_pct": 4.2,
        "period_label": "1주 후",
        "actual_direction": "up",
    },
}

DEMO_TIMELINE: list[dict] = [
    {"period": "2024-01", "signal": "bullish", "display_label": "긍정", "price_change_pct": 4.2},
    {"period": "2024-02", "signal": "neutral", "display_label": "중립", "price_change_pct": 0.8},
    {"period": "2024-03", "signal": "bearish", "display_label": "부정", "price_change_pct": -2.1},
]


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


def get_market_outcome(trace_id: str, signal: str) -> dict:
    """샘플 시장 결과 (데모용)."""
    if trace_id in DEMO_OUTCOMES:
        return DEMO_OUTCOMES[trace_id].copy()

    defaults = {
        "bullish": 3.5,
        "neutral": 0.5,
        "bearish": -2.8,
    }
    pct = defaults.get(signal, 0.0)
    return {
        "price_change_pct": pct,
        "period_label": "1주 후 (샘플)",
        "actual_direction": "up" if pct > 1 else ("down" if pct < -1 else "flat"),
    }


def get_demo_timeline() -> list[dict]:
    return [e.copy() for e in DEMO_TIMELINE]
