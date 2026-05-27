"""Stock Chain Entity 추출 모듈."""
from __future__ import annotations

import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

ENTITY_TYPES = [
    "company", "industry", "product",
    "supply_chain", "technology", "market_event", "price_change",
]

COMPANY_MAP: dict[str, str] = {
    "삼성전자": "005930",
    "SK하이닉스": "000660",
    "NVIDIA": "NVDA",
    "엔비디아": "NVDA",
    "TSMC": "TSM",
    "인텔": "INTC",
    "마이크론": "MU",
    "AMD": "AMD",
}

INDUSTRY_KEYWORDS = [
    "반도체", "메모리", "AI", "서버", "데이터센터", "IT",
]

PRODUCT_KEYWORDS = [
    "HBM", "DRAM", "NAND", "DDR5", "GPU", "CPU", "AI 서버",
]

TECHNOLOGY_KEYWORDS = ["HBM3", "EUV", "파운드리", "패키징"]

MARKET_EVENT_PATTERNS: list[tuple[str, str]] = [
    (r"수요\s*증가", "demand_increase"),
    (r"공급\s*부족", "supply_shortage"),
    (r"투자\s*확대", "investment_expansion"),
    (r"실적\s*발표", "earnings_release"),
    (r"금리\s*인상", "rate_hike"),
]

PRICE_PATTERNS: list[tuple[str, str]] = [
    (r"가격\s*상승", "price_increase"),
    (r"가격\s*하락", "price_decrease"),
    (r"DRAM\s*가격", "dram_price"),
    (r"HBM\s*가격", "hbm_price"),
]

NAME_ALIASES: dict[str, str] = {
    "엔비디아": "NVIDIA",
    "AI서버": "AI 서버",
}


def extract_market_entities(text: str) -> list[dict]:
    """텍스트에서 Stock Chain Entity를 추출한다."""
    entities: list[dict] = []
    seen: set[str] = set()

    for name, ticker in COMPANY_MAP.items():
        if name in text:
            norm = normalize_entity_name(name)
            if norm not in seen:
                seen.add(norm)
                entities.append(_build_entity(norm, "company", ticker=ticker))

    for kw in INDUSTRY_KEYWORDS:
        if kw in text and kw not in seen:
            seen.add(kw)
            entities.append(_build_entity(kw, "industry"))

    for kw in PRODUCT_KEYWORDS:
        if kw in text and kw not in seen:
            seen.add(kw)
            entities.append(_build_entity(kw, "product"))

    for kw in TECHNOLOGY_KEYWORDS:
        if kw in text and kw not in seen:
            seen.add(kw)
            entities.append(_build_entity(kw, "technology"))

    for pattern, event_type in MARKET_EVENT_PATTERNS:
        if re.search(pattern, text):
            label = event_type.replace("_", " ")
            if label not in seen:
                seen.add(label)
                entities.append(_build_entity(
                    label, "market_event", event_type=event_type,
                ))

    for pattern, price_type in PRICE_PATTERNS:
        if re.search(pattern, text):
            label = price_type.replace("_", " ")
            if label not in seen:
                seen.add(label)
                entities.append(_build_entity(
                    label, "price_change", event_type=price_type,
                ))

    if "공급" in text and "공급망" not in seen:
        seen.add("공급망")
        entities.append(_build_entity("공급망", "supply_chain"))

    logger.info("Entity 추출  총=%d건", len(entities))
    return entities


def normalize_entity_name(name: str) -> str:
    """Entity 이름을 정규화한다."""
    return NAME_ALIASES.get(name, name.strip())


def normalize_entities(entities: list[dict]) -> list[dict]:
    """Entity 목록의 이름을 정규화한다."""
    normalized: list[dict] = []
    seen: set[str] = set()

    for ent in entities:
        name = normalize_entity_name(ent.get("name", ""))
        key = f"{ent.get('entity_type', '')}:{name}"
        if key in seen:
            continue
        seen.add(key)

        ent_copy = dict(ent)
        ent_copy["name"] = name
        normalized.append(ent_copy)

    logger.info("Entity 정규화  %d → %d", len(entities), len(normalized))
    return normalized


def entities_from_event_graph(graph: dict) -> list[dict]:
    """Event Graph 노드를 Stock Chain Entity로 변환한다."""
    entities: list[dict] = []
    type_map = {
        "company": "company",
        "industry": "industry",
        "product": "product",
        "market_event": "market_event",
    }

    for node in graph.get("nodes", []):
        etype = type_map.get(node.get("node_type", ""), "market_event")
        entities.append(_build_entity(
            normalize_entity_name(node.get("name", "")),
            etype,
            ticker=node.get("ticker"),
            event_type=node.get("event_type"),
        ))

    return normalize_entities(entities)


def _build_entity(
    name: str,
    entity_type: str,
    ticker: str | None = None,
    event_type: str | None = None,
) -> dict:
    return {
        "name": name,
        "entity_type": entity_type,
        "ticker": ticker,
        "event_type": event_type,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
