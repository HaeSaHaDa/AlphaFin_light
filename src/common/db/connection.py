"""MariaDB 연결 유틸리티."""
from __future__ import annotations

import logging
import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

_ENV_LOADED = False


def _load_env() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    env_path = Path(__file__).resolve().parents[3] / ".env"
    load_dotenv(env_path)
    _ENV_LOADED = True


def get_connection() -> pymysql.Connection:
    """.env 기반으로 MariaDB 연결을 생성하여 반환한다.

    Returns:
        pymysql.Connection 객체.

    Raises:
        ValueError: 필수 환경 변수가 누락된 경우.
        pymysql.Error: DB 연결 실패 시.
    """
    _load_env()

    host = os.getenv("DB_HOST", "").strip()
    port = os.getenv("DB_PORT", "").strip()
    name = os.getenv("DB_NAME", "").strip()
    user = os.getenv("DB_USER", "").strip()
    password = os.getenv("DB_PASSWORD", "").strip()

    missing = []
    if not host:
        missing.append("DB_HOST")
    if not name:
        missing.append("DB_NAME")
    if not user:
        missing.append("DB_USER")

    if missing:
        raise ValueError(f".env에 필수 DB 설정 누락: {', '.join(missing)}")

    conn = pymysql.connect(
        host=host,
        port=int(port) if port else 3306,
        database=name,
        user=user,
        password=password,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
    logger.info("MariaDB 연결 성공  host=%s  db=%s", host, name)
    return conn
