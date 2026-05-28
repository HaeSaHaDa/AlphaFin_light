# Retrieval Audit

## Flow

```text
POST /api/query/run
  → run_runtime_query_selected(ticker, keywords)
  → build_runtime_query(company, ticker, keywords)
  → execute_retrieval(query, ticker, top_k=8)
  → filters: { ticker }
```

## DB / Vector

- `document_embeddings` + `document_chunks` ticker 필터
- Query builder: company + ticker + keywords (no substring resolver on UI path)

## 검증

| 항목 | 상태 |
|------|------|
| ticker 필터 | OK |
| trace별 chunk 분리 | OK |
| placeholder 005930 제거 (TASK-033) | OK |
| latest retrieval API (UI) | 미사용 |
