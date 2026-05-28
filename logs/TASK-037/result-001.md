# TASK-037 결과

## 구현 요약

### Backend
- `GET /api/market-graph/{trace_id}` — `build_ticker_centric_chain` + 분석 risks/themes → Market Relationship Graph
- `GET /api/runtime-status/{trace_id}` — Runtime phase/label

### Frontend
- `dashboard-ui/src/market-graph/*` — builder, filter, score, relation-extractor, legend, tooltip
- `components/market-graph/*` — MarketRelationshipGraph, legend, toolbar, detail panels
- `components/runtime-header/*` — StickyRuntimeHeader, section nav, status badge
- Dashboard: sticky header + section scroll IDs + RuntimeMarketGraphPanel
- Event Graph 페이지: Market Graph API 기반 전체 화면

## 검증 (현대자동차 trace 20260528_095707)
- center: 현대자동차 / 005380
- nodes: 11, edges: 10
- 삼성전자(오염 sample) 노드 없음: OK

## API
```text
GET /api/market-graph/{traceId}
GET /api/runtime-status/{traceId}
```
