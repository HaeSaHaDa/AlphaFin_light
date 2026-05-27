# TASK-026-build-retrieval-analysis-viewer.md

# TASK-026 Retrieval & Analysis Viewer 고도화

## 상태

DONE

---

# 완료 결과

- `/analysis` Retrieval & Analysis Viewer 구축
- explainability 필드 API 보강 및 npm build 성공

---

# 관련 문서

```text
prompts/TASK-026/prompt-001.md
logs/TASK-026/result-001.md
```

---

# 목표

현재 Dashboard UI에서
Retrieval, Analysis, Reflection 흐름을
더 상세하고 추적 가능하게 시각화하는
Retrieval & Analysis Viewer를 구축한다.

현재 TASK의 목표는
단순 결과 표시를 넘어,
Financial AI Engine이:

```text
무엇을 검색했고
왜 그렇게 분석했고
어떤 근거를 사용했는지
```

를 상세하게 보여주는 것이다.

현재 단계에서는
복잡한 explainable AI framework보다
명시적이고 추적 가능한 reasoning visualization에 집중한다.

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
→ Dashboard UI
```

현재 시스템은:

```text
기본 Dashboard UI
```

까지 가능하다.

하지만 현재 구조는:

```text
retrieval 근거
analysis reasoning
reflection reasoning
```

을 상세하게 추적하기 어렵다.

현재 TASK에서는
AI 분석 흐름을 상세하게 시각화한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Retrieval Detail Viewer 구현
- Chunk Ranking Viewer 구현
- Similarity Score Viewer 구현
- Context Assembly Viewer 구현
- Analysis Reasoning Viewer 구현
- Reflection Reasoning Viewer 구현
- Source Trace Viewer 구현
- Prompt/Context Preview Viewer 구현
- Engine Step Timeline 구현
- Analysis Metadata Panel 구현
- 샘플 분석 흐름 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- LLM token streaming
- 실시간 reasoning animation
- Prompt editing 기능
- Multi-user annotation
- Collaborative review
- RLHF feedback UI
- Autonomous prompt optimization
- 실시간 투자 recommendation
- Auto trading visualization
- GPT 내부 attention visualization
- Chain-of-thought 완전 노출

현재 TASK는
추적 가능한 reasoning visualization만 구현한다.

---

# 생성 대상 구조

```text
dashboard-ui/src/components/
├─ retrieval-detail/
├─ context-viewer/
├─ reasoning-viewer/
├─ reflection-detail/
├─ source-trace/
├─ timeline/
└─ metadata-panel/
```

---

# Viewer 역할

현재 Viewer 역할:

- Retrieval 근거 표시
- similarity score 표시
- analysis reasoning 표시
- reflection reasoning 표시
- source trace 표시
- pipeline timeline 표시
- 발표용 explainability 강화

---

# Retrieval Detail Viewer

역할:

- retrieval chunk 상세 표시
- similarity ranking 표시
- retrieval source 표시

예상 표시 항목:

```text
- chunk rank
- similarity score
- source file
- chunk preview
- retrieval timestamp
```

---

# Context Assembly Viewer

역할:

- 어떤 Context가 합쳐졌는지 표시
- Layered Context 표시

예상 표시 항목:

```text
- retrieval context
- memory context
- reflection context
- stock chain context
```

---

# Analysis Reasoning Viewer

역할:

- bullish/bearish reasoning 표시
- risk reasoning 표시

예상 표시 항목:

```text
- bullish_factors
- bearish_factors
- risks
- evidence summary
```

---

# Reflection Detail Viewer

역할:

- reflection reasoning 표시
- missing risk reasoning 표시

예상 표시 항목:

```text
- overconfidence_detected
- missing_risks
- context_gaps
- improvement_suggestions
```

---

# Source Trace Viewer

역할:

- 어떤 source가 사용됐는지 표시
- retrieval source 추적

예상 표시 항목:

```text
- source path
- chunk id
- retrieval order
- related stock/entity
```

---

# Timeline Viewer

역할:

- pipeline 단계 흐름 표시
- temporal lifecycle 표시

예상 표시 항목:

```text
retrieval
→ context assembly
→ reasoning
→ reflection
→ memory update
→ stock chain
→ evaluation
```

---

# Metadata Panel 역할

현재 Metadata 역할:

- trace_id 표시
- execution time 표시
- token usage 표시(optional)
- hallucination risk 표시
- engine version 표시

---

# UI 레이아웃 목표

예상 레이아웃:

```text
┌─────────────────────────────────┐
│ Query / Metadata                │
├──────────────┬──────────────────┤
│ Retrieval    │ Context Viewer   │
├──────────────┼──────────────────┤
│ Analysis     │ Reflection       │
├──────────────┴──────────────────┤
│ Source Trace                    │
├─────────────────────────────────┤
│ Timeline                        │
└─────────────────────────────────┘
```

---

# API 연동 대상

현재 API 연동 대상:

```text
GET /api/retrieval/{trace_id}
GET /api/reflection/{trace_id}
GET /api/trace/{trace_id}
GET /api/evaluation/{trace_id}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Dashboard API 재사용
- 기존 Dashboard UI 재사용
- trace_id 기반 조회 유지
- source traceability 유지
- 발표용 explainability 우선
- 작은 component 유지
- 과도한 animation 금지
- 과도한 abstraction 금지
- Chain-of-thought 직접 노출 금지

---

# 예상 기능

## Retrieval Detail Component

예상 기능:

```text
render_chunk_rankings()
render_similarity_scores()
```

---

## Context Viewer Component

예상 기능:

```text
render_context_layers()
render_context_sources()
```

---

## Reasoning Viewer Component

예상 기능:

```text
render_bullish_factors()
render_bearish_factors()
render_risk_factors()
```

---

## Reflection Detail Component

예상 기능:

```text
render_missing_risks()
render_overconfidence()
```

---

## Source Trace Component

예상 기능:

```text
render_source_paths()
render_chunk_sources()
```

---

## Timeline Component

예상 기능:

```text
render_pipeline_steps()
render_temporal_flow()
```

---

## Metadata Panel Component

예상 기능:

```text
render_trace_metadata()
render_hallucination_risk()
```

---

# Viewer 활용 목표

현재 활용 목표:

```text
- 발표용 explainability 강화
- Retrieval debugging
- Reflection debugging
- Reasoning 흐름 확인
- Source traceability 강화
- Engine transparency 강화
```

현재 단계에서는
실시간 투자 recommendation UI를 구현하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Retrieval Viewer 검증

- chunk ranking 표시 여부
- similarity score 표시 여부
- retrieval source 표시 여부

---

## Context Viewer 검증

- Layered Context 표시 여부
- Context source 표시 여부

---

## Reasoning Viewer 검증

- bullish/bearish reasoning 표시 여부
- risk reasoning 표시 여부

---

## Reflection Viewer 검증

- missing_risks 표시 여부
- context_gaps 표시 여부

---

## Source Trace 검증

- source path 표시 여부
- chunk trace 표시 여부

---

## Timeline 검증

- pipeline 단계 표시 여부
- temporal flow 표시 여부

---

## Metadata 검증

- trace_id 표시 여부
- hallucination risk 표시 여부
- execution metadata 표시 여부

---

## 구조 검증

- 신규 component 구조 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-026/
```

---

# 관련 Logs

```text
logs/TASK-026/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Retrieval Detail Viewer 구축 완료
- Context Viewer 구축 완료
- Reasoning Viewer 구축 완료
- Reflection Detail Viewer 구축 완료
- Source Trace Viewer 구축 완료
- Timeline Viewer 구축 완료
- Metadata Panel 구축 완료
- 발표 가능한 explainability 확보
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-027-build-event-graph-visualization
- TASK-028-build-memory-timeline-visualization
- TASK-029-build-signal-evaluation-system

단,
현재 TASK에서는
실시간 투자 recommendation 시스템을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- End-to-End traceability 유지
- Retrieval explainability 유지
- Memory lifecycle 유지
- Reflection 기반 개선 유지
- 발표 가능한 transparency 유지
- 과도한 Autonomous AI 구조 금지