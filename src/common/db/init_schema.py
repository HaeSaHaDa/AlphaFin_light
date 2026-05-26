"""database/schema.sql을 실행하여 초기 테이블을 생성한다."""
from __future__ import annotations

import logging
from pathlib import Path

from connection import get_connection

logger = logging.getLogger(__name__)

SCHEMA_PATH = Path(__file__).resolve().parents[3] / "database" / "schema.sql"


def initialize_database() -> bool:
    """schema.sql을 읽어 MariaDB에 실행한다.

    Returns:
        True: 성공, False: 실패.
    """
    if not SCHEMA_PATH.exists():
        logger.error("schema.sql 파일을 찾을 수 없습니다: %s", SCHEMA_PATH)
        return False

    sql_text = SCHEMA_PATH.read_text(encoding="utf-8")

    lines_no_comments = [
        line for line in sql_text.splitlines()
        if not line.strip().startswith("--")
    ]
    clean_sql = "\n".join(lines_no_comments)

    statements = [
        s.strip() for s in clean_sql.split(";") if s.strip()
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for stmt in statements:
                if not stmt:
                    continue
                cursor.execute(stmt)
                logger.debug("실행 완료: %s...", stmt[:60])
        conn.commit()
        logger.info("schema.sql 실행 완료  (%d개 구문)", len(statements))
        return True
    except Exception:
        conn.rollback()
        logger.exception("schema.sql 실행 실패")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    ok = initialize_database()
    if ok:
        logger.info("=== DB 초기화 성공 ===")
    else:
        logger.error("=== DB 초기화 실패 ===")
