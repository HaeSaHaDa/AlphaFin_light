"""selectedTicker 중심 Market Relationship Graph payload."""
from __future__ import annotations

import re

from .ticker_centric_chain import build_ticker_centric_chain, parse_company_name
from .trace_service import get_trace_by_id, get_unified_result_by_trace, load_stock_chain_file

RELATION_MAP: dict[str, str] = {
    "supply": "SUPPLIES",
    "supplies": "SUPPLIES",
    "demand_propagation": "AFFECTED_BY",
    "demand": "AFFECTED_BY",
    "impact": "AFFECTED_BY",
    "competition": "COMPETES_WITH",
    "compete": "COMPETES_WITH",
    "competitor": "COMPETES_WITH",
    "dependency": "DEPENDS_ON",
    "depends": "DEPENDS_ON",
    "depends_on": "DEPENDS_ON",
    "risk": "EXPOSED_TO",
    "exposed": "EXPOSED_TO",
    "retrieval": "RELATED_TO",
}

CATEGORY_MAP: dict[str, str] = {
    "company": "company",
    "industry": "sector",
    "product": "product",
    "market_event": "theme",
    "supply_chain": "product",
    "price_change": "macro",
}

MACRO_KEYWORDS: dict[str, tuple[str, str]] = {
    "금리": ("macro:금리", "AFFECTED_BY"),
    "환율": ("macro:환율", "AFFECTED_BY"),
    "유가": ("macro:유가", "AFFECTED_BY"),
    "ira": ("macro:IRA 정책", "BENEFITS_FROM"),
    "중국": ("risk:중국 리스크", "EXPOSED_TO"),
}


def _map_relation(raw: str | None) -> str:
    key = (raw or "").strip().lower()
    return RELATION_MAP.get(key, "RELATED_TO")


def _map_category(entity_type: str | None, *, is_center: bool = False) -> str:
    if is_center:
        return "company"
    return CATEGORY_MAP.get((entity_type or "").strip().lower(), "theme")


def _impact_from_relation(relation_type: str) -> str:
    if relation_type in ("EXPOSED_TO", "COMPETES_WITH"):
        return "negative"
    if relation_type in ("BENEFITS_FROM", "SUPPLIES"):
        return "positive"
    return "neutral"


def _relation_direction(source: str, target: str, center_name: str, relation_type: str) -> str:
    if relation_type in ("AFFECTED_BY", "BENEFITS_FROM"):
        if target == center_name:
            return "inbound"
    if source == center_name:
        return "outbound"
    if target == center_name:
        return "inbound"
    return "lateral"


def _relevance(impact: float | None, *, is_center: bool = False) -> float:
    if is_center:
        return 1.0
    base = float(impact) if impact is not None else 0.55
    return round(min(1.0, max(0.35, base)), 3)


def _confidence(
    relevance: float,
    evidence_count: int,
    relation_type: str,
) -> float:
    rel_bias = 0.05 if relation_type in ("SUPPLIES", "EXPOSED_TO", "BENEFITS_FROM") else 0.0
    bonus = min(0.18, evidence_count * 0.06) + rel_bias
    return round(min(0.98, max(0.4, relevance + bonus)), 3)


def _keywords_from_query(query: str, ticker: str, company: str) -> list[str]:
    q = (query or "").strip()
    for token in [ticker, company, *company.split()]:
        if token:
            q = q.replace(token, " ")
    parts = [p for p in re.split(r"[\s,·]+", q) if len(p) >= 2]
    return parts[:6]


def _build_evidence_from_chunks(
    chunks: list[dict],
    ticker: str,
    relation_type: str,
) -> list[str]:
    out: list[str] = []
    selected = [ch for ch in chunks if isinstance(ch, dict) and ch.get("ticker") == ticker][:2]
    for ch in selected:
        out.append(
            f"retrieval:{ch.get('document_type', 'doc')}#{ch.get('chunk_id', '?')}",
        )
    if relation_type in ("EXPOSED_TO", "AFFECTED_BY"):
        out.append("analysis:risks")
    return out[:3]


def _explain_relation(source: str, target: str, relation_type: str, center_name: str) -> str:
    if relation_type == "BENEFITS_FROM":
        return f"{center_name}는 {source} 이슈의 수혜 가능성이 있습니다."
    if relation_type == "EXPOSED_TO":
        return f"{center_name}는 {target if source == center_name else source} 리스크에 노출됩니다."
    if relation_type == "SUPPLIES":
        return f"{source}는 {target}에 공급망 영향이 있습니다."
    if relation_type == "COMPETES_WITH":
        return f"{source}와 {target}는 경쟁 구도로 연결됩니다."
    if relation_type == "DEPENDS_ON":
        return f"{source}는 {target}에 의존적인 관계로 해석됩니다."
    return f"{source}와 {target}는 시장 이슈로 연관됩니다."


def _relation_to_story(rel: dict) -> str:
    return (
        f"{rel.get('source')} → {rel.get('target')} "
        f"({rel.get('relation')}, conf {rel.get('confidence')})"
    )


def _base_context(trace_id: str) -> tuple[dict, str, str, str, dict, list[dict], dict]:
    result = get_unified_result_by_trace(trace_id) or {}
    ticker = (result.get("ticker") or "").strip()
    query = result.get("query") or ""
    company = parse_company_name(query, ticker) or ticker
    analysis = result.get("analysis_result") or {}
    chunks = analysis.get("referenced_chunks") or []
    chain_file = load_stock_chain_file(trace_id) or {}
    centered = build_ticker_centric_chain(
        chain_file, ticker, query, retrieval_chunks=chunks,
    )
    center_name = centered.get("center_name") or company
    return result, ticker, query, center_name, analysis, chunks, centered


def build_market_graph_by_trace(trace_id: str) -> dict | None:
    result, ticker, query, center_name, analysis, chunks, centered = _base_context(trace_id)
    if not result:
        return None

    nodes: list[dict] = []
    edges: list[dict] = []
    seen_nodes: set[str] = set()

    def add_node(
        node_id: str,
        label: str,
        category: str,
        *,
        node_ticker: str | None = None,
        is_center: bool = False,
        relevance: float = 0.6,
        description: str = "",
    ) -> None:
        if node_id in seen_nodes:
            return
        seen_nodes.add(node_id)
        nodes.append({
            "id": node_id,
            "label": label,
            "category": category,
            "ticker": node_ticker,
            "is_center": is_center,
            "relevance": relevance,
            "description": description,
        })

    def add_edge(
        source: str,
        target: str,
        edge_type: str,
        relevance: float,
        reason: str = "",
        evidence: list[str] | None = None,
    ) -> None:
        ev = evidence or []
        edges.append({
            "id": f"{source}->{target}:{edge_type}",
            "source": source,
            "target": target,
            "edge_type": edge_type,
            "direction": _relation_direction(source, target, center_name, edge_type),
            "confidence": _confidence(relevance, len(ev), edge_type),
            "relevance": relevance,
            "impact": _impact_from_relation(edge_type),
            "reason": reason,
            "evidence": ev,
        })

    for ent in centered.get("entities") or []:
        name = ent.get("name") or ""
        if not name:
            continue
        is_center = bool(ent.get("is_center")) or name == center_name
        et = ent.get("entity_type")
        cat = _map_category(et, is_center=is_center)
        if (
            cat == "company"
            and not is_center
            and ent.get("ticker")
            and ent.get("ticker") != ticker
        ):
            cat = "competitor"
        desc = ""
        if cat == "competitor":
            desc = f"{center_name}과(와) 경쟁 구도로 추정됩니다."
        elif cat == "sector":
            desc = f"{center_name} 산업·업종 인텔리전스 연결"
        elif cat == "product":
            desc = f"{center_name} 핵심 제품·공급망 연결"
        add_node(
            name,
            name,
            cat,
            node_ticker=ent.get("ticker"),
            is_center=is_center,
            relevance=_relevance(None, is_center=is_center),
            description=desc,
        )

    for ln in centered.get("links") or []:
        src, tgt = ln.get("source"), ln.get("target")
        if not src or not tgt:
            continue
        edge_type = _map_relation(ln.get("relation_type"))
        relevance = _relevance(ln.get("impact_score"))
        reason = str(ln.get("relation_type") or edge_type)
        evidence = _build_evidence_from_chunks(chunks, ticker, edge_type)
        if src not in seen_nodes:
            add_node(src, src, "theme", relevance=relevance)
        if tgt not in seen_nodes:
            add_node(tgt, tgt, "theme", relevance=relevance)
        add_edge(src, tgt, edge_type, relevance, reason=reason, evidence=evidence)

    for comp in centered.get("entities") or []:
        if comp.get("entity_type") != "company":
            continue
        name = comp.get("name")
        ct = comp.get("ticker")
        if not name or name == center_name or not ct or ct == ticker:
            continue
        add_node(
            name,
            name,
            "competitor",
            node_ticker=ct,
            relevance=0.72,
            description="동종 종목(company entity)",
        )
        add_edge(
            center_name,
            name,
            "COMPETES_WITH",
            0.72,
            reason="동종 company 연결",
            evidence=_build_evidence_from_chunks(chunks, ticker, "COMPETES_WITH"),
        )

    risks: list[str] = []
    for r in analysis.get("risks") or []:
        if isinstance(r, str) and r.strip():
            risks.append(r.strip()[:80])
    for i, risk_text in enumerate(risks[:6]):
        rid = f"risk:{i}:{risk_text[:24]}"
        add_node(
            rid,
            risk_text,
            "risk",
            relevance=0.78,
            description=f"{center_name} 리스크 노출 요인",
        )
        add_edge(
            center_name,
            rid,
            "EXPOSED_TO",
            0.78,
            reason="analysis risks",
            evidence=_build_evidence_from_chunks(chunks, ticker, "EXPOSED_TO"),
        )

    themes: list[str] = []
    for kw in _keywords_from_query(query, ticker, center_name):
        themes.append(kw)
    for bf in (analysis.get("bullish_factors") or [])[:3]:
        if isinstance(bf, str) and len(bf) >= 4:
            themes.append(bf[:40])
    seen_theme: set[str] = set()
    for th in themes:
        key = th.strip()
        if not key or key in seen_theme or key == center_name:
            continue
        seen_theme.add(key)
        tid = f"theme:{key}"
        add_node(
            tid,
            key,
            "theme",
            relevance=0.7,
            description=f"{center_name} 투자 테마·키워드",
        )
        add_edge(
            tid,
            center_name,
            "AFFECTED_BY",
            0.7,
            reason="query/theme",
            evidence=_build_evidence_from_chunks(chunks, ticker, "AFFECTED_BY"),
        )

    # Macro dictionary 기반 관계 생성 (query + risks 기반)
    low = f"{query} {' '.join(risks)}".lower()
    for token, (macro_id, macro_relation) in MACRO_KEYWORDS.items():
        if token.lower() not in low:
            continue
        label = macro_id.split(":", 1)[1]
        category = "macro" if macro_id.startswith("macro:") else "risk"
        add_node(macro_id, label, category, relevance=0.8, description="macro dictionary match")
        if macro_relation == "BENEFITS_FROM":
            add_edge(
                macro_id,
                center_name,
                macro_relation,
                0.82,
                reason=f"macro keyword:{token}",
                evidence=_build_evidence_from_chunks(chunks, ticker, macro_relation),
            )
        else:
            add_edge(
                center_name,
                macro_id,
                macro_relation,
                0.8,
                reason=f"macro keyword:{token}",
                evidence=_build_evidence_from_chunks(chunks, ticker, macro_relation),
            )
        seen_theme.add(label)

    return {
        "trace_id": trace_id,
        "query": query,
        "center_ticker": ticker,
        "center_company": center_name,
        "nodes": nodes,
        "edges": edges,
        "risks": risks,
        "themes": list(seen_theme),
    }


def fetch_relation_explanation(trace_id: str) -> dict | None:
    graph = build_market_graph_by_trace(trace_id)
    if not graph:
        return None
    center_name = graph.get("center_company", "")
    relations: list[dict] = []
    for edge in (graph.get("edges") or [])[:18]:
        relation = edge.get("edge_type", "RELATED_TO")
        relation_row = {
            "source": edge.get("source", ""),
            "target": edge.get("target", ""),
            "relation": relation,
            "direction": edge.get("direction", "lateral"),
            "confidence": float(edge.get("confidence") or edge.get("relevance") or 0.5),
            "impact": edge.get("impact", "neutral"),
            "explanation": _explain_relation(
                edge.get("source", ""),
                edge.get("target", ""),
                relation,
                center_name,
            ),
            "evidence": list(edge.get("evidence") or []),
        }
        # weak relation pruning
        if relation_row["confidence"] < 0.55 and relation == "RELATED_TO":
            continue
        relations.append(relation_row)
    return {
        "trace_id": trace_id,
        "center_ticker": graph.get("center_ticker", ""),
        "center_company": center_name,
        "relations": relations[:12],
    }


def fetch_risk_exposure(trace_id: str) -> dict | None:
    rel = fetch_relation_explanation(trace_id)
    if not rel:
        return None
    rows: list[dict] = []
    for r in rel.get("relations") or []:
        if r.get("relation") != "EXPOSED_TO":
            continue
        risk_label = r.get("target") if r.get("direction") != "inbound" else r.get("source")
        confidence = float(r.get("confidence") or 0.5)
        rows.append({
            "risk": risk_label,
            "exposure_level": "high" if confidence >= 0.8 else "medium",
            "confidence": confidence,
            "impact": "negative",
            "evidence": list(r.get("evidence") or []),
        })
    return {
        "trace_id": trace_id,
        "center_ticker": rel.get("center_ticker", ""),
        "center_company": rel.get("center_company", ""),
        "risks": rows[:8],
    }


def fetch_market_insight(trace_id: str) -> dict | None:
    result, _, _, center_name, analysis, _, _ = _base_context(trace_id)
    rel = fetch_relation_explanation(trace_id)
    if not result or not rel:
        return None
    key_rel = rel.get("relations")[:5]
    story = (
        f"{center_name} 기준 시장 인텔리전스: "
        + "; ".join(_relation_to_story(r) for r in key_rel)
        if key_rel
        else f"{center_name} 관련 핵심 관계가 부족합니다."
    )
    return {
        "trace_id": trace_id,
        "center_ticker": rel.get("center_ticker", ""),
        "center_company": center_name,
        "market_story": story,
        "bullish": list((analysis.get("bullish_factors") or [])[:4]),
        "bearish": list((analysis.get("bearish_factors") or [])[:4]),
        "key_relations": key_rel,
    }


def fetch_runtime_status(trace_id: str) -> dict | None:
    result = get_unified_result_by_trace(trace_id)
    if not result:
        return None
    trace = get_trace_by_id(trace_id) or {}
    steps = trace.get("steps") or []
    last = steps[-1] if steps else {}
    last_status = (last.get("status") or "").lower()

    if result.get("analysis_result"):
        phase = "analysis_complete"
        label = "Analysis Complete"
    elif steps:
        phase = "runtime_active"
        label = "Runtime Active"
    else:
        phase = "runtime_active"
        label = "Runtime Active"

    if last_status in ("running", "in_progress"):
        phase = "retrieval_running"
        label = "Retrieval Running"

    return {
        "trace_id": trace_id,
        "ticker": result.get("ticker", ""),
        "company_name": parse_company_name(
            result.get("query", ""),
            result.get("ticker", ""),
        ),
        "query": result.get("query", ""),
        "phase": phase,
        "label": label,
        "step_count": len(steps),
        "last_step": last.get("name") or last.get("step") or "",
    }
