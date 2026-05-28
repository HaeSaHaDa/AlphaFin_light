# TASK-034 Prompt 001

## 목표

KOSPI200 company master, 종목 선택·토픽 키워드 분리, selectedTicker 기반 Runtime Query Flow 구축.

## 수행

- `company_master` 테이블 및 seed/pykrx 로더
- `GET /api/company/search`, `GET /api/company/{ticker}`, `POST /api/query/run`
- `run_runtime_query_selected` (ticker + keywords 확정)
- Dashboard `company-selector` UI (자동완성 → 선택 확정 → 분석 실행)
- 삼성전기/삼성전자 exact match 우선 검색

## 검증

- `삼성전기` 검색 → 009150 단독
- `삼성전자` 검색 → 005930 단독
- UI에서 목록 선택 후 `/api/query/run` 실행
