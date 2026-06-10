"""Event consolidation — news/disclosure/chunk → canonical market events."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from src.dashboard_api.services.trace_service import get_unified_result_by_trace, load_layer_memories

from .canonical_event_builder import (
    build_canonical_title,
    build_event_summary,
    infer_event_type,
    infer_impact_direction,
    make_event_id,
    merge_clusters,
)
from .disclosure_deduplicator import deduplicate_disclosures
from .event_confidence import compute_event_confidence
from .event_importance import compute_event_importance
from .event_memory_manager import assign_memory_layers, dedupe_active_layers
from .event_repository import (
    list_events_by_trace,
    list_evidence_by_event,
    load_chunks_by_ids,
    upsert_market_event,
)
from .news_deduplicator import deduplicate_news

logger = logging.getLogger(__name__)


def _chunk_to_item(chunk: dict, meta: dict | None, ticker: str) -> dict:
    cid = chunk.get("chunk_id")
    m = meta or {}
    metadata: dict = {}
    raw_metadata = chunk.get("metadata_json")
    if isinstance(raw_metadata, dict):
        metadata = raw_metadata
    elif isinstance(raw_metadata, str) and raw_metadata.strip():
        try:
            parsed = json.loads(raw_metadata)
            metadata = parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            metadata = {}
    doc_type = chunk.get("document_type") or m.get("document_type", "news_article")
    source_type = "DISCLOSURE" if doc_type == "disclosure" else "NEWS"
    body = chunk.get("chunk_text") or chunk.get("text") or m.get("body", "")
    title = (
        chunk.get("title")
        or chunk.get("report_name")
        or metadata.get("title")
        or metadata.get("report_name")
        or m.get("title")
        or (body.splitlines()[0].strip() if body else "")
        or f"[{doc_type}] chunk #{cid}"
    )
    return {
        "source_type": source_type,
        "source_id": str(cid),
        "title": title,
        "body": body,
        "url": chunk.get("url") or metadata.get("url"),
        "published_at": chunk.get("published_at") or metadata.get("published_at"),
        "relevance_score": float(chunk.get("score") or 0),
        "ticker": chunk.get("ticker") or ticker,
        "document_type": doc_type,
    }


def _disclosure_chunk_to_item(ch: dict, ticker: str) -> dict:
    return {
        "source_type": "DISCLOSURE",
        "source_id": str(ch.get("chunk_id") or ch.get("document_id") or ""),
        "title": ch.get("section_name") or ch.get("title") or "공시",
        "body": (ch.get("chunk_text") or "")[:500],
        "url": ch.get("document_url"),
        "published_at": ch.get("report_date"),
        "relevance_score": float(ch.get("score") or ch.get("importance_score") or 0.8),
        "ticker": ticker,
        "document_type": "disclosure",
    }


def extract_raw_items(unified: dict, disclosure_evidence: list[dict] | None = None) -> list[dict]:
    ticker = (unified.get("ticker") or "").strip()
    analysis = unified.get("analysis_result") or {}
    chunks = analysis.get("referenced_chunks") or []
    runtime_context = unified.get("runtime_context") or {}
    merged_evidence = runtime_context.get("merged_evidence") or []
    evidence_by_key = {
        (item.get("chunk_id"), item.get("document_type")): item
        for item in merged_evidence
        if isinstance(item, dict)
    }
    chunks = [
        {
            **evidence_by_key.get(
                (chunk.get("chunk_id"), chunk.get("document_type")),
                {},
            ),
            **chunk,
        }
        for chunk in chunks
    ]
    chunk_ids = [int(c["chunk_id"]) for c in chunks if c.get("chunk_id") is not None]
    meta_map = load_chunks_by_ids(chunk_ids)

    items: list[dict] = []
    for ch in chunks:
        cid = ch.get("chunk_id")
        meta = meta_map.get(int(cid)) if cid is not None else None
        items.append(_chunk_to_item(ch, meta, ticker))

    for ch in disclosure_evidence or []:
        items.append(_disclosure_chunk_to_item(ch, ticker))

    return items


def consolidate_events(
    trace_id: str,
    *,
    persist: bool = True,
    selected_ticker: str | None = None,
) -> dict:
    unified = get_unified_result_by_trace(trace_id)
    if not unified:
        return {"trace_id": trace_id, "events": [], "event_count": 0}

    ticker = (selected_ticker or unified.get("ticker") or "").strip()
    disclosure_evidence: list[dict] = []
    runtime_ctx = unified.get("runtime_context") or {}
    if isinstance(runtime_ctx, dict) and runtime_ctx.get("disclosure_chunks"):
        disclosure_evidence = runtime_ctx.get("disclosure_chunks") or []
    else:
        try:
            from src.dashboard_api.services.disclosure_service import fetch_disclosure_evidence

            ev = fetch_disclosure_evidence(trace_id)
            if ev:
                disclosure_evidence = ev.get("evidence") or []
        except Exception:
            logger.debug("disclosure evidence skip", exc_info=True)

    raw = extract_raw_items(unified, disclosure_evidence)
    if ticker:
        raw = [r for r in raw if not r.get("ticker") or r.get("ticker") == ticker]

    news = deduplicate_news(raw)
    disc = deduplicate_disclosures(raw)
    merged_items = news + [d for d in disc if d not in news]

    clusters = merge_clusters(merged_items)
    events: list[dict] = []
    for cluster in clusters:
        canonical = build_canonical_title(cluster, unified.get("company_name", ""))
        eid = make_event_id(ticker, canonical)
        evidence = [
            {
                "source_type": c.get("source_type", "CHUNK"),
                "source_id": c.get("source_id"),
                "title": c.get("title"),
                "url": c.get("url"),
                "published_at": c.get("published_at"),
                "relevance_score": c.get("relevance_score"),
            }
            for c in cluster
        ]
        conf = compute_event_confidence(evidence)
        imp = compute_event_importance(evidence, confidence=conf)
        event = {
            "event_id": eid,
            "trace_id": trace_id,
            "ticker": ticker,
            "company_name": unified.get("company_name", ""),
            "canonical_title": canonical,
            "event_summary": build_event_summary(cluster, canonical),
            "event_type": infer_event_type(cluster),
            "event_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "confidence_score": conf,
            "importance_score": imp,
            "impact_direction": infer_impact_direction(cluster),
            "evidence": evidence,
            "evidence_count": len(evidence),
        }
        events.append(event)
        if persist:
            try:
                upsert_market_event(event, evidence)
            except Exception:
                logger.warning("event persist skip  %s", eid, exc_info=True)

    layered = {
        "short_term": load_layer_memories("short_term"),
        "mid_term": load_layer_memories("mid_term"),
        "long_term": load_layer_memories("long_term"),
    }
    memory_layers = assign_memory_layers(events, layered, persist=persist)
    memory_layers = dedupe_active_layers(memory_layers)

    events.sort(key=lambda e: e.get("confidence_score", 0), reverse=True)
    return {
        "trace_id": trace_id,
        "ticker": ticker,
        "query": unified.get("query", ""),
        "event_count": len(events),
        "events": events,
        "memory_layers": memory_layers,
        "dedup_stats": {
            "raw_items": len(raw),
            "after_news_dedup": len(news),
            "after_disclosure_dedup": len(disc),
            "canonical_events": len(events),
        },
    }


def fetch_events_for_trace(trace_id: str, *, selected_ticker: str | None = None) -> dict:
    cached = list_events_by_trace(trace_id)
    if cached:
        unified = get_unified_result_by_trace(trace_id) or {}
        runtime_context = unified.get("runtime_context") or {}
        disclosure_evidence = runtime_context.get("disclosure_chunks") or []
        raw_by_source = {
            str(item.get("source_id")): item
            for item in extract_raw_items(unified, disclosure_evidence)
            if item.get("source_id") is not None
        }
        events = []
        for row in cached:
            ev_id = row["event_id"]
            evidence = list_evidence_by_event(ev_id)
            source_items: list[dict] = []
            hydrated_evidence: list[dict] = []
            for item in evidence:
                source = raw_by_source.get(str(item.get("source_id")))
                if source:
                    source_items.append(source)
                    item = {
                        **item,
                        "title": source.get("title") or item.get("title"),
                        "url": source.get("url") or item.get("url"),
                        "published_at": (
                            source.get("published_at") or item.get("published_at")
                        ),
                    }
                hydrated_evidence.append(item)
            summary = row.get("event_summary")
            if source_items:
                summary = build_event_summary(
                    source_items,
                    row.get("canonical_title", ""),
                )
            events.append({
                **row,
                "event_summary": summary,
                "evidence": hydrated_evidence,
                "evidence_count": len(hydrated_evidence),
            })
        if selected_ticker:
            events = [e for e in events if e.get("ticker") == selected_ticker]
        if events:
            return {
                "trace_id": trace_id,
                "ticker": events[0].get("ticker", ""),
                "event_count": len(events),
                "events": events,
                "from_cache": True,
            }
    return consolidate_events(trace_id, selected_ticker=selected_ticker)


def dedupe_retrieval_chunks(chunks: list[dict], events: list[dict]) -> list[dict]:
    """Filter retrieval chunks already represented in canonical events."""
    if not events or not chunks:
        return chunks
    titles = [e.get("canonical_title", "") for e in events]
    from .event_similarity import title_similarity

    out: list[dict] = []
    for ch in chunks:
        preview = ch.get("chunk_preview") or ch.get("title") or ""
        if any(title_similarity(preview, t) > 0.85 for t in titles):
            continue
        out.append(ch)
    return out if out else chunks[:3]


if __name__ == "__main__":
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    logging.basicConfig(level=logging.INFO)
    tid = sys.argv[1] if len(sys.argv) > 1 else ""
    if not tid:
        print("Usage: python -m src.event_consolidation.event_consolidator <trace_id>")
        sys.exit(1)
    result = consolidate_events(tid, persist=False)
    print(f"events={result['event_count']}  dedup={result.get('dedup_stats')}")
