"""Event Node 및 Market Entity 추출 모듈."""
from __future__ import annotations

import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

NODE_TYPES = [
    "company", "industry", "product",
    "market_event", "earnings_event",
    "supply_chain_event", "technology_event",
]

COMPANY_KEYWORDS: dict[str, str] = {
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
    "반도체", "메모리", "AI", "서버", "데이터센터",
    "파운드리", "패키징", "모바일", "자동차",
]

PRODUCT_KEYWORDS = [
    "HBM", "DRAM", "NAND", "DDR5", "LPDDR",
    "GPU", "CPU", "NPU", "SSD",
]

EVENT_PATTERNS: list[tuple[str, str]] = [
    (r"수요\s*증가", "demand_increase"),
    (r"수출\s*증가", "export_increase"),
    (r"가격\s*상승", "price_increase"),
    (r"가격\s*하락", "price_decrease"),
    (r"실적\s*개선", "earnings_improvement"),
    (r"실적\s*악화", "earnings_decline"),
    (r"공급\s*부족", "supply_shortage"),
    (r"공급\s*과잉", "supply_excess"),
    (r"투자\s*확대", "investment_expansion"),
    (r"시장\s*성장", "market_growth"),
    (r"경쟁\s*심화", "competition_increase"),
    (r"기술\s*발전", "tech_advancement"),
    (r"규제\s*강화", "regulation_tightening"),
    (r"수혜", "benefit"),
    (r"리스크", "risk"),
]


def extract_event_nodes(text: str) -> list[dict]:
    """텍스트에서 Event Node를 추출한다.

    Args:
        text: 분석 대상 텍스트 (뉴스, 공시, 분석 결과 등).

    Returns:
        추출된 Node dict 목록.
    """
    nodes: list[dict] = []
    seen: set[str] = set()

    for name, ticker in COMPANY_KEYWORDS.items():
        if name in text and name not in seen:
            seen.add(name)
            nodes.append(_build_node(name, "company", ticker=ticker))

    for kw in INDUSTRY_KEYWORDS:
        if kw in text and kw not in seen:
            seen.add(kw)
            nodes.append(_build_node(kw, "industry"))

    for kw in PRODUCT_KEYWORDS:
        if kw in text and kw not in seen:
            seen.add(kw)
            nodes.append(_build_node(kw, "product"))

    for pattern, event_type in EVENT_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            label = match.strip()
            if label not in seen:
                seen.add(label)
                nodes.append(_build_node(
                    label, "market_event", event_type=event_type,
                ))

    logger.info("Event Node 추출  텍스트=%d자  노드=%d개", len(text), len(nodes))
    return nodes


def extract_market_entities(text: str) -> dict:
    """텍스트에서 기업/산업/제품 엔티티를 분류 추출한다.

    Returns:
        {"companies": [...], "industries": [...], "products": [...]}
    """
    companies = []
    for name, ticker in COMPANY_KEYWORDS.items():
        if name in text:
            companies.append({"name": name, "ticker": ticker})

    industries = [kw for kw in INDUSTRY_KEYWORDS if kw in text]
    products = [kw for kw in PRODUCT_KEYWORDS if kw in text]

    result = {
        "companies": companies,
        "industries": industries,
        "products": products,
    }

    logger.info(
        "Entity 추출  기업=%d  산업=%d  제품=%d",
        len(companies), len(industries), len(products),
    )
    return result


def _build_node(
    name: str,
    node_type: str,
    ticker: str | None = None,
    event_type: str | None = None,
) -> dict:
    return {
        "name": name,
        "node_type": node_type,
        "ticker": ticker,
        "event_type": event_type,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
