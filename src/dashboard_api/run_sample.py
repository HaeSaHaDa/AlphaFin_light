"""Dashboard API 샘플 검증 (TestClient)."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from src.dashboard_api.app import app

ENDPOINTS = [
    "/api/retrieval/latest",
    "/api/reflection/latest",
    "/api/memory/latest",
    "/api/stock-chain/latest",
    "/api/trace/latest",
    "/api/evaluation/latest",
    "/health",
    "/docs",
]


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Dashboard API 검증 시작 ===")
    client = TestClient(app)

    checks: dict[str, bool] = {}

    for path in ENDPOINTS:
        resp = client.get(path)
        ok = resp.status_code == 200
        checks[path] = ok
        logger.info("  GET %-30s : %s (%d)", path, "OK" if ok else "FAIL", resp.status_code)

    eval_data = client.get("/api/evaluation/latest").json()
    checks["has_overall_score"] = eval_data.get("overall_score") is not None
    checks["has_trace_id"] = bool(eval_data.get("trace_id"))

    refl = client.get("/api/reflection/latest").json()
    checks["has_missing_risks"] = "missing_risks" in refl

    for name, ok in checks.items():
        if name not in [e for e in ENDPOINTS]:
            logger.info("  %-30s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Dashboard API 검증 완료 ===")
    logger.info("실행: uvicorn src.dashboard_api.app:app --host 0.0.0.0 --port 8000")
    logger.info("Swagger: http://localhost:8000/docs")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
