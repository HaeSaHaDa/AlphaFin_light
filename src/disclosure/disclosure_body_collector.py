"""OpenDART disclosure body download and text extraction."""
from __future__ import annotations

import io
import logging
import re
import zipfile

import requests
from bs4 import BeautifulSoup

from src.collectors.opendart.collector import load_api_key

logger = logging.getLogger(__name__)

OPENDART_DOCUMENT_URL = "https://opendart.fss.or.kr/api/document.xml"
REQUEST_TIMEOUT_SEC = 30

_HEADING_TAGS = {
    "cover-title",
    "document-name",
    "section-title",
    "title",
}
_TEXT_TAGS = {"p", "li"}
_SPACE_RE = re.compile(r"[ \t\r\f\v]+")


def _normalize_text(value: str) -> str:
    lines = []
    for raw_line in (value or "").splitlines():
        line = _SPACE_RE.sub(" ", raw_line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def _decode_markup(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "euc-kr", "cp949"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _is_heading(node) -> bool:
    name = (node.name or "").lower()
    return name in _HEADING_TAGS or str(node.get("atoc") or "").upper() == "Y"


def _append_line(lines: list[str], value: str) -> None:
    text = _normalize_text(value)
    if text and (not lines or lines[-1] != text):
        lines.append(text)


def extract_disclosure_sections(markup: str) -> list[dict[str, str]]:
    """Extract headings, paragraphs, and table rows from DART XML/HTML."""
    soup = BeautifulSoup(markup or "", "lxml-xml")
    if not soup.find():
        soup = BeautifulSoup(markup or "", "html.parser")

    for tag in soup.find_all(["script", "style"]):
        tag.decompose()

    sections: list[dict[str, str]] = []
    section_name = "본문"
    lines: list[str] = []

    def flush() -> None:
        nonlocal lines
        text = "\n".join(lines).strip()
        if text:
            sections.append({"section_name": section_name[:120], "text": text})
        lines = []

    for node in soup.find_all(True):
        name = (node.name or "").lower()
        if _is_heading(node):
            heading = _normalize_text(node.get_text(" ", strip=True))
            if heading:
                flush()
                section_name = heading
            continue
        if name == "tr":
            cells = [
                _normalize_text(cell.get_text(" ", strip=True))
                for cell in node.find_all(True)
                if (cell.name or "").lower() in {"th", "td"}
            ]
            _append_line(lines, " | ".join(cell for cell in cells if cell))
            continue
        if name in _TEXT_TAGS and node.find_parent("tr") is None:
            _append_line(lines, node.get_text(" ", strip=True))

    flush()
    if sections:
        return sections

    fallback = _normalize_text(soup.get_text("\n", strip=True))
    return [{"section_name": "본문", "text": fallback}] if fallback else []


def build_disclosure_body(sections: list[dict[str, str]]) -> str:
    parts = []
    for section in sections:
        name = (section.get("section_name") or "본문").strip()
        text = (section.get("text") or "").strip()
        if text:
            parts.append(f"## {name}\n{text}")
    return "\n\n".join(parts)


def fetch_disclosure_body(
    receipt_no: str,
    *,
    api_key: str | None = None,
    timeout: int = REQUEST_TIMEOUT_SEC,
) -> dict:
    """Download a disclosure archive and return cleaned body text."""
    receipt = (receipt_no or "").strip()
    if not receipt:
        raise ValueError("receipt_no is required")

    response = requests.get(
        OPENDART_DOCUMENT_URL,
        params={
            "crtfc_key": api_key or load_api_key(),
            "rcept_no": receipt,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    if not zipfile.is_zipfile(io.BytesIO(response.content)):
        message = _normalize_text(response.text)[:300]
        raise ValueError(f"OpenDART document response is not a ZIP: {message}")

    sections: list[dict[str, str]] = []
    source_files: list[str] = []
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        for name in sorted(archive.namelist()):
            if name.endswith("/") or not name.lower().endswith((".xml", ".html", ".htm")):
                continue
            source_files.append(name)
            sections.extend(extract_disclosure_sections(_decode_markup(archive.read(name))))

    body = build_disclosure_body(sections)
    logger.info(
        "OpenDART body collected  receipt_no=%s  files=%d  sections=%d  chars=%d",
        receipt,
        len(source_files),
        len(sections),
        len(body),
    )
    return {
        "receipt_no": receipt,
        "disclosure_body": body,
        "sections": sections,
        "source_files": source_files,
    }
