# TASK-035 Result 001

## 완료

| 항목 | 상태 |
|------|------|
| RuntimeQueryProvider (selectedTicker + traceId) | OK |
| runtime-panel-loader 병렬 로드 | OK |
| Dashboard runtime-panels 바인딩 | OK |
| API client latest fallback 제거 | OK |
| loadLatest / sample UI 제거 | OK |
| Event graph DEMO_PROPAGATION 제거 | OK |
| RelatedNewsPanel mock headlines 제거 | OK |
| 서브페이지 ?trace_id= 연동 | OK |
| TASK-034 done (기존) | OK |

## 동작

1. 종목 선택 + 키워드 → `POST /api/query/run`
2. `traceId` 생성 → `loadRuntimePanels(traceId)` (retrieval, reflection, memory, stock-chain, trace, evaluation, signal)
3. 모든 패널 동일 payload

## 실행

```bash
uvicorn src.dashboard_api.app:app --host 0.0.0.0 --port 8000
cd dashboard-ui && npm run dev
```

http://localhost:3000
