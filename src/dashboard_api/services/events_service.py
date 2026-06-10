"""Canonical events API service."""
from __future__ import annotations

from src.event_consolidation.event_consolidator import (
    dedupe_retrieval_chunks,
    fetch_events_for_trace,
)
from src.event_consolidation.event_repository import (
    list_events_by_ticker,
    list_evidence_by_event,
)

from .trace_service import get_unified_result_by_trace


def _serialize_event(ev: dict) -> dict:
    return {
        "event_id": ev.get("event_id", ""),
        "trace_id": ev.get("trace_id"),
        "ticker": ev.get("ticker", ""),
        "company_name": ev.get("company_name"),
        "canonical_title": ev.get("canonical_title", ""),
        "event_summary": ev.get("event_summary"),
        "event_type": ev.get("event_type", "market_news"),
        "event_date": str(ev.get("event_date") or ""),
        "confidence_score": float(ev.get("confidence_score") or 0),
        "importance_score": float(ev.get("importance_score") or 0),
        "impact_direction": ev.get("impact_direction", "neutral"),
        "evidence_count": ev.get("evidence_count") or len(ev.get("evidence") or []),
        "evidence": ev.get("evidence") or [],
    }


def fetch_events_by_trace(trace_id: str, *, ticker: str | None = None) -> dict | None:
    if not get_unified_result_by_trace(trace_id):
        return None
    data = fetch_events_for_trace(trace_id, selected_ticker=ticker)
    data["events"] = [_serialize_event(e) for e in data.get("events", [])]
    return data


def fetch_events_by_ticker(ticker: str) -> dict:
    rows = list_events_by_ticker(ticker)
    events = []
    for row in rows:
        ev_id = row["event_id"]
        evidence = list_evidence_by_event(ev_id)
        events.append(_serialize_event({**row, "evidence": evidence, "evidence_count": len(evidence)}))
    if not events:
        return {"ticker": ticker, "event_count": 0, "events": []}
    return {"ticker": ticker, "event_count": len(events), "events": events}


def fetch_event_evidence(event_id: str) -> dict | None:
    evidence = list_evidence_by_event(event_id)
    if not evidence:
        return None
    return {
        "event_id": event_id,
        "evidence_count": len(evidence),
        "evidence": evidence,
    }


def fetch_memory_events(trace_id: str, *, ticker: str | None = None) -> dict | None:
    data = fetch_events_by_trace(trace_id, ticker=ticker)
    if not data:
        return None
    return {
        "trace_id": trace_id,
        "ticker": data.get("ticker", ""),
        "event_count": data.get("event_count", 0),
        "events": data.get("events", []),
        "memory_layers": data.get("memory_layers", []),
    }


def apply_retrieval_dedup(retrieval: dict, trace_id: str, ticker: str | None = None) -> dict:
    """Attach canonical events and dedupe chunks in retrieval payload."""
    ev_data = fetch_events_by_trace(trace_id, ticker=ticker)
    if not ev_data:
        return retrieval
    events = ev_data.get("events", [])
    retrieval = dict(retrieval)
    retrieval["canonical_events"] = events
    retrieval["chunks"] = dedupe_retrieval_chunks(retrieval.get("chunks") or [], events)
    retrieval["chunk_count"] = len(retrieval["chunks"])
    return retrieval
