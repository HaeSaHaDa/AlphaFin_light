"""Retrieval API service."""
from __future__ import annotations

import json
import logging

from .trace_service import get_latest_unified_result, get_unified_result_by_trace

logger = logging.getLogger(__name__)


def fetch_latest_retrieval() -> dict | None:
    result = get_latest_unified_result()
    if not result:
        return None
    return _build_retrieval_payload(result)


def fetch_retrieval_by_trace(trace_id: str) -> dict | None:
    result = get_unified_result_by_trace(trace_id)
    if not result:
        return None
    return _build_retrieval_payload(result)


def _parse_metadata(chunk: dict) -> dict:
    metadata = chunk.get("metadata_json")
    if isinstance(metadata, dict):
        return metadata
    if not isinstance(metadata, str) or not metadata.strip():
        return {}
    try:
        parsed = json.loads(metadata)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def hydrate_retrieval_chunks(unified: dict) -> list[dict]:
    analysis = unified.get("analysis_result") or {}
    referenced = analysis.get("referenced_chunks") or []
    runtime_context = unified.get("runtime_context") or {}
    evidence = runtime_context.get("merged_evidence") or []
    if not evidence:
        return referenced

    evidence_by_key = {
        (item.get("chunk_id"), item.get("document_type")): item
        for item in evidence
        if isinstance(item, dict)
    }
    hydrated: list[dict] = []
    for chunk in referenced:
        source = evidence_by_key.get(
            (chunk.get("chunk_id"), chunk.get("document_type")),
        )
        item = {**source, **chunk} if source else dict(chunk)
        metadata = _parse_metadata(item)
        text = item.get("text") or item.get("chunk_text") or ""
        title = (
            item.get("title")
            or item.get("report_name")
            or metadata.get("title")
            or metadata.get("report_name")
            or (text.splitlines()[0].strip() if text else "")
        )
        hydrated.append({
            **item,
            "title": title.strip() if isinstance(title, str) else title,
            "text": text,
            "source": metadata.get("source") or item.get("source") or "",
            "url": item.get("url") or metadata.get("url") or item.get("document_url"),
            "published_at": (
                item.get("published_at")
                or metadata.get("published_at")
                or item.get("report_date")
            ),
        })
    return hydrated


def _enrich_chunks(chunks: list[dict]) -> list[dict]:
    ranked = sorted(chunks, key=lambda chunk: chunk.get("score", 0), reverse=True)
    enriched: list[dict] = []
    for rank, chunk in enumerate(ranked, start=1):
        doc_type = chunk.get("document_type", "unknown")
        chunk_id = chunk.get("chunk_id", "")
        ticker = chunk.get("ticker", "")
        metadata = _parse_metadata(chunk)
        text = (
            chunk.get("text")
            or chunk.get("chunk_text")
            or metadata.get("body")
            or ""
        )
        title = (
            chunk.get("title")
            or chunk.get("report_name")
            or metadata.get("title")
            or metadata.get("report_name")
            or (text.splitlines()[0].strip() if text else "")
        )
        enriched.append({
            **chunk,
            "rank": rank,
            "source_file": f"data/processed/{doc_type}/chunk_{chunk_id}.json",
            "title": title,
            "text": text,
            "url": (
                chunk.get("url")
                or metadata.get("url")
                or chunk.get("document_url")
            ),
            "published_at": (
                chunk.get("published_at")
                or metadata.get("published_at")
                or chunk.get("report_date")
            ),
            "source": metadata.get("source") or chunk.get("source") or "",
            "chunk_preview": title or f"[{doc_type}] chunk #{chunk_id}",
            "related_entity": ticker or "",
        })
    return enriched


def _build_retrieval_payload(unified: dict) -> dict:
    analysis = unified.get("analysis_result", {})
    eval_result = unified.get("evaluation_result", {})
    chunks = _enrich_chunks(hydrate_retrieval_chunks(unified))
    trace_id = unified.get("trace_id", "")
    ticker = unified.get("ticker", "") or ""
    runtime_context = unified.get("runtime_context") or {}

    payload = {
        "trace_id": trace_id,
        "query": unified.get("query", ""),
        "ticker": ticker,
        "chunk_count": len(chunks) or unified.get("retrieval_chunk_count", 0),
        "chunks": chunks,
        "retrieval_quality": eval_result.get("retrieval_quality", {}),
        "context_usage": eval_result.get("context_usage", {}),
        "unified_context_length": unified.get("unified_context_length", 0),
        "retrieval_timestamp": unified.get("completed_at", ""),
        "freshness": runtime_context.get("freshness", {}),
        "analysis": {
            "summary": analysis.get("summary", ""),
            "bullish_factors": analysis.get("bullish_factors", []),
            "bearish_factors": analysis.get("bearish_factors", []),
            "risks": analysis.get("risks", []),
            "model": analysis.get("model", ""),
        },
        "context_layers": {
            "retrieval": {
                "chunk_count": len(chunks),
                "context_length": unified.get("unified_context_length", 0),
            },
            "memory": unified.get("memory_updates", {}),
            "reflection": unified.get("reflection_result", {}),
            "stock_chain": unified.get("stock_chain", {}),
            "temporal": unified.get("temporal_result", {}),
        },
    }
    if trace_id:
        try:
            from .events_service import apply_retrieval_dedup

            payload = apply_retrieval_dedup(payload, trace_id, ticker=ticker or None)
        except Exception:
            logger.debug("retrieval event dedup skip", exc_info=True)
    return payload
