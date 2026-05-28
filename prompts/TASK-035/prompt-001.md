# TASK-035 Prompt 001

## 목표

selectedTicker + traceId 기준 Dashboard 전체 패널 Runtime 동기화.

## 수행

- `runtime-state/` — RuntimeQueryProvider, panel loader, sync helpers
- `runtime-panels/` — traceId 필수 래퍼 패널
- API `/latest` 클라이언트 호출 제거
- 서브페이지 trace_id URL 연동, loadLatest 제거
- mock 뉴스·event graph demo 데이터 제거

## 검증

- 동일 traceId로 retrieval/signal/memory/stock-chain 로드
- trace 없을 때 idle/에러만 표시 (sample 없음)
