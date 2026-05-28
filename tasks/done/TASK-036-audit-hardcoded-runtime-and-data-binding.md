# TASK-036-audit-hardcoded-runtime-and-data-binding.md

# TASK-036 Hardcoded Runtime & Data Binding Audit

## 상태

DONE

---

# 목표

현재 Financial AI Dashboard와 Runtime Engine 전체에서:

```text
hardcoded data
sample payload
mock rendering
default state
fallback trace
static graph
demo signal
initial memory
```

등이 남아있는지 전수 조사하고,

실제 Runtime 기반:

```text
selectedTicker
+
traceId
+
DB retrieval
+
runtime payload
```

기반으로 동작하는지 검증한다.

현재 TASK의 목표는:

```text
"실제로 Runtime 기반인가?"
```

를 시스템 전체에서 Audit하는 것이다.

현재 단계에서는
기능 추가보다:

```text
Runtime Integrity
Data Consistency
Runtime Purity
```

검증에 집중한다.

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
→ Runtime Query Flow
→ KOSPI200 Company Master
→ Dashboard Runtime Binding
```

현재 Runtime 구조는:

```text
selectedTicker
+
traceId
```

기반으로 동작해야 한다.

하지만 현재 시스템은 초기 구축 과정에서:

```text
sample JSON
fallback payload
mock graph
hardcoded signal
latest trace fallback
initial memory
demo response
```

가 일부 남아있을 가능성이 존재한다.

현재 TASK에서는:

```text
Runtime 전체 Audit
```

을 수행한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Dashboard 전체 Runtime Audit
- hardcoded data 탐지
- sample payload 탐지
- mock rendering 탐지
- fallback trace 탐지
- static graph 탐지
- fake signal 탐지
- initial state 탐지
- placeholder payload 탐지
- selectedTicker binding 검증
- traceId binding 검증
- retrieval binding 검증
- DB binding 검증
- Runtime payload consistency 검증
- API response consistency 검증
- Panel synchronization 검증
- Runtime state audit
- useEffect default state audit
- demo data 제거
- audit report 생성
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 신규 AI 모델 추가
- 신규 Retrieval 알고리즘 추가
- Backtesting
- Auto Trading
- Broker API
- HTS 기능
- Real-time Streaming
- Kubernetes
- Multi-user SaaS
- UI 리디자인
- 신규 기능 추가

현재 TASK는:

```text
Runtime Audit
```

만 수행한다.

---

# 현재 문제

현재 의심 증상:

```text
현대자동차 검색
↓

일부 패널은 현대차 데이터

↓

일부 패널은 삼성전자 느낌 데이터

↓

일부는 기본값 표시
```

원인 가능성:

```text
hardcoded payload
fallback trace
sample graph
initial state rendering
```

---

# Audit 목표

현재 목표:

```text
전체 시스템에서:
- 실제 Runtime 기반인지
- hardcoded인지
- sample인지
- fallback인지
```

전수 확인.

---

# Audit 대상 영역

## Dashboard Panels

검사 대상:

```text
Signal Panel
News Panel
Event Graph
Memory Timeline
Evaluation Summary
Reflection Viewer
Retrieval Viewer
Stock Chain
```

---

## Runtime State

검사 대상:

```text
selectedTicker store
traceId store
runtime cache
loading state
default state
fallback state
```

---

## API Response

검사 대상:

```text
/api/query/run
/api/trace/{traceId}
/api/retrieval/{traceId}
/api/signal/{traceId}
/api/evaluation/{traceId}
/api/reflection/{traceId}
/api/memory/{traceId}
/api/stock-chain/{traceId}
```

---

## Retrieval Flow

검사 대상:

```text
DB retrieval
vector retrieval
chunk retrieval
ticker filtering
query builder
```

---

## Frontend Rendering

검사 대상:

```text
default props
sample JSON
fallback rendering
placeholder payload
demo state
mock hooks
```

---

# 생성 대상 구조

```text
audit/
├─ runtime-audit/
│  ├─ dashboard-audit.md
│  ├─ retrieval-audit.md
│  ├─ runtime-state-audit.md
│  ├─ api-audit.md
│  ├─ frontend-audit.md
│  └─ hardcoded-data-report.md
```

```text
logs/TASK-036/
├─ audit-result.md
├─ removed-hardcoded-items.md
└─ runtime-consistency-report.md
```

---

# Audit 기준

현재 기준:

| 항목 | 기준 |
|---|---|
| Signal | traceId 기반인가 |
| News | selectedTicker 기반인가 |
| Graph | retrieval 기반인가 |
| Memory | runtime memory인가 |
| Evaluation | runtime evaluation인가 |
| Reflection | runtime reflection인가 |
| Retrieval | 실제 chunk retrieval인가 |

---

# 제거 대상

현재 제거 대상:

```text
- latest trace fallback
- sample signal
- static graph payload
- hardcoded ticker
- 삼성전자 기본값
- mock memory
- demo evaluation
- placeholder retrieval result
- fake confidence score
- static event graph
```

---

# Runtime Purity 목표

현재 목표:

```text
검색 실행
↓

실제 retrieval 수행

↓

실제 runtime payload 생성

↓

전체 Dashboard 동일 payload 사용
```

---

# Audit Report 목표

현재 목표:

```text
어디가 Runtime 기반인지
어디가 hardcoded인지
어디가 sample인지
```

명확히 기록.

---

# Runtime Verification 목표

현재 목표:

```text
삼성전기 검색
↓

삼성전기 retrieval

↓

삼성전기 signal

↓

삼성전기 graph

↓

삼성전기 memory
```

전체 일관성 확인.

---

# 검색 검증 목표

현재 목표:

```text
selectedTicker 변경
↓

모든 Panel 변경
```

동기화 검증.

---

# API 검증 목표

현재 목표:

```text
traceId별 payload 분리
```

예상 검증:

```text
trace_001 → 삼성전기
trace_002 → 현대자동차
```

payload 분리 여부 확인.

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Runtime Flow 유지
- 기존 Retrieval 구조 유지
- 기존 Dashboard UI 유지
- explainability 유지
- OpenAI 호출 최소화 유지
- 실제 Runtime 기준 검증
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## dashboard-audit.md

역할:

- Dashboard Runtime Audit

예상 내용:

```text
어떤 Panel이 Runtime 기반인지 기록
```

---

## retrieval-audit.md

역할:

- Retrieval Audit

예상 내용:

```text
실제 retrieval 여부 확인
```

---

## runtime-state-audit.md

역할:

- Runtime State Audit

예상 내용:

```text
selectedTicker/traceId consistency 확인
```

---

## hardcoded-data-report.md

역할:

- hardcoded 제거 목록 기록

예상 내용:

```text
제거된 sample payload 기록
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- Runtime Integrity 확보
- Dashboard Consistency 확보
- 실제 Runtime Demonstration 확보
- 발표 안정성 확보
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Runtime 검증

- 실제 Runtime payload 사용 여부
- 실제 traceId 기반 rendering 여부

---

## Retrieval 검증

- 실제 retrieval 수행 여부
- ticker 기반 retrieval 여부

---

## Dashboard 검증

- 모든 Panel synchronization 여부
- sample fallback 제거 여부

---

## API 검증

- trace별 payload 분리 여부
- hardcoded response 제거 여부

---

## State 검증

- selectedTicker consistency 여부
- traceId consistency 여부

---

## Audit 검증

- hardcoded data report 작성 여부
- runtime audit report 작성 여부

---

# 관련 Prompt

```text
prompts/TASK-036/
```

---

# 관련 Logs

```text
logs/TASK-036/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Runtime Audit 완료
- hardcoded data 제거 완료
- sample payload 제거 완료
- Dashboard consistency 확보 완료
- Runtime Integrity 확보 완료
- Runtime Audit Report 작성 완료
- 발표 가능한 Runtime 안정성 확보 완료
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-037-build-portfolio-backtesting-suite
- TASK-038-build-backtesting-visualization
- TASK-039-build-presentation-demo-scenario

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- Runtime Integrity 우선
- Runtime Consistency 우선
- ticker 기반 정확성 우선
- End-to-End traceability 유지
- 발표 가능한 Runtime 안정성 유지
- OpenAI 비용 안정성 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지