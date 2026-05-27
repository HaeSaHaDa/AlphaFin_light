# TASK-025-build-dashboard-ui.md

# TASK-025 Dashboard UI 구축

## 상태

TODO

---

# 목표

Financial AI Engine 내부 흐름을
시각적으로 확인할 수 있는
Dashboard UI를 구축한다.

현재 TASK의 목표는
단순 API 응답 확인을 넘어,
Retrieval, Reflection, Memory Lifecycle,
Stock Chain, Evaluation 결과를
사용자가 직관적으로 이해할 수 있는 UI를 만드는 것이다.

현재 단계에서는
복잡한 실시간 collaborative dashboard보다
명시적이고 추적 가능한 단일 사용자 Dashboard에 집중한다.

---

# 배경

현재 프로젝트는 다음 흐름까지 구축 완료되었다.

```text
수집
→ 저장
→ Chunking
→ Embedding
→ Semantic Retrieval
→ Context Assembly
→ Financial Analysis
→ Evaluation
→ Character Layer
→ Memory Layer
→ Market Event Graph
→ Layered Memory
→ Reflection
→ Memory Importance
→ Temporal Market Memory
→ Stock Chain
→ Unified Engine Runner
→ Engine Evaluation Suite
→ Dashboard Backend API
```

현재 시스템은:

```text
Backend API 조회
```

까지 가능하다.

하지만 현재 구조는:

```text
엔진 흐름을 직관적으로 시각화
```

하지 않는다.

현재 TASK에서는
Financial AI Engine을
발표 및 분석 가능한 Dashboard UI로 구축한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Dashboard UI 프로젝트 구조 생성
- Retrieval Viewer 구현
- Reflection Viewer 구현
- Memory Timeline Viewer 구현
- Stock Chain Viewer 구현
- Engine Trace Viewer 구현
- Evaluation Score Panel 구현
- Query Input UI 구현
- API 연동 구현
- 기본 레이아웃 및 Navigation 구현
- 샘플 Dashboard 실행 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Multi-user Dashboard
- Authentication/Authorization
- Realtime Collaboration
- WebSocket Streaming
- 실시간 거래 화면
- Broker API 연동
- TradingView 연동
- 모바일 앱
- Electron Desktop App
- Kubernetes Deployment
- Cloud SaaS 구조
- 실시간 자동 투자 기능
- Autonomous Trading Dashboard

현재 TASK는
단일 발표용 Dashboard UI만 구현한다.

---

# 생성 대상 구조

```text
dashboard-ui/
├─ src/
│  ├─ app/
│  ├─ components/
│  │  ├─ retrieval/
│  │  ├─ reflection/
│  │  ├─ memory/
│  │  ├─ stock-chain/
│  │  ├─ trace/
│  │  └─ evaluation/
│  ├─ services/
│  ├─ hooks/
│  ├─ types/
│  └─ utils/
├─ public/
├─ package.json
└─ README.md
```

---

# 기술 스택

현재 Dashboard UI 기술 스택:

```text
- Next.js 15
- TypeScript
- Tailwind CSS
- shadcn/ui
- React Query(optional)
- Recharts
```

---

# Dashboard 역할

현재 Dashboard 역할:

- Retrieval 결과 시각화
- Reflection 결과 시각화
- Memory lifecycle 시각화
- Stock Chain propagation 시각화
- Engine Trace 시각화
- Evaluation Score 시각화
- 발표 데모 지원

---

# 주요 화면 구성

## 1. Query Input Panel

역할:

- 사용자 Query 입력
- Engine 실행 요청
- trace_id 조회

예상 기능:

```text
- Query 입력창
- Run Engine 버튼
- Latest Trace 조회
```

---

## 2. Retrieval Viewer

역할:

- retrieval chunk 표시
- similarity score 표시
- source 표시

예상 표시 항목:

```text
- chunk text
- similarity score
- chunk source
- retrieval rank
```

---

## 3. Reflection Viewer

역할:

- Reflection 결과 표시
- missing_risks 표시
- overconfidence 표시

예상 표시 항목:

```text
- reflection_summary
- missing_risks
- context_gaps
- improvement_suggestions
```

---

## 4. Memory Timeline Viewer

역할:

- Short/Mid/Long Memory 표시
- promote/decay 표시
- temporal lifecycle 표시

예상 표시 항목:

```text
- memory layer
- importance score
- promotion history
- decay history
```

---

## 5. Stock Chain Viewer

역할:

- Stock Chain 시각화
- propagation 표시
- entity relation 표시

예상 표시 항목:

```text
NVIDIA
↓
HBM
↓
삼성전자
↓
DRAM 가격
```

가능하면:

```text
- node graph
- relation edge
- impact score
```

표시.

---

## 6. Engine Trace Viewer

역할:

- Full reasoning trace 표시
- pipeline 단계 표시

예상 표시 항목:

```text
retrieval
→ context assembly
→ reflection
→ memory update
→ temporal tracking
→ stock chain
→ final result
```

---

## 7. Evaluation Score Panel

역할:

- Engine score 표시
- hallucination risk 표시
- consistency score 표시

예상 표시 항목:

```text
retrieval_score
reasoning_score
reflection_score
memory_score
stock_chain_score
overall_score
```

---

# UI 레이아웃 목표

예상 레이아웃:

```text
┌─────────────────────────────┐
│ Query Input                 │
├──────────────┬──────────────┤
│ Retrieval    │ Reflection   │
├──────────────┼──────────────┤
│ Memory       │ Stock Chain  │
├──────────────┴──────────────┤
│ Engine Trace                │
├─────────────────────────────┤
│ Evaluation Score            │
└─────────────────────────────┘
```

---

# API 연동 대상

현재 API 연동 대상:

```text
GET /api/retrieval/latest
GET /api/reflection/latest
GET /api/memory/latest
GET /api/stock-chain/latest
GET /api/trace/latest
GET /api/evaluation/latest
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Dashboard API 재사용
- trace_id 기반 조회 유지
- API response 구조 유지
- 발표용 가독성 우선
- 작은 component 유지
- 과도한 animation 금지
- 과도한 abstraction 금지
- 실시간 streaming 금지

---

# 예상 기능

## Query Panel

예상 기능:

```text
submit_query(query)
load_latest_trace()
```

---

## Retrieval Component

예상 기능:

```text
render_chunks()
render_similarity_scores()
```

---

## Reflection Component

예상 기능:

```text
render_missing_risks()
render_reflection_summary()
```

---

## Memory Timeline Component

예상 기능:

```text
render_memory_layers()
render_promotions()
render_decays()
```

---

## Stock Chain Component

예상 기능:

```text
render_stock_chain_graph()
render_propagation()
```

---

## Trace Component

예상 기능:

```text
render_pipeline_trace()
render_reasoning_steps()
```

---

## Evaluation Component

예상 기능:

```text
render_scores()
render_hallucination_risk()
```

---

# Dashboard 활용 목표

현재 활용 목표:

```text
- 발표 데모
- Retrieval debugging
- Reflection debugging
- Memory lifecycle 확인
- Stock Chain propagation 확인
- Engine reasoning 흐름 확인
```

현재 단계에서는
실시간 투자 Dashboard를 구현하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## UI 실행 검증

- Dashboard UI 실행 성공 여부
- localhost 접속 성공 여부
- API 연동 성공 여부

---

## Retrieval Viewer 검증

- retrieval chunk 표시 여부
- similarity score 표시 여부

---

## Reflection Viewer 검증

- missing_risks 표시 여부
- reflection_summary 표시 여부

---

## Memory Viewer 검증

- layer 표시 여부
- promotion/decay 표시 여부

---

## Stock Chain Viewer 검증

- propagation 표시 여부
- entity relation 표시 여부

---

## Trace Viewer 검증

- Full pipeline 표시 여부
- reasoning trace 표시 여부

---

## Evaluation Viewer 검증

- overall_score 표시 여부
- hallucination risk 표시 여부

---

## 구조 검증

- `dashboard-ui/` 생성 여부
- component 구조 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-025/
```

---

# 관련 Logs

```text
logs/TASK-025/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Dashboard UI 구축 완료
- API 연동 성공
- Retrieval Viewer 동작 성공
- Reflection Viewer 동작 성공
- Memory Timeline 동작 성공
- Stock Chain Viewer 동작 성공
- Trace Viewer 동작 성공
- Evaluation Panel 동작 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-026-build-retrieval-analysis-viewer
- TASK-027-build-event-graph-visualization
- TASK-028-build-memory-timeline-visualization

단,
현재 TASK에서는
실시간 투자 플랫폼을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- End-to-End traceability 유지
- Retrieval 기반 분석 유지
- Memory lifecycle 유지
- Reflection 기반 개선 유지
- 발표 가능한 UI 유지
- 과도한 Autonomous AI 구조 금지