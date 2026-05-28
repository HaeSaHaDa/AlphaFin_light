# API Audit

## traceId 필수 (Dashboard UI)

| Endpoint | trace별 payload |
|----------|-----------------|
| GET /api/trace/{traceId} | OK |
| GET /api/retrieval/{traceId} | OK |
| GET /api/reflection/{traceId} | OK |
| GET /api/memory/{traceId} | OK (query/ticker filter) |
| GET /api/stock-chain/{traceId} | OK (ticker filter) |
| GET /api/evaluation/{traceId} | OK |
| GET /api/signal/{traceId} | OK |
| POST /api/query/run | OK |

## /latest 비활성 (TASK-036)

모든 `GET /api/*/latest` → **400** + trace_id 사용 안내.

레거시: `run_sample.py`는 dev 전용, /latest 호출 시 실패.
