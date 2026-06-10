"""Merge news + disclosure runtime evidence with source priority."""
from __future__ import annotations

from .disclosure_retrieval_ranker import SOURCE_PRIORITY


def _source_weight(chunk: dict) -> float:
    doc = (chunk.get("document_type") or "").lower()
    if doc == "disclosure":
        return SOURCE_PRIORITY["DISCLOSURE"]
    src = (chunk.get("source") or "").lower()
    if "disclosure" in src:
        return SOURCE_PRIORITY["DISCLOSURE"]
    if doc == "news_article":
        return SOURCE_PRIORITY["NEWS"]
    return SOURCE_PRIORITY.get("CHUNK", 0.6)


def _merge_score(chunk: dict) -> float:
    rel = float(chunk.get("score") or chunk.get("rank_score") or 0)
    return round(min(1.0, rel * 0.7 + _source_weight(chunk) * 0.3), 4)


def merge_runtime_evidence(
    news_chunks: list[dict],
    disclosure_chunks: list[dict],
    *,
    max_items: int = 12,
) -> list[dict]:
    merged: list[dict] = []
    seen: set[str] = set()

    for ch in disclosure_chunks + news_chunks:
        key = f"{ch.get('document_type')}:{ch.get('chunk_id')}"
        if key in seen:
            continue
        seen.add(key)
        item = {
            **ch,
            "merge_score": _merge_score(ch),
            "source_priority": "HIGH" if _source_weight(ch) >= 0.9 else "MEDIUM",
        }
        merged.append(item)

    merged.sort(key=lambda x: x.get("merge_score", 0), reverse=True)
    return merged[:max_items]


def build_reasoning_context(merged: list[dict], limit: int = 8) -> list[str]:
    lines: list[str] = []
    for ch in merged[:limit]:
        doc = ch.get("document_type", "chunk")
        label = "공시" if doc == "disclosure" else "뉴스"
        title = ch.get("report_name") or ch.get("section_name") or ch.get("text", "")[:80]
        if not title:
            title = f"chunk #{ch.get('chunk_id', '?')}"
        lines.append(f"[{label}] {title}")
    return lines


def source_breakdown(merged: list[dict]) -> dict[str, int]:
    counts = {"DISCLOSURE": 0, "NEWS": 0, "OTHER": 0}
    for ch in merged:
        doc = (ch.get("document_type") or "").lower()
        if doc == "disclosure":
            counts["DISCLOSURE"] += 1
        elif doc == "news_article":
            counts["NEWS"] += 1
        else:
            counts["OTHER"] += 1
    return counts
