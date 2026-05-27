"""Stock Chain 생성 모듈."""
from __future__ import annotations

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

SUPPLY_CHAIN_RULES: list[dict] = [
    {"source": "NVIDIA", "target": "GPU", "relation_type": "supply", "impact_score": 0.85},
    {"source": "GPU", "target": "AI 서버", "relation_type": "demand_propagation", "impact_score": 0.82},
    {"source": "AI 서버", "target": "HBM", "relation_type": "demand_propagation", "impact_score": 0.88},
    {"source": "HBM", "target": "삼성전자", "relation_type": "supply", "impact_score": 0.80},
    {"source": "HBM", "target": "SK하이닉스", "relation_type": "supply", "impact_score": 0.78},
    {"source": "HBM", "target": "DRAM", "relation_type": "product_link", "impact_score": 0.75},
    {"source": "DRAM", "target": "dram price", "relation_type": "price_impact", "impact_score": 0.72},
    {"source": "삼성전자", "target": "반도체", "relation_type": "industry_link", "impact_score": 0.70},
    {"source": "반도체", "target": "메모리", "relation_type": "industry_link", "impact_score": 0.68},
]

INDUSTRY_CHAIN_RULES: list[dict] = [
    {"source": "AI", "target": "서버", "relation_type": "industry_link", "impact_score": 0.75},
    {"source": "서버", "target": "데이터센터", "relation_type": "industry_link", "impact_score": 0.72},
    {"source": "메모리", "target": "반도체", "relation_type": "industry_link", "impact_score": 0.70},
]

NEGATIVE_PROPAGATION_RULES: list[dict] = [
    {"source": "rate hike", "target": "IT", "relation_type": "risk_propagation", "impact_score": 0.70},
    {"source": "IT", "target": "반도체", "relation_type": "demand_decrease", "impact_score": 0.68},
    {"source": "반도체", "target": "삼성전자", "relation_type": "risk_propagation", "impact_score": 0.65},
]


def _entity_names(entities: list[dict]) -> set[str]:
    return {e.get("name", "") for e in entities}


def build_supply_chain_relations(entities: list[dict]) -> list[dict]:
    """공급망 기반 Chain Relation을 생성한다."""
    names = _entity_names(entities)
    relations: list[dict] = []
    seen: set[str] = set()

    for rule in SUPPLY_CHAIN_RULES:
        src, tgt = rule["source"], rule["target"]
        if src in names or tgt in names or _fuzzy_match(names, src, tgt):
            key = f"{src}→{tgt}"
            if key in seen:
                continue
            seen.add(key)
            relations.append(_build_link(
                src, tgt,
                rule["relation_type"],
                rule["impact_score"],
                entities,
            ))

    logger.info("공급망 Relation  %d건", len(relations))
    return relations


def build_industry_chain_relations(entities: list[dict]) -> list[dict]:
    """산업 연결 Chain Relation을 생성한다."""
    names = _entity_names(entities)
    relations: list[dict] = []
    seen: set[str] = set()

    for rule in INDUSTRY_CHAIN_RULES + NEGATIVE_PROPAGATION_RULES:
        src, tgt = rule["source"], rule["target"]
        if src in names or tgt in names:
            key = f"{src}→{tgt}"
            if key in seen:
                continue
            seen.add(key)
            relations.append(_build_link(
                src, tgt,
                rule["relation_type"],
                rule["impact_score"],
                entities,
            ))

    logger.info("산업 Chain Relation  %d건", len(relations))
    return relations


def build_stock_chain(
    entities: list[dict],
    query: str = "",
    ticker: str | None = None,
) -> dict:
    """Entity 목록으로 Stock Chain을 구성한다."""
    supply = build_supply_chain_relations(entities)
    industry = build_industry_chain_relations(entities)
    links = supply + industry

    chain = {
        "query": query,
        "ticker": ticker,
        "entities": entities,
        "links": links,
        "metadata": {
            "entity_count": len(entities),
            "link_count": len(links),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    }

    logger.info(
        "Stock Chain 생성  entities=%d  links=%d",
        len(entities), len(links),
    )
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


def _fuzzy_match(names: set[str], src: str, tgt: str) -> bool:
    text = " ".join(names).lower()
    return src.lower() in text or tgt.lower() in text


def _find_ticker(name: str, entities: list[dict]) -> str | None:
    for ent in entities:
        if ent.get("name") == name:
            return ent.get("ticker")
    return None


def _build_link(
    source: str,
    target: str,
    relation_type: str,
    impact_score: float,
    entities: list[dict],
) -> dict:
    return {
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "impact_score": round(impact_score, 4),
        "source_ticker": _find_ticker(source, entities),
        "target_ticker": _find_ticker(target, entities),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
