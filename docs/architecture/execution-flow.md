# AlphaFin LTE 실행 흐름

## 문서 목적

현재 구현된 Runtime Query의 실제 실행 순서와 결과 조회 흐름을 정의한다.

---

# 표준 실행 명령

Runtime:

```bash
python -m src.runtime_flow.runtime_query_runner "<회사명이 포함된 질문>"
```

Backend:

```bash
python -m uvicorn src.dashboard_api.app:app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd dashboard-ui
npm run dev
```

---

# Runtime Query 흐름

```text
사용자 질문 또는 selectedTicker
→ Company Resolver
→ Ingestion Cache 확인
→ 필요 시 뉴스/문서 수집 및 embedding
→ OpenDART 공시 cache/수집 확인
→ 뉴스 Vector Retrieval
→ 공시 Retrieval
→ Evidence 병합
→ Runtime Context 생성
→ Unified Engine
→ Evaluation / Reflection
→ Memory / Event Graph / Stock Chain
→ Unified Result / Trace 저장
→ Dashboard Bundle 조회
```

---

# 단계별 책임

## 1. Query 입력

- 자유 질문: `run_runtime_query`
- 선택 종목: `run_runtime_query_selected`
- Dashboard API: `POST /api/query/run`, `POST /api/runtime/run`

## 2. Company Resolve

`src/company_resolver/`와 `src/company_master/`가 회사명, ticker, corp_code를 확정한다.

## 3. Ingestion

`src/ingestion_pipeline/`이 ticker별 준비 상태와 embedding 수를 확인한다.
준비된 데이터는 cache를 재사용한다.

## 4. Retrieval

`src/runtime_flow/retrieval_executor.py`가 MariaDB embedding을 ticker로 필터링한다.
`src/disclosure/`는 공시 chunk를 별도로 검색한다.

## 5. Evidence 통합

`src/runtime_query/`가 뉴스와 공시 결과를 정규화하고 병합한다.

Runtime Context 주요 필드:

```text
trace_id
ticker
query
news_chunks
disclosure_chunks
merged_evidence
reasoning_context
source_breakdown
```

## 6. Unified Engine

`src/rag/unified_engine/`이 다음 단계를 실행한다.

```text
Context Assembly
→ Character Analysis
→ Evaluation
→ Reflection
→ Analysis Memory
→ Layered/Temporal Memory
→ Event Graph
→ Stock Chain
→ Result 저장
```

## 7. Trace 저장

`data/unified_engine/`에 다음 파일이 생성된다.

```text
final_results/{trace_id}_result.json
traces/{trace_id}_trace.json
engine_runs/{trace_id}_pipeline.json
```

## 8. Dashboard 조회

Frontend는 traceId를 기준으로 Runtime, Retrieval, Memory, Graph, Evaluation API를 호출한다.
latest/sample fallback보다 명시적 trace 조회를 우선한다.

---

# Runtime 상태 유지

Frontend의 Runtime Context는 다음 값을 유지한다.

```text
selectedTicker
traceId
companyName
runtimeQuery
phase
panelStatus
```

URL의 `trace_id`와 sessionStorage의 Runtime session을 사용한다.

---

# 현재 확인된 위험

- OpenAI 호출 성공 여부가 최종 `completed` 상태에 직접 반영되지 않을 수 있다.
- module 실행 시 `src.runtime_flow.__init__` 선행 import warning이 발생한다.
- 실행은 trace, memory, graph, signal 파일을 실제로 갱신한다.
