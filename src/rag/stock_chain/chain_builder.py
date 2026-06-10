"""Stock Chain 생성 모듈."""
from __future__ import annotations

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def build_stock_chain(
    entities: list[dict],
    query: str = "",
    ticker: str | None = None,
) -> dict:
    """Runtime Entity를 담고 Event Graph Relation 병합을 준비한다."""
    chain = {
        "query": query,
        "ticker": ticker,
        "entities": entities,
        "links": [],
        "metadata": {
            "entity_count": len(entities),
            "link_count": 0,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    }

    logger.info("Stock Chain 생성  runtime entities=%d", len(entities))
    return chain


def merge_event_graph_links(chain: dict, event_graph: dict) -> dict:
    """Event Graph Relation을 Stock Chain에 병합한다."""
    existing = {
        f"{l['source']}→{l['target']}" for l in chain.get("links", [])
    }

    for rel in event_graph.get("relations", []):
        key = f"{rel['source']}→{rel['target']}"
        if key in existing:
            continue
        existing.add(key)
        chain["links"].append({
            "source": rel["source"],
            "target": rel["target"],
            "relation_type": rel.get("relation_type", "impact"),
            "impact_score": rel.get("confidence", 0.6),
            "source_ticker": rel.get("source_ticker"),
            "target_ticker": rel.get("target_ticker"),
            "from_event_graph": True,
        })

    chain["metadata"]["link_count"] = len(chain["links"])
    logger.info("Event Graph 병합  총 links=%d", len(chain["links"]))
    return chain
