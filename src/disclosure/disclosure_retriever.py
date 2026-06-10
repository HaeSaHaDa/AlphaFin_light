"""Disclosure retrieval (selectedTicker-centric)."""
from __future__ import annotations

import re
from datetime import datetime

from .disclosure_query_builder import pick_retrieval_candidates


def _tokens(text: str) -> set[str]:
    return {t for t in re.split(r"[\s,./()]+", (text or "").lower()) if len(t) >= 2}


def _score(query: str, chunk: str, importance: float | None = None) -> float:
    q = _tokens(query)
    c = _tokens(chunk)
    if not q or not c:
        return 0.0
    overlap = len(q & c) / max(1, len(q))
    imp = float(importance or 0.5)
    return round(min(1.0, overlap * 0.75 + imp * 0.25), 4)


def _within_date_window(report_date: str | None, max_age_days: int = 365) -> bool:
    if not report_date:
        return False
    try:
        report = datetime.strptime(str(report_date)[:10], "%Y-%m-%d")
    except ValueError:
        return False
    return max(0, (datetime.now() - report).days) <= max_age_days


def retrieve_disclosure_chunks(ticker: str, query: str, top_k: int = 8) -> list[dict]:
    rows = pick_retrieval_candidates(ticker)
    ranked: list[dict] = []
    for r in rows:
        if not _within_date_window(r.get("report_date")):
            continue
        s = _score(query, r.get("chunk_text", ""), r.get("importance_score"))
        if s <= 0:
            continue
        text = r.get("chunk_text") or ""
        ranked.append(
            {
                "chunk_id": r["chunk_id"],
                "document_id": r["document_id"],
                "report_name": r.get("report_name", ""),
                "report_type": r.get("report_type", ""),
                "report_date": str(r.get("report_date") or ""),
                "section_name": r.get("section_name", ""),
                "score": s,
                "text": text,
                "chunk_text": text,
                "ticker": ticker,
                "document_type": "disclosure",
                "source": "disclosure_documents",
            },
        )
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:top_k]
