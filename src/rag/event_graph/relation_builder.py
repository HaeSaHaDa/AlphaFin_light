"""Event Relation 생성 모듈."""
from __future__ import annotations

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

RELATION_TYPES = [
    "benefit",
    "supply",
    "competition",
    "impact",
    "price_impact",
    "demand_increase",
    "risk_propagation",
]

_IMPACT_CHAIN_RULES: list[dict] = [
    {
        "source_type": "market_event",
        "source_events": ["demand_increase", "market_growth"],
        "target_type": "product",
        "relation_type": "demand_increase",
        "confidence": 0.80,
    },
    {
        "source_type": "product",
        "target_type": "company",
        "relation_type": "benefit",
        "confidence": 0.75,
    },
    {
        "source_type": "market_event",
        "source_events": ["price_increase"],
        "target_type": "company",
        "relation_type": "price_impact",
        "confidence": 0.70,
    },
    {
        "source_type": "market_event",
        "source_events": ["competition_increase", "regulation_tightening"],
        "target_type": "company",
        "relation_type": "risk_propagation",
        "confidence": 0.65,
    },
    {
        "source_type": "industry",
        "target_type": "company",
        "relation_type": "impact",
        "confidence": 0.70,
    },
    {
        "source_type": "company",
        "target_type": "company",
        "relation_type": "competition",
        "confidence": 0.60,
    },
]


def build_event_relations(nodes: list[dict]) -> list[dict]:
    """Node 목록에서 규칙 기반으로 Relation을 생성한다.

    Args:
        nodes: extract_event_nodes 결과 목록.

    Returns:
        Relation dict 목록.
    """
    relations: list[dict] = []
    seen: set[str] = set()

    for rule in _IMPACT_CHAIN_RULES:
        sources = [n for n in nodes if n["node_type"] == rule["source_type"]]
        targets = [n for n in nodes if n["node_type"] == rule["target_type"]]

        allowed_events = rule.get("source_events")

        for src in sources:
            if allowed_events and src.get("event_type") not in allowed_events:
                continue

            for tgt in targets:
                if src["name"] == tgt["name"]:
                    continue

                key = f"{src['name']}→{tgt['name']}→{rule['relation_type']}"
                if key in seen:
                    continue
                seen.add(key)

                relations.append(_build_relation(
                    source=src["name"],
                    target=tgt["name"],
                    relation_type=rule["relation_type"],
                    confidence=rule["confidence"],
                    source_node=src,
                    target_node=tgt,
                ))

    logger.info(
        "Relation 생성  노드=%d  관계=%d", len(nodes), len(relations),
    )
    return relations


def detect_market_impact_relations(
    analysis_result: dict,
    nodes: list[dict],
) -> list[dict]:
    """분석 결과의 bullish/bearish/risks에서 영향 관계를 추가 추출한다."""
    relations: list[dict] = []

    company_nodes = [n for n in nodes if n["node_type"] == "company"]
    if not company_nodes:
        return relations

    primary_company = company_nodes[0]["name"]

    for factor in analysis_result.get("bullish_factors", []):
        relations.append(_build_relation(
            source=factor[:40],
            target=primary_company,
            relation_type="benefit",
            confidence=0.75,
        ))

    for factor in analysis_result.get("bearish_factors", []):
        relations.append(_build_relation(
            source=factor[:40],
            target=primary_company,
            relation_type="risk_propagation",
            confidence=0.70,
        ))

    for risk in analysis_result.get("risks", []):
        relations.append(_build_relation(
            source=risk[:40],
            target=primary_company,
            relation_type="risk_propagation",
            confidence=0.65,
        ))

    logger.info(
        "Impact Relation 추출  bullish=%d  bearish=%d  risks=%d  총=%d",
        len(analysis_result.get("bullish_factors", [])),
        len(analysis_result.get("bearish_factors", [])),
        len(analysis_result.get("risks", [])),
        len(relations),
    )
    return relations


def _build_relation(
    source: str,
    target: str,
    relation_type: str,
    confidence: float,
    source_node: dict | None = None,
    target_node: dict | None = None,
) -> dict:
    return {
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "confidence": round(confidence, 4),
        "source_ticker": (source_node or {}).get("ticker"),
        "target_ticker": (target_node or {}).get("ticker"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
