"""TASK-036: selectedTicker 중심 stock chain 검증."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.dashboard_api.services.ticker_centric_chain import build_ticker_centric_chain

SAMPLE_POLLUTED = {
    "entities": [
        {"name": "삼성전자", "entity_type": "company", "ticker": "005930"},
        {"name": "반도체", "entity_type": "industry", "ticker": None},
        {"name": "AI", "entity_type": "market_event", "ticker": None},
    ],
    "links": [
        {"source": "삼성전자", "target": "반도체", "impact_score": 0.9},
        {"source": "반도체", "target": "AI", "impact_score": 0.8},
    ],
}

CASES = [
    ("삼성전기 009150 실적", "009150", "삼성전기", "009150"),
    ("현대자동차 005380 전망", "005380", "현대자동차", "005380"),
]


def main() -> int:
    failed = 0
    for query, ticker, expect_name, expect_ticker in CASES:
        out = build_ticker_centric_chain(SAMPLE_POLLUTED, ticker, query, [])
        center = next((e for e in out["entities"] if e.get("is_center")), None)
        names = {e.get("name") for e in out["entities"]}
        if "삼성전자" in names:
            print(f"FAIL {ticker}: 삼성전자 sample graph 잔존")
            failed += 1
            continue
        if not center:
            print(f"FAIL {ticker}: center entity 없음")
            failed += 1
            continue
        if center.get("name") != expect_name or center.get("ticker") != expect_ticker:
            print(
                f"FAIL {ticker}: center={center.get('name')}/{center.get('ticker')} "
                f"expected {expect_name}/{expect_ticker}",
            )
            failed += 1
            continue
        print(f"OK {ticker}: center {center.get('name')}/{center.get('ticker')}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
