"""selectedTicker 중심 Stock Chain / Event Graph payload 생성."""
from __future__ import annotations

import re
from typing import Any


def parse_company_name(query: str, ticker: str) -> str:
    """runtime query에서 회사명 추출 (ticker·키워드 제거)."""
    q = (query or "").strip()
    t = (ticker or "").strip()
    if t:
        q = re.sub(rf"\b{t}\b", "", q).strip()
    parts = [p for p in re.split(r"\s+", q) if p and not p.isdigit()]
    return parts[0] if parts else ""


def _is_conflicting_company(entity: dict, selected_ticker: str) -> bool:
    """다른 종목 ticker를 가진 company entity — 샘플 graph 오염 제거."""
    if not selected_ticker:
        return False
    if entity.get("entity_type") != "company":
        return False
    et = (entity.get("ticker") or "").strip()
    if et and et != selected_ticker:
        return True
    return False


def _bfs_names_from_center(
    center_name: str,
    links: list[dict],
    max_depth: int = 2,
) -> set[str]:
    if not center_name:
        return set()
    adj: dict[str, set[str]] = {}
    for ln in links:
        s, t = ln.get("source"), ln.get("target")
        if not s or not t:
            continue
        adj.setdefault(s, set()).add(t)
        adj.setdefault(t, set()).add(s)

    visited = {center_name}
    frontier = {center_name}
    for _ in range(max_depth):
        nxt: set[str] = set()
        for node in frontier:
            for nb in adj.get(node, set()):
                if nb not in visited:
                    visited.add(nb)
                    nxt.add(nb)
        frontier = nxt
        if not frontier:
            break
    return visited


def _chain_from_retrieval_chunks(
    center_name: str,
    ticker: str,
    chunks: list[dict],
) -> tuple[list[dict], list[dict]]:
    """stock_chain 파일이 없거나 오염 시 retrieval chunk 기반 최소 graph."""
    entities: list[dict] = [
        {
            "name": center_name,
            "entity_type": "company",
            "ticker": ticker,
            "is_center": True,
        },
    ]
    links: list[dict] = []
    seen: set[str] = set()
    for i, ch in enumerate(chunks[:6]):
        doc = ch.get("document_type") or "document"
        label = f"{doc} #{ch.get('chunk_id', i + 1)}"
        if label in seen:
            continue
        seen.add(label)
        entities.append({
            "name": label,
            "entity_type": "market_event",
            "ticker": None,
        })
        links.append({
            "source": center_name,
            "target": label,
            "relation_type": "retrieval",
            "impact_score": float(ch.get("score") or 0.5),
        })
    return entities, links


def build_ticker_centric_chain(
    chain: dict | None,
    ticker: str,
    query: str,
    retrieval_chunks: list[dict] | None = None,
) -> dict:
    """
    selectedTicker 중심 entities/links.
    다른 KOSPI company ticker(예: 005930)는 제거 — 삼성전자 sample fallback 방지.
    """
    ticker = (ticker or "").strip()
    center_name = parse_company_name(query, ticker) or ticker
    raw_entities = list((chain or {}).get("entities") or [])
    raw_links = list((chain or {}).get("links") or [])

    # 1) 오염 company 제거
    entities = [e for e in raw_entities if not _is_conflicting_company(e, ticker)]
    links = list(raw_links)

    # 2) center entity 보장
    center_ent = None
    for e in entities:
        if e.get("ticker") == ticker or e.get("name") == center_name:
            center_ent = {**e, "ticker": ticker, "is_center": True}
            break
    if not center_ent:
        center_ent = {
            "name": center_name,
            "entity_type": "company",
            "ticker": ticker,
            "is_center": True,
        }
        entities.insert(0, center_ent)
    else:
        entities = [
            {**e, "is_center": e.get("name") == center_ent.get("name")}
            for e in entities
        ]

    # 3) center 기준 BFS로 연결된 노드만 유지 (company 외 industry/product)
    bfs_root = center_ent.get("name") or center_name
    if links:
        reachable = _bfs_names_from_center(bfs_root, links, max_depth=2)
        reachable.add(bfs_root)
        entities = [e for e in entities if e.get("name") in reachable]
        names = {e.get("name") for e in entities}
        links = [
            ln
            for ln in links
            if ln.get("source") in names and ln.get("target") in names
        ]

    # 4) 링크 없으면 retrieval 기반만 (engine chain 미사용)
    if not links and retrieval_chunks:
        entities, links = _chain_from_retrieval_chunks(
            center_name, ticker, retrieval_chunks,
        )
    elif not links and not entities:
        entities, links = _chain_from_retrieval_chunks(
            center_name, ticker, retrieval_chunks or [],
        )

    return {
        "entities": entities,
        "links": links,
        "center_name": center_ent.get("name") or center_name,
        "center_ticker": ticker,
    }
