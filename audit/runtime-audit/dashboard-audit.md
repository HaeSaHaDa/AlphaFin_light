# Dashboard Runtime Audit

## 기준

모든 패널은 **동일 traceId** + **selectedTicker** Runtime 실행 결과만 표시.

| 패널 | 바인딩 | 상태 |
|------|--------|------|
| Signal | `GET /api/signal/{traceId}` via RuntimeQueryProvider | OK |
| News | `data.retrieval.chunks` 동일 trace | OK |
| Event Graph | `GET /api/stock-chain/{traceId}` | OK |
| Memory | `GET /api/memory/{traceId}` (query/ticker 필터) | OK |
| Evaluation | `GET /api/evaluation/{traceId}` | OK |
| Reflection | `GET /api/reflection/{traceId}` | OK |
| Retrieval | `GET /api/retrieval/{traceId}` | OK |
| Stock Chain | `GET /api/stock-chain/{traceId}` | OK |

## 제거·수정 (TASK-036)

- Stock Chain viewer: NVIDIA/삼성전자 **preferred** 하드코드 제거 → ticker entity links
- Engine timeline: **DEMO_FLOW** 제거
- Event graph layout: NVIDIA seed root → **payload.ticker/query**
- Graph toolbar: HIGHLIGHT_PRESETS → **runtime entities**
- Explainability/Accuracy: "(샘플)" 라벨 제거

## 잔여 주의

- trace 파일 없을 때 `/api/trace/{id}`는 unified summary만 반환 (동일 trace_id, cross-trace 아님)
- Stock chain 엔진 출력에 타 종목 entity가 섞일 수 있음 → API **ticker 필터** 적용됨
