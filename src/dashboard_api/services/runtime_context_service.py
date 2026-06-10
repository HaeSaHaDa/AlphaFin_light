"""Runtime context & evidence API service."""
from __future__ import annotations

import json

from .retrieval_service import hydrate_retrieval_chunks
from .trace_service import get_unified_result_by_trace


def fetch_runtime_context_by_trace(trace_id: str) -> dict | None:
    unified = get_unified_result_by_trace(trace_id)
    if not unified:
        return None
    ctx = unified.get("runtime_context")
    if isinstance(ctx, dict) and ctx:
        return ctx
    return _build_fallback_context(unified)


def fetch_runtime_evidence_by_trace(trace_id: str) -> dict | None:
    unified = get_unified_result_by_trace(trace_id)
    if not unified:
        return None
    ctx = fetch_runtime_context_by_trace(trace_id) or {}
    merged = hydrate_retrieval_chunks(unified)
    display_evidence = [_display_evidence(item) for item in merged]
    analysis = unified.get("analysis_result") or {}
    return {
        "trace_id": trace_id,
        "ticker": unified.get("ticker", ""),
        "query": unified.get("query", ""),
        "merged_evidence": display_evidence,
        "reasoning_context": [
            _evidence_label(item) for item in display_evidence
        ],
        "source_breakdown": ctx.get("source_breakdown") or {},
        "has_disclosure": ctx.get("has_disclosure", False),
        "analysis_summary": analysis.get("summary", ""),
        "bullish_factors": analysis.get("bullish_factors", []),
        "bearish_factors": analysis.get("bearish_factors", []),
        "risks": analysis.get("risks", []),
    }


def _metadata(item: dict) -> dict:
    raw = item.get("metadata_json")
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str) or not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def _display_evidence(item: dict) -> dict:
    meta = _metadata(item)
    text = item.get("text") or item.get("chunk_text") or ""
    title = (
        item.get("title")
        or item.get("report_name")
        or meta.get("title")
        or meta.get("report_name")
        or (text.splitlines()[0].strip() if text else "")
    )
    return {
        **item,
        "title": title,
        "text": text,
        "source": meta.get("source") or item.get("source") or "",
        "url": item.get("url") or meta.get("url") or item.get("document_url"),
        "published_at": (
            item.get("published_at")
            or meta.get("published_at")
            or item.get("report_date")
        ),
    }


def _evidence_label(item: dict) -> str:
    kind = "공시" if item.get("document_type") == "disclosure" else "뉴스"
    title = item.get("title") or "제목 없는 문서"
    return f"[{kind}] {title}"


def _build_fallback_context(unified: dict) -> dict:
    """Legacy traces without runtime_context."""
    from src.runtime_query.disclosure_runtime_integration import retrieve_disclosure_runtime
    from src.runtime_query.unified_retrieval_builder import build_unified_retrieval

    ticker = unified.get("ticker", "")
    query = unified.get("query", "")
    from src.runtime_flow.retrieval_executor import execute_retrieval

    news_raw = (
        execute_retrieval(
            query,
            ticker,
            top_k=6,
            document_type="news_article",
        )
        if ticker and query
        else []
    )
    disc = retrieve_disclosure_runtime(ticker, query) if ticker and query else []
    news, disclosure, merged = build_unified_retrieval(
        query,
        ticker,
        news_chunks=news_raw,
        disclosure_chunks=disc,
    )
    from src.runtime_query.runtime_context_assembler import assemble_runtime_context

    return assemble_runtime_context(
        ticker=ticker,
        query=query,
        trace_id=unified.get("trace_id", ""),
        news_chunks=news,
        disclosure_chunks=disclosure,
        merged_evidence=merged,
    )
