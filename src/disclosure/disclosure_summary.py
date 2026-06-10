"""Disclosure summary helpers."""
from __future__ import annotations


def summarize_disclosure_row(row: dict) -> str:
    report = row.get("report_name", "")
    typ = row.get("report_type", "")
    dt = row.get("report_date", "")
    return f"{dt} {typ} {report}".strip()


def build_disclosure_timeline(rows: list[dict], limit: int = 20) -> list[dict]:
    timeline = [
        {
            "report_date": str(r.get("report_date") or ""),
            "report_type": r.get("report_type", ""),
            "title": r.get("report_name", ""),
            "summary": r.get("summary", "") or summarize_disclosure_row(r),
        }
        for r in rows
    ]
    timeline.sort(key=lambda x: x["report_date"], reverse=True)
    return timeline[:limit]
