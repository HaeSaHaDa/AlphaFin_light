"""Stock Chain 품질 평가 모듈."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHAIN_DIR = PROJECT_ROOT / "data" / "stock_chain"


def evaluate_stock_chain(unified_result: dict) -> dict:
    """Stock Chain 품질을 평가한다."""
    sc = unified_result.get("stock_chain", {})
    trace_id = unified_result.get("trace_id", "")

    entity_count = sc.get("entity_count", 0)
    link_count = sc.get("link_count", 0)
    propagation_paths = sc.get("propagation_paths", 0)

    chain_data = _load_chain_file(trace_id)
    links = chain_data.get("links", []) if chain_data else []

    entity_consistency = min(entity_count / 10.0, 1.0) if entity_count else 0.0
    propagation_consistency = min(propagation_paths / 10.0, 1.0) if propagation_paths else 0.0

    relation_types = set(l.get("relation_type", "") for l in links)
    relation_quality = min(len(relation_types) / 4.0, 1.0) if relation_types else 0.5

    has_samsung = any(
        "삼성" in l.get("target", "") or "삼성" in l.get("source", "")
        for l in links
    )
    has_hbm = any(
        "HBM" in l.get("target", "") or "HBM" in l.get("source", "")
        for l in links
    )
    chain_continuity = 0.0
    if has_samsung and has_hbm:
        chain_continuity = 0.9
    elif link_count >= 5:
        chain_continuity = 0.7
    else:
        chain_continuity = 0.4

    ticker_links = sum(
        1 for l in links if l.get("source_ticker") or l.get("target_ticker")
    )
    ticker_score = min(ticker_links / max(len(links), 1), 1.0) if links else 0.5

    factors = {
        "entity_consistency": round(entity_consistency, 4),
        "propagation_consistency": round(propagation_consistency, 4),
        "relation_quality": round(relation_quality, 4),
        "chain_continuity": round(chain_continuity, 4),
        "ticker_connection": round(ticker_score, 4),
    }

    stock_chain_score = round(sum(factors.values()) / len(factors), 4)

    result = {
        "stock_chain_score": stock_chain_score,
        "factors": factors,
        "entity_count": entity_count,
        "link_count": link_count,
        "propagation_paths": propagation_paths,
    }

    logger.info(
        "Stock Chain 평가  score=%.4f  links=%d",
        stock_chain_score, link_count,
    )
    return result


def _load_chain_file(trace_id: str) -> dict | None:
    if not trace_id:
        return None
    fp = CHAIN_DIR / f"{trace_id}_chain.json"
    if not fp.exists():
        for alt in CHAIN_DIR.glob("*_chain.json"):
            try:
                with open(alt, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception):
                continue
        return None
    try:
        with open(fp, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return None
