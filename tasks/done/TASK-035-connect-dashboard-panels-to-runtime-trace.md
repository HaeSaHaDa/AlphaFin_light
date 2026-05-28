# TASK-035-connect-dashboard-panels-to-runtime-trace.md

# TASK-035 Dashboard Panels Runtime Trace 연결

## 상태

DONE

---

# 목표

현재 Dashboard는 일부 패널이:

```text
latest trace
sample graph
default signal
mock state
fallback rendering
```

기반으로 동작할 가능성이 존재한다.

현재 TASK의 목표는:

```text
selectedTicker
+
traceId
```

기준으로 Dashboard 전체 패널을 완전히 동기화하여:

```text
검색한 종목의 실제 Runtime 데이터
```

만 표시하도록 Runtime Binding을 완성하는 것이다.

현재 단계에서는
기능 추가보다:

```text
Dashboard 데이터 일관성
Runtime State 통합
실제 Runtime Trace 기반 렌더링
```

에 집중한다.

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
→ Topic Query Flow
```

현재 시스템은:

```text
종목 선택
+
topic keyword
```

기반 Runtime 실행까지 가능하다.

하지만 현재 Dashboard는 일부 패널이:

```text
selectedTicker 미연결
traceId 미연결
sample fallback 사용
```

상태일 가능성이 존재한다.

현재 TASK에서는:

```text
Dashboard 전체 Runtime State 통합
```

을 수행한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- selectedTicker 전역 상태 통합
- traceId 전역 상태 통합
- Dashboard 전체 패널 Runtime Binding
- Signal Panel traceId 연결
- News Panel traceId 연결
- Event Graph traceId 연결
- Memory Timeline traceId 연결
- Evaluation Panel traceId 연결
- Reflection Panel traceId 연결
- Retrieval Viewer traceId 연결
- Dashboard state synchronization 구축
- Runtime refresh flow 구축
- query 변경 시 전체 panel refresh 구현
- sample fallback 제거
- latest trace fallback 제거
- mock rendering 제거
- 실제 Runtime payload 기반 렌더링
- Runtime loading state 구축
- Runtime error state 구축
- Dashboard consistency 개선
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
- 분산 MLOps
- Kubernetes
- Multi-user SaaS

현재 TASK는:

```text
Dashboard Runtime Binding
```

만 수행한다.

---

# 현재 문제

현재 증상:

```text
현대자동차 검색
↓

일부 Panel은 현대차 데이터

↓

일부 Panel은 삼성전자 느낌 데이터

↓

일부 Panel은 기본값
```

가능성 존재.

원인:

```text
패널별 state 분리
traceId 미통합
selectedTicker 미통합
fallback payload 사용
```

---

# 목표 Runtime 구조

현재 목표 구조:

```text
selectedTicker
+
traceId
```

↓

모든 Dashboard Panel 공유

↓

동일 Runtime Payload 사용

↓

전체 화면 동기화
```

---

# 생성 대상 구조

```text
dashboard-ui/src/runtime-state/
├─ runtime-trace-store.ts
├─ selected-ticker-store.ts
├─ runtime-query-context.ts
├─ runtime-panel-loader.ts
└─ dashboard-runtime-sync.ts
```

```text
dashboard-ui/src/components/runtime-panels/
├─ RuntimeSignalPanel.tsx
├─ RuntimeNewsPanel.tsx
├─ RuntimeEventGraphPanel.tsx
├─ RuntimeMemoryPanel.tsx
├─ RuntimeEvaluationPanel.tsx
├─ RuntimeReflectionPanel.tsx
└─ RuntimeRetrievalPanel.tsx
```

---

# Runtime State 역할

현재 역할:

- selectedTicker 상태 관리
- traceId 상태 관리
- Dashboard 전체 synchronization

---

# Runtime Trace 역할

현재 역할:

- Runtime Payload 기준값
- 실제 retrieval 결과 관리
- 실제 signal 관리
- 실제 memory 관리

---

# Panel 역할

현재 역할:

- 동일 traceId payload 사용
- fallback 제거
- runtime consistency 유지

---

# 제거 대상

현재 TASK에서 제거 대상:

```text
- latest trace fallback
- sample signal payload
- mock graph data
- default retrieval response
- static memory payload
- hardcoded evaluation result
```

---

# Runtime Flow 목표

현재 목표 흐름:

```text
종목 선택:
삼성전기 009150

↓

topic:
MLCC 전장부품

↓

runtime query 실행

↓

traceId 생성

↓

모든 Panel 동일 traceId 사용

↓

전체 Dashboard 동기화
```

---

# Dashboard Synchronization 목표

현재 목표:

| 패널 | 기준 |
|---|---|
| Signal | traceId |
| News | traceId |
| Event Graph | traceId |
| Memory | traceId |
| Evaluation | traceId |
| Reflection | traceId |
| Retrieval | traceId |

전부 동일 Runtime 기준 사용.

---

# Loading UX 목표

현재 목표:

```text
Runtime query 실행 중
↓

전체 Dashboard loading state 표시
```

예상 UI:

```text
분석 중...
뉴스 검색 중...
AI reasoning 생성 중...
```

---

# Error UX 목표

현재 목표:

```text
Runtime 실패 시
fallback sample 금지
```

예상 UI:

```text
데이터를 불러오지 못했습니다.
retrieval 결과가 없습니다.
```

---

# API 연동 대상

현재 API 대상:

```text
POST /api/query/run
GET /api/trace/{traceId}
GET /api/retrieval/{traceId}
GET /api/signal/{traceId}
GET /api/evaluation/{traceId}
GET /api/reflection/{traceId}
GET /api/memory/{traceId}
GET /api/stock-chain/{traceId}
```

---

# Runtime Payload 예시

```json
{
  "trace_id": "trace_001",
  "ticker": "009150",
  "company": "삼성전기",
  "signal": "bullish",
  "confidence": 0.82,
  "news": [],
  "retrieval_chunks": [],
  "memory": [],
  "stock_chain": []
}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Runtime Flow 재사용
- 기존 Retrieval 구조 재사용
- 기존 Dashboard UI 재사용
- selectedTicker 기반 유지
- traceId 기반 유지
- explainability 유지
- OpenAI 호출 최소화 유지
- 발표 가능한 UX 유지
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## runtime-trace-store.ts

역할:

- traceId 상태 관리

예상 기능:

```text
setCurrentTrace()
loadRuntimeTrace()
```

---

## selected-ticker-store.ts

역할:

- selectedTicker 상태 관리

예상 기능:

```text
setSelectedTicker()
getSelectedTicker()
```

---

## dashboard-runtime-sync.ts

역할:

- Dashboard synchronization

예상 기능:

```text
syncDashboardPanels()
refreshAllPanels()
```

---

## RuntimeSignalPanel.tsx

역할:

- 실제 signal rendering

예상 기능:

```text
renderRuntimeSignal()
```

---

## RuntimeNewsPanel.tsx

역할:

- 실제 retrieval news rendering

예상 기능:

```text
renderRuntimeNews()
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 실제 Runtime 기반 Dashboard
- 종목별 Dynamic Dashboard
- Explainable Runtime Visualization
- 발표 가능한 Runtime UX
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## State 검증

- selectedTicker 상태 유지 여부
- traceId 상태 유지 여부

---

## Synchronization 검증

- 모든 Panel 동일 traceId 사용 여부
- query 변경 시 전체 refresh 여부

---

## Retrieval 검증

- 실제 retrieval 결과 표시 여부
- 종목별 retrieval 분리 여부

---

## Dashboard 검증

- 삼성전기 검색 시 삼성전기 Dashboard 여부
- 현대차 검색 시 현대차 Dashboard 여부
- sample fallback 제거 여부

---

## Runtime 검증

- 실제 Runtime Payload 사용 여부
- 실제 trace 기반 rendering 여부
- loading/error state 정상 여부

---

## 구조 검증

- 기존 Runtime 구조 유지 여부
- 기존 Retrieval 구조 유지 여부
- TASK 범위 외 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-035/
```

---

# 관련 Logs

```text
logs/TASK-035/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Dashboard Runtime Binding 성공
- selectedTicker 전역 상태 통합 성공
- traceId 전역 상태 통합 성공
- 전체 Panel synchronization 성공
- sample fallback 제거 성공
- 실제 Runtime Payload rendering 성공
- 종목별 Dashboard consistency 확보 성공
- 발표 가능한 Runtime Dashboard 확보 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-036-build-portfolio-backtesting-suite
- TASK-037-build-backtesting-visualization
- TASK-038-build-presentation-demo-scenario

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- Runtime consistency 우선
- ticker 기반 정확성 우선
- End-to-End traceability 유지
- 발표 가능한 UX 유지
- OpenAI 비용 안정성 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지