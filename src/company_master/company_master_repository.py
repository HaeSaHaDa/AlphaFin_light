"""company_master DB CRUD."""
from __future__ import annotations

import json
import logging
from typing import Any

from src.common.db.connection import get_connection

logger = logging.getLogger(__name__)


def ensure_table() -> None:
    from pathlib import Path

    sql_path = Path(__file__).resolve().parents[2] / "database" / "schema_company_master.sql"
    if not sql_path.exists():
        return
    ddl = sql_path.read_text(encoding="utf-8")
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for stmt in ddl.split(";"):
                s = stmt.strip()
                if s:
                    cur.execute(s)
        conn.commit()
    finally:
        conn.close()


def upsert_master_row(row: dict[str, Any]) -> None:
    aliases = row.get("aliases") or []
    if isinstance(aliases, list):
        aliases_json = json.dumps(aliases, ensure_ascii=False)
    else:
        aliases_json = aliases

    sql = """
        INSERT INTO company_master
            (ticker, company_name, market, corp_code, sector, industry, aliases)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            company_name = VALUES(company_name),
            market = VALUES(market),
            corp_code = COALESCE(VALUES(corp_code), corp_code),
            sector = VALUES(sector),
            industry = VALUES(industry),
            aliases = VALUES(aliases)
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (
                row["ticker"],
                row["company_name"],
                row.get("market", "KOSPI"),
                row.get("corp_code"),
                row.get("sector"),
                row.get("industry"),
                aliases_json,
            ))
        conn.commit()
    finally:
        conn.close()


def get_by_ticker(ticker: str) -> dict | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM company_master WHERE ticker = %s LIMIT 1",
                (ticker,),
            )
            row = cur.fetchone()
    finally:
        conn.close()
    return _row_to_dict(row) if row else None


def list_all(limit: int = 500) -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM company_master ORDER BY company_name LIMIT %s",
                (limit,),
            )
            rows = cur.fetchall()
    finally:
        conn.close()
    return [_row_to_dict(r) for r in rows]


def _row_to_dict(row: dict) -> dict:
    aliases = row.get("aliases")
    if isinstance(aliases, str):
        try:
            aliases = json.loads(aliases)
        except json.JSONDecodeError:
            aliases = []
    return {
        "ticker": row.get("ticker", ""),
        "company_name": row.get("company_name", ""),
        "market": row.get("market", ""),
        "corp_code": row.get("corp_code", ""),
        "sector": row.get("sector", ""),
        "industry": row.get("industry", ""),
        "aliases": aliases or [],
    }
