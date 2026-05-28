# TASK-038 result-001

## 수행 요약

- TASK-037 상태를 `DONE`으로 정정
- TASK-038 상태를 `DOING`으로 변경
- Backend Market Graph reasoning 확장
  - relation type: `COMPETES_WITH`, `AFFECTED_BY`, `BENEFITS_FROM` 추가
  - edge direction / confidence / impact / evidence 생성
  - macro keyword dictionary(금리/환율/유가/IRA/중국) 기반 관계 생성
  - weak relation pruning 기반 relation explanation 생성
- Backend API 확장
  - `GET /api/relation-explanation/{trace_id}`
  - `GET /api/risk-exposure/{trace_id}`
  - `GET /api/market-insight/{trace_id}`
- Frontend reasoning 모듈 추가 (`dashboard-ui/src/reasoning/*`)
- Frontend market-intelligence 컴포넌트 추가 (`dashboard-ui/src/components/market-intelligence/*`)
- RuntimeMarketGraphPanel에 Market Insight 표시 연결

## 변경 파일(핵심)

- `src/dashboard_api/services/market_graph_service.py`
- `src/dashboard_api/routes/market_graph.py`
- `src/dashboard_api/schemas/market_graph_schema.py`
- `dashboard-ui/src/services/api.ts`
- `dashboard-ui/src/types/market-graph.ts`
- `dashboard-ui/src/reasoning/*`
- `dashboard-ui/src/components/market-intelligence/*`
- `dashboard-ui/src/components/runtime-panels/RuntimeMarketGraphPanel.tsx`

## 남은 확인

- 로컬 서버 재시작 후 `/api/market-insight/{traceId}` 응답 확인
- 대시보드에서 relation explanation/리스크 노출 UI 확인
