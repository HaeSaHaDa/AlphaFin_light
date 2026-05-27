# TASK-028 — Dashboard Query Flow 수정

## 목표

Dashboard에서 Query 입력 시 Unified Engine이 실행되고,
반환된 `trace_id` 기반으로 모든 Viewer가 갱신되도록 흐름 수정.

## 배경

기존 Dashboard는 `GET /api/*/latest` 에만 의존하여
새 Query를 입력해도 이전(삼성전자) 결과가 고정 표시되는 문제 발생.

## 수행 내용

### 백엔드

- `src/dashboard_api/routes/engine.py` 신규 생성
  - `POST /api/engine/run` 엔드포인트
  - `query`, `persona`, `ticker` 입력 지원
  - `run_unified_pipeline` 호출 → `trace_id` 반환
- `src/dashboard_api/routes/memory.py`
  - `GET /api/memory/{trace_id}` 추가
- `src/dashboard_api/routes/stock_chain.py`
  - `GET /api/stock-chain/{trace_id}` 추가
- `src/dashboard_api/services/memory_service.py`
  - `fetch_memory_by_trace(trace_id)` 추가
- `src/dashboard_api/services/stock_chain_service.py`
  - `fetch_stock_chain_by_trace(trace_id)` 추가
- `src/dashboard_api/app.py`
  - `engine` 라우터 등록

### 프론트엔드

- `dashboard-ui/src/services/api.ts`
  - `getMemory(traceId?)` — `/latest` → `/{trace_id}` 전환
  - `getStockChain(traceId?)` — `/latest` → `/{trace_id}` 전환
  - `runEngine(query, ticker, persona)` 신규 — `POST /api/engine/run`
  - `loadDashboardData`: 모든 fetch를 `traceId` 기반으로 통일
- `dashboard-ui/src/hooks/use-dashboard-data.ts`
  - `runAndLoad(query, ticker)` 신규: 엔진 실행 → `load(trace_id)` 체인
  - `engineRunning` 상태 추가 (spinner용)
  - query 변경 시 이전 결과 `EMPTY` 초기화
- `dashboard-ui/src/components/query/query-input-panel.tsx`
  - **Run Engine** 버튼 추가 (엔진 실행 + trace_id 기반 로드)
  - `engineRunning` spinner 표시
  - 종목명 → ticker 자동 추론(`TICKER_MAP`)
  - trace_id 직접 입력 조회 유지
  - Latest Trace 버튼 유지
- `dashboard-ui/src/components/dashboard-client.tsx`
  - `runAndLoad`, `engineRunning` 연결

## 검증

- `npm run build` 타입 에러 없음 (exit 0)
- `run_sample.py` 모든 GET /api/*/latest 정상 (exit 0)
- latest API 의존 제거 완료 (getMemory, getStockChain 포함)
- trace_id 기반 조회 전체 적용

## 제외

- Multi-user session
- WebSocket / 실시간 streaming
- 투자 recommendation
- 과도한 추상화
