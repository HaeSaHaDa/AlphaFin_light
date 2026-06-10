"""Assemble unified runtime context payload."""
from __future__ import annotations

from .runtime_evidence_merger import build_reasoning_context, source_breakdown


def assemble_runtime_context(
    *,
    ticker: str,
    query: str,
    trace_id: str = "",
    news_chunks: list[dict],
    disclosure_chunks: list[dict],
    merged_evidence: list[dict],
    collect_status: str = "",
    freshness: dict | None = None,
    keywords: list[str] | None = None,
) -> dict:
    breakdown = source_breakdown(merged_evidence)
    return {
        "trace_id": trace_id,
        "ticker": ticker,
        "query": query,
        "keywords": keywords or [],
        "news_chunks": news_chunks,
        "disclosure_chunks": disclosure_chunks,
        "merged_evidence": merged_evidence,
        "reasoning_context": build_reasoning_context(merged_evidence),
        "source_breakdown": breakdown,
        "disclosure_collect_status": collect_status,
        "has_disclosure": breakdown.get("DISCLOSURE", 0) > 0,
        "disclosure_priority": "HIGH" if breakdown.get("DISCLOSURE", 0) > 0 else "NONE",
        "freshness": freshness or {},
    }
