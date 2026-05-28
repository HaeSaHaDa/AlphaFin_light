# TASK-033-connect-runtime-query-db-and-retrieval-flow.md

# TASK-033 Runtime Query / DB / Retrieval Flow 연결

## 상태

TODO

---

# 목표

현재 Dashboard와 Engine이:

```text
샘플 데이터
mock trace
고정 JSON
fallback rendering
```

중심으로 동작하는 문제를 해결하고,

실제 Runtime 기반:

```text
검색어 입력
→ Company Resolver
→ ingestion
→ DB 저장
→ retrieval
→ engine 실행
→ trace 생성
→ dashboard rendering
```

흐름을 완전히 연결한다.

현재 TASK의 목표는
단순 UI 출력이 아니라:

```text
실제 검색어 기반
실제 데이터 기반
실제 retrieval 기반
```

Financial AI Engine Runtime을 완성하는 것이다.

---

# 배경

현재 프로젝트는 다음 흐름까지 구축 완료되었다.

```text
수집
→ 저장
→ Chunking
→ Embedding
→ Semantic Retrieval
→ Financial Analysis
→ Reflection
→ Layered Memory
→ Temporal Market Memory
→ Stock Chain
→ Signal Evaluation
→ Explainable Dashboard
→ Company Resolver
→ Dynamic Ingestion Pipeline
→ Cost Guard
→ Embedding Cache
→ Dashboard Stabilization
```

현재 시스템은:

```text
회사명 입력
→ ingestion 실행
```

까지 일부 가능하다.

하지만 현재 Dashboard는:

```text
실제 DB 연결 부족
실제 retrieval 연결 부족
sample trace fallback 사용 가능성
hardcoded rendering 가능성
```

문제가 존재한다.

현재 TASK에서는:

```text
실제 Runtime Query Flow
```

를 완전히 연결한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Query → Company Resolver 연결
- Resolver → Ingestion 연결
- Ingestion → DB 저장 검증
- DB → Retrieval 연결
- Retrieval → Engine 연결
- Engine → Trace 생성 연결
- Trace → Dashboard Rendering 연결
- 실제 DB 조회 구현
- 실제 Retrieval Query 구현
- 실제 Chunk Retrieval 구현
- Dynamic Trace 생성 구현
- Latest Trace fallback 제거
- Hardcoded Sample 제거
- Dashboard 실시간 Runtime 연결
- API 응답 검증
- Query 기반 종목 전환 검증
- Runtime Log 출력 강화
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 신규 AI 모델 추가
- 신규 Retrieval 알고리즘 추가
- 신규 Memory 구조 추가
- Real-time Streaming
- Broker API
- Auto Trading
- HTS 기능
- Multi-user SaaS
- 분산 MLOps
- Kubernetes
- 실시간 전체 시장 ingestion

현재 TASK는:

```text
Runtime Integration
```

만 수행한다.

---

# 현재 문제

현재 Dashboard 증상:

```text
현대자동차 검색
↓

삼성전자 느낌 결과 유지
```

가능성 존재.

현재 의심 구조:

```text
Query Input
↓

sample trace 호출

↓

sample JSON rendering
```

가능성 존재.

---

# 목표 Runtime Flow

현재 TASK 목표 흐름:

```text
사용자 입력:
현대자동차 전기차 전망

↓

Company Resolver

↓

ticker:
005380

↓

ingestion cache 확인

↓

필요 시 ingestion 실행

↓

DB 저장

↓

retrieval query 실행

↓

관련 chunk 검색

↓

engine reasoning 실행

↓

trace 생성

↓

dashboard rendering
```

---

# 생성 대상 구조

```text
src/runtime_flow/
├─ runtime_query_runner.py
├─ retrieval_executor.py
├─ trace_manager.py
├─ runtime_context_builder.py
├─ runtime_logger.py
└─ dashboard_response_builder.py
```

---

# Runtime Query 역할

현재 역할:

- 실제 query 기반 실행
- company resolver 연결
- runtime ingestion 연결
- dynamic trace 생성

---

# Retrieval 역할

현재 역할:

- DB 기반 retrieval
- vector similarity search
- chunk retrieval
- query relevance filtering

---

# Trace 역할

현재 역할:

- runtime trace 생성
- trace_id 발급
- dashboard 연결
- explainability 유지

---

# Dashboard 역할

현재 역할:

- 실제 runtime 결과 표시
- 실제 retrieval 결과 표시
- 실제 종목 정보 표시
- 실제 signal 표시

---

# 제거 대상

현재 TASK에서 제거 대상:

```text
- sample trace fallback
- hardcoded sample data
- static retrieval response
- 삼성전자 고정 response
- mock dashboard rendering
```

---

# Runtime Log 목표

현재 목표:

```text
[Resolver]
현대자동차 → 005380

[Ingestion]
cache hit

[Retrieval]
retrieved 8 chunks

[Engine]
runtime reasoning completed

[Trace]
trace_id 생성 완료
```

---

# DB 검증 목표

현재 검증 대상:

```sql
SELECT * FROM companies;
SELECT * FROM news_documents;
SELECT * FROM chunks;
SELECT * FROM embeddings;
SELECT * FROM traces;
```

---

# Retrieval 검증 목표

현재 검증 목표:

```text
현대자동차 query
↓

현대자동차 관련 chunk retrieval
```

삼성전자 query:

```text
삼성전자 관련 chunk retrieval
```

종목별 retrieval 분리 확인.

---

# Dashboard 검증 목표

현재 검증 목표:

```text
현대자동차 검색
↓

현대자동차 정보 표시
```

삼성전자 검색:

```text
삼성전자 정보 표시
```

동적 전환 검증.

---

# API 연동 대상

현재 API 대상:

```text
POST /api/engine/run
POST /api/ingestion/run
GET /api/retrieval/{trace_id}
GET /api/trace/{trace_id}
GET /api/signal/{trace_id}
GET /api/evaluation/{trace_id}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Engine 구조 재사용
- 기존 Retrieval 구조 재사용
- 기존 Dashboard UI 재사용
- 기존 Company Resolver 재사용
- 기존 Embedding Cache 재사용
- 실제 DB 기반 실행 우선
- runtime trace 기반 rendering
- explainability 유지
- OpenAI 호출 최소화
- 발표 가능한 Runtime UX 유지
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## runtime_query_runner.py

역할:

- runtime query 실행

예상 기능:

```text
run_runtime_query()
execute_dynamic_analysis()
```

---

## retrieval_executor.py

역할:

- 실제 retrieval 실행

예상 기능:

```text
execute_retrieval()
retrieve_chunks()
```

---

## trace_manager.py

역할:

- trace 생성 및 조회

예상 기능:

```text
create_trace()
load_trace()
```

---

## runtime_context_builder.py

역할:

- retrieval 기반 context 생성

예상 기능:

```text
build_runtime_context()
assemble_query_context()
```

---

## dashboard_response_builder.py

역할:

- dashboard runtime response 생성

예상 기능:

```text
build_dashboard_response()
render_runtime_payload()
```

---

# Runtime UX 목표

현재 목표:

```text
사용자:
현대자동차 분석해줘

↓

실제 retrieval 수행

↓

실제 현대차 뉴스 retrieval

↓

실제 reasoning 수행

↓

실제 trace 생성

↓

실제 dashboard rendering
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 실제 Runtime AI Demonstration
- Query 기반 Dynamic Analysis
- 실제 Retrieval Explainability
- 실제 DB 기반 Dashboard
- 발표 가능한 Runtime Flow
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Resolver 검증

- company resolver 동작 여부
- ticker mapping 정상 여부

---

## Ingestion 검증

- ingestion cache 동작 여부
- DB 저장 여부

---

## Retrieval 검증

- 실제 retrieval query 실행 여부
- chunk retrieval 정상 여부
- 종목별 retrieval 분리 여부

---

## Trace 검증

- trace_id 생성 여부
- dynamic trace 생성 여부

---

## Dashboard 검증

- query 기반 결과 변경 여부
- 종목별 dashboard 변경 여부
- hardcoded sample 제거 여부

---

## Runtime 검증

- 실제 runtime execution 여부
- 실제 engine reasoning 여부
- runtime log 출력 여부

---

## 구조 검증

- 기존 Engine 유지 여부
- 기존 Event Graph 유지 여부
- TASK 범위 외 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-033/
```

---

# 관련 Logs

```text
logs/TASK-033/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Runtime Query Flow 연결 성공
- DB 기반 Retrieval 성공
- Dynamic Trace 생성 성공
- Query 기반 Dashboard Rendering 성공
- Hardcoded Sample 제거 성공
- 실제 Runtime Execution 성공
- 실제 종목별 분석 성공
- 발표 가능한 Runtime Demonstration 확보 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-034-build-portfolio-backtesting-suite
- TASK-035-build-backtesting-visualization
- TASK-036-build-presentation-demo-scenario

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- 실제 Runtime Flow 우선
- End-to-End traceability 유지
- 실제 Retrieval 기반 유지
- 발표 가능한 Runtime UX 유지
- OpenAI 비용 안정성 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지