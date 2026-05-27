"""Stock Chain 저장 및 조회 모듈."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CHAIN_DIR = PROJECT_ROOT / "data" / "stock_chain"
PROPAGATION_LOG_DIR = DEFAULT_CHAIN_DIR / "propagation_logs"


def save_stock_chain(
    chain: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path | None:
    """Stock Chain을 JSON으로 저장한다."""
    out = Path(output_dir) if output_dir else DEFAULT_CHAIN_DIR
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        ticker = chain.get("ticker", "general")
        query_slug = chain.get("query", "chain")[:20].replace(" ", "_")
        filename = f"{ticker}_{query_slug}_chain.json"

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chain, f, ensure_ascii=False, indent=2)

    logger.info("Stock Chain 저장  %s", filepath)
    return filepath


def load_related_chains(
    ticker: str,
    chain_dir: Path | str | None = None,
) -> list[dict]:
    """ticker 관련 Stock Chain을 로드한다."""
    out = Path(chain_dir) if chain_dir else DEFAULT_CHAIN_DIR
    if not out.exists():
        return []

    results: list[dict] = []
    for fp in out.glob("*_chain.json"):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                chain = json.load(f)
            if chain.get("ticker") == ticker:
                results.append(chain)
                continue
            for ent in chain.get("entities", []):
                if ent.get("ticker") == ticker:
                    results.append(chain)
                    break
            for link in chain.get("links", []):
                if link.get("source_ticker") == ticker or link.get("target_ticker") == ticker:
                    if chain not in results:
                        results.append(chain)
                    break
        except (json.JSONDecodeError, Exception):
            logger.warning("Chain 파싱 실패  %s", fp)

    logger.info("관련 Chain 조회  ticker=%s  결과=%d건", ticker, len(results))
    return results


def save_propagation_log(
    propagation: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path:
    """Propagation log를 저장한다."""
    out = Path(output_dir) if output_dir else PROPAGATION_LOG_DIR
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        seed = propagation.get("seed_event", "event")[:15].replace(" ", "_")
        filename = f"{seed}_propagation.json"

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(propagation, f, ensure_ascii=False, indent=2)

    logger.info("propagation log 저장  %s", filepath.name)
    return filepath


def build_stock_chain_context(
    chains: list[dict],
    propagation_paths: list[dict] | None = None,
    max_links: int = 8,
) -> str:
    """Stock Chain을 Prompt Context 문자열로 변환한다."""
    if not chains and not propagation_paths:
        return ""

    parts: list[str] = ["[Stock Chain]"]

    seen_links: set[str] = set()
    count = 0

    for chain in chains:
        for link in chain.get("links", []):
            if count >= max_links:
                break
            key = f"{link['source']}→{link['target']}"
            if key in seen_links:
                continue
            seen_links.add(key)

            score = link.get("impact_score", 0)
            rtype = link.get("relation_type", "")
            parts.append(
                f"- {link['source']} → {link['target']}  "
                f"[{rtype}] (impact={score:.2f})"
            )
            count += 1

    if propagation_paths:
        parts.append("")
        parts.append("[Propagation Paths]")
        for path in propagation_paths[:5]:
            parts.append(
                f"- {path.get('path_str', '')}  "
                f"(impact={path.get('cumulative_impact', 0):.2f})"
            )

    parts.append("")
    context = "\n".join(parts)

    logger.info("Stock Chain Context  len=%d  links=%d", len(context), count)
    return context
