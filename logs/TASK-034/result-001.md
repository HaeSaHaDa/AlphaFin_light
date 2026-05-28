# TASK-034 Result 001

## 완료 항목

| 항목 | 상태 |
|------|------|
| KOSPI200 company_master (seed 50종, pykrx fallback) | OK |
| company_master 모듈 5개 | OK |
| GET /api/company/search (exact 우선) | OK |
| GET /api/company/{ticker} | OK |
| POST /api/query/run | OK |
| run_runtime_query_selected | OK |
| Dashboard company-selector UI | OK |
| selectedTicker 상태 (use-dashboard-data) | OK |
| TASK-033 done (기존) | OK |

## 검색 검증 (CLI)

```
삼성전기 -> [('삼성전기', '009150')]
삼성전자 -> [('삼성전자', '005930')]
삼성전   -> 삼성전기·삼성전자 각각 노출 (사용자 선택 필요)
```

## 실행

```bash
# Backend
uvicorn src.dashboard_api.app:app --host 0.0.0.0 --port 8000

# Frontend
cd dashboard-ui && npm run dev
```

데모: 자동완성에서 **삼성전기** 선택 → 키워드 `MLCC 전장부품` → 분석 실행 → ticker `009150` 확정.

## 비고

- startup 시 `load_kospi200_companies(sync_companies_table=False)` 자동 적재
- 부분 문자열 자동 resolver는 UI에서 제거; 목록 선택 필수
