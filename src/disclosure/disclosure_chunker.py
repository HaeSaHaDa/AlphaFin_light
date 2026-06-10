"""Disclosure chunking."""
from __future__ import annotations

import re

from .disclosure_query_builder import build_section_name
from .disclosure_repository import (
    list_disclosures_for_chunking,
    sync_disclosure_document_chunks,
)

_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def _split_text(text: str, max_chars: int = 900) -> list[str]:
    t = (text or "").strip()
    if not t:
        return []
    out: list[str] = []
    cur = ""
    for paragraph in [part.strip() for part in re.split(r"\n{1,}", t) if part.strip()]:
        if len(cur) + len(paragraph) + 1 > max_chars and cur:
            out.append(cur.strip())
            cur = ""
        if len(paragraph) > max_chars:
            for start in range(0, len(paragraph), max_chars):
                piece = paragraph[start:start + max_chars]
                if cur:
                    out.append(cur.strip())
                    cur = ""
                out.append(piece)
            continue
        cur = f"{cur}\n{paragraph}".strip()
    if cur:
        out.append(cur)
    return out


def _split_sections(text: str) -> list[tuple[str, str]]:
    matches = list(_SECTION_RE.finditer(text or ""))
    if not matches:
        return [("본문", (text or "").strip())] if (text or "").strip() else []

    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            sections.append((match.group(1).strip()[:120], body))
    return sections


def chunk_disclosure_documents(ticker: str) -> dict:
    docs = list_disclosures_for_chunking(ticker, limit=120)
    synced_chunks = 0
    generated_chunks = 0
    body_documents = 0
    for d in docs:
        text = d.get("raw_text") or d.get("summary") or d.get("report_name") or ""
        has_body = bool(
            d.get("raw_text")
            and (d.get("raw_text") or "").strip() != (d.get("report_name") or "").strip()
        )
        if has_body:
            body_documents += 1
        rows: list[dict] = []
        chunk_index = 0
        if not has_body:
            for chunk in _split_text(text, max_chars=500):
                rows.append(
                    {
                        "document_id": d["document_id"],
                        "chunk_index": chunk_index,
                        "chunk_text": chunk,
                        "section_name": build_section_name(chunk),
                        "importance_score": round(
                            min(1.0, 0.4 + len(chunk) / 1200),
                            3,
                        ),
                    },
                )
                chunk_index += 1
            generated_chunks += len(rows)
            synced_chunks += sync_disclosure_document_chunks(d["document_id"], rows)
            continue

        for section_name, section_text in _split_sections(text):
            for chunk in _split_text(section_text):
                content = (
                    f"{d.get('report_name') or ''}\n"
                    f"[{section_name}]\n"
                    f"{chunk}"
                ).strip()
                rows.append(
                    {
                        "document_id": d["document_id"],
                        "chunk_index": chunk_index,
                        "chunk_text": content,
                        "section_name": section_name,
                        "importance_score": round(
                            min(1.0, 0.45 + len(chunk) / 1800),
                            3,
                        ),
                    },
                )
                chunk_index += 1
        generated_chunks += len(rows)
        synced_chunks += sync_disclosure_document_chunks(d["document_id"], rows)

    return {
        "status": "completed",
        "ticker": ticker,
        "chunks": synced_chunks,
        "raw_rows": generated_chunks,
        "body_documents": body_documents,
    }
