"""OpenDART disclosure collector for Disclosure Store."""
from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta

from src.collectors.opendart.collector import fetch_disclosures, load_api_key
from src.company_resolver.company_resolver import resolve_company

from .disclosure_body_collector import fetch_disclosure_body
from .disclosure_query_builder import classify_report_type
from .disclosure_repository import upsert_disclosure_documents

logger = logging.getLogger(__name__)


def collect_disclosures(
    ticker: str,
    *,
    corp_code: str | None = None,
    company_name: str | None = None,
    days: int = 365,
    body_limit: int = 10,
) -> dict:
    resolved = None
    if (not corp_code or not company_name) and ticker:
        resolved = resolve_company(ticker)
    corp = corp_code or (resolved.corp_code if resolved else "")
    name = company_name or (resolved.company_name if resolved else ticker)
    if not corp:
        return {"status": "failed", "error": "corp_code를 찾을 수 없습니다.", "ticker": ticker}

    end = datetime.now()
    begin = end - timedelta(days=days)
    data = fetch_disclosures(corp, begin.strftime("%Y%m%d"), end.strftime("%Y%m%d"))
    if data.get("status") not in (None, "", "000"):
        return {
            "status": "failed",
            "error": data.get("message", "OpenDART 공시 목록 조회 실패"),
            "dart_status": data.get("status", ""),
            "ticker": ticker,
            "corp_code": corp,
            "company_name": name,
            "fetched": 0,
        }
    items = data.get("list") or []
    body_api_key = load_api_key() if items and body_limit > 0 else None
    rows: list[dict] = []
    body_fetched = 0
    body_failed = 0
    body_chars = 0
    for index, it in enumerate(items):
        report_name = it.get("report_nm", "")
        report_type, source_type = classify_report_type(report_name)
        receipt_no = it.get("rcept_no", "")
        raw_date = it.get("rcept_dt") or ""
        report_date = (
            f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
            if len(raw_date) == 8
            else None
        )
        disclosure_body = None
        body_files: list[str] = []
        if index < max(0, body_limit) and receipt_no:
            try:
                body_result = fetch_disclosure_body(
                    receipt_no,
                    api_key=body_api_key,
                )
                disclosure_body = body_result.get("disclosure_body") or None
                body_files = body_result.get("source_files") or []
                if disclosure_body:
                    body_fetched += 1
                    body_chars += len(disclosure_body)
            except Exception:
                body_failed += 1
                logger.warning(
                    "OpenDART body collection failed  receipt_no=%s",
                    receipt_no,
                    exc_info=True,
                )
            if index + 1 < min(len(items), max(0, body_limit)):
                time.sleep(0.15)

        metadata = {
            **it,
            "body_collected": bool(disclosure_body),
            "body_source_files": body_files,
        }
        rows.append(
            {
                "ticker": ticker,
                "corp_code": corp,
                "company_name": name,
                "report_name": report_name,
                "report_type": report_type,
                "report_date": report_date,
                "source_type": source_type,
                "document_url": f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={it.get('rcept_no','')}",
                "summary": "",
                "raw_text": disclosure_body,
                "receipt_no": receipt_no,
                "metadata_json": metadata,
            },
        )

    inserted = upsert_disclosure_documents(rows)
    logger.info("collect_disclosures  ticker=%s  fetched=%d  upsert=%d", ticker, len(rows), inserted)
    return {
        "status": "completed",
        "ticker": ticker,
        "corp_code": corp,
        "company_name": name,
        "fetched": len(rows),
        "upserted": inserted,
        "body_fetched": body_fetched,
        "body_failed": body_failed,
        "body_chars": body_chars,
    }


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--body-limit", type=int, default=10)
    args = ap.parse_args()
    print(collect_disclosures(args.ticker, days=args.days, body_limit=args.body_limit))
