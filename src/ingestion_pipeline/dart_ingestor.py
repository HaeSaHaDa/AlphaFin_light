"""OpenDART 공시 수집 → DB 저장."""
from __future__ import annotations

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DART_DIR = PROJECT_ROOT / "src" / "collectors" / "opendart"
DB_DIR = PROJECT_ROOT / "src" / "common" / "db"


def ingest_dart(corp_code: str, ticker: str, days: int = 180) -> int:
    """공시 목록을 조회해 dart_disclosures에 저장한다."""
    if str(DART_DIR) not in sys.path:
        sys.path.insert(0, str(DART_DIR))
    if str(DB_DIR) not in sys.path:
        sys.path.insert(0, str(DB_DIR))

    from collector import fetch_disclosures  # type: ignore[import]
    from store import insert_dart_disclosures  # type: ignore[import]

    end = datetime.now()
    start = end - timedelta(days=days)
    begin_date = start.strftime("%Y%m%d")
    end_date = end.strftime("%Y%m%d")

    try:
        resp = fetch_disclosures(corp_code, begin_date, end_date)
    except Exception:
        logger.exception("공시 수집 실패  corp_code=%s", corp_code)
        return 0

    items = resp.get("list") or []
    for d in items:
        d["corp_code"] = corp_code
        d["stock_code"] = ticker

    raw_dir = PROJECT_ROOT / "data" / "raw" / "dart"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"{ticker}_disclosures.json"

    import json

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(resp, f, ensure_ascii=False, indent=2)

    inserted = insert_dart_disclosures(items, raw_file_path=str(raw_path))
    logger.info("공시 DB 저장  ticker=%s  inserted=%d", ticker, inserted)
    return inserted
