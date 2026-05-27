# TASK-028-build-memory-timeline-visualization.md

# TASK-028 Memory Timeline Visualization 구축

## 상태

TODO

---

# 목표

Financial AI Engine의
Memory Lifecycle 흐름을
시간 축 기반으로 시각화하는
Memory Timeline Visualization을 구축한다.

현재 TASK의 목표는
단순 Memory Layer 조회를 넘어,
AI가 어떤 시장 이벤트를:

```text
단기 기억
→ 중기 기억
→ 장기 기억
```

으로 유지하고,
어떤 이벤트를 잊어버렸는지까지
직관적으로 보여주는 것이다.

현재 단계에서는
복잡한 cognitive simulation보다
발표 가능한 Memory Lifecycle Visualization에 집중한다.

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
→ Retrieval & Analysis Viewer
→ Event Graph Visualization
```

현재 시스템은:

```text
Memory 상태 조회
```

까지 가능하다.

하지만 현재 구조는:

```text
Memory가 어떻게 변화했는가
```

를 시간 흐름 기반으로 보여주지 못한다.

현재 TASK에서는
시장 이벤트의 Memory Lifecycle을
Timeline 기반으로 시각화한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Memory Timeline Visualization 구현
- Short/Mid/Long Memory Track 구현
- Memory Promotion Visualization 구현
- Memory Decay Visualization 구현
- Importance Score Visualization 구현
- Temporal Event Timeline 구현
- Memory Detail Panel 구현
- Timeline Filtering 구현
- Memory Transition Animation(optional) 구현
- AI Memory Summary Panel 구현
- 샘플 Timeline Visualization 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 실제 Cognitive Architecture
- Human-like Memory Simulation
- Reinforcement Memory Learning
- Real-time Streaming Memory
- Multi-agent Shared Memory
- Autonomous Memory Evolution
- 장기 자율 학습
- Dynamic Memory Compression
- Memory Fine-tuning
- Neural Memory Network

현재 TASK는
발표 가능한 Memory Lifecycle Visualization만 구현한다.

---

# 생성 대상 구조

```text
dashboard-ui/src/components/
├─ memory-timeline/
│  ├─ MemoryTimeline.tsx
│  ├─ MemoryTrack.tsx
│  ├─ MemoryNode.tsx
│  ├─ MemoryDetailPanel.tsx
│  ├─ MemoryLegend.tsx
│  ├─ MemoryToolbar.tsx
│  └─ MemorySummaryPanel.tsx
```

---

# 기술 스택

현재 Timeline Visualization 기술 스택:

```text
- Recharts
또는
- React Flow
또는
- custom timeline UI
```

현재 단계에서는
발표용 readability를 우선한다.

---

# Timeline 역할

현재 Memory Timeline 역할:

- 시장 이벤트 lifecycle 시각화
- Memory promotion 표시
- Memory decay 표시
- importance 변화 표시
- AI 기억 구조 설명
- 발표용 explainability 강화

---

# Memory Layer 대상

현재 Layer 대상:

```text
- short-term memory
- mid-term memory
- long-term memory
```

---

# Memory 예시

예상 흐름:

```text
NVIDIA 실적 발표
↓
short-term memory 저장
↓
HBM 시장 영향 지속
↓
mid-term memory promotion
↓
장기 산업 변화 판단
↓
long-term memory 저장
```

---

# Promotion 역할

현재 Promotion 역할:

- 중요 이벤트 유지
- 시장 영향 지속 이벤트 승격
- 장기 산업 변화 유지

---

# Decay 역할

현재 Decay 역할:

- 영향 감소 이벤트 제거
- relevance 감소 이벤트 축소
- memory importance 감소

---

# Importance Score 목표

예상 표시:

```text
NVIDIA HBM 수요 증가
importance_score: 0.91

중기 기억 유지 중
```

---

# Temporal Event 목표

예상 표시:

```text
2024-01
NVIDIA 실적 발표

↓

2024-02
HBM 공급 부족 심화

↓

2024-03
삼성전자 수혜 기대 증가
```

---

# UI 레이아웃 목표

예상 레이아웃:

```text
┌────────────────────────────────┐
│ Memory Toolbar                 │
├────────────────────────────────┤
│                                │
│      Memory Timeline           │
│                                │
├────────────────┬───────────────┤
│ Memory Detail  │ Memory Summary│
└────────────────┴───────────────┘
```

---

# Timeline 기능 목표

## Memory Node 기능

예상 기능:

```text
- memory hover
- memory click detail
- importance 표시
- promotion 표시
```

---

## Timeline 기능

예상 기능:

```text
- temporal flow 표시
- layer transition 표시
- event grouping 표시
```

---

## Toolbar 기능

예상 기능:

```text
- layer filter
- importance filter
- reset timeline
- focus event
```

---

# Summary Panel 역할

현재 Summary 역할:

- 현재 핵심 기억 표시
- 중요 시장 이벤트 표시
- 장기 기억 요약 표시

예상 표시:

```text
현재 AI 핵심 기억:

- HBM 공급 부족 지속
- AI 서버 투자 확대
- 삼성전자 메모리 수혜 가능성
```

---

# API 연동 대상

현재 API 연동 대상:

```text
GET /api/memory/latest
GET /api/memory/{trace_id}
GET /api/trace/{trace_id}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Memory Layer 재사용
- 기존 Temporal Memory 재사용
- 기존 Dashboard UI 재사용
- trace_id 기반 조회 유지
- 발표용 readability 우선
- Memory explainability 우선
- 작은 component 유지
- 과도한 animation 금지
- 과도한 abstraction 금지

---

# 예상 기능

## MemoryTimeline.tsx

역할:

- 전체 Timeline 렌더링
- temporal flow 관리

예상 기능:

```text
render_timeline()
update_timeline()
```

---

## MemoryTrack.tsx

역할:

- memory layer track 표시

예상 기능:

```text
render_short_term_track()
render_mid_term_track()
render_long_term_track()
```

---

## MemoryNode.tsx

역할:

- memory event 표시
- importance rendering

예상 기능:

```text
render_memory_node()
render_importance_badge()
```

---

## MemoryDetailPanel.tsx

역할:

- memory 상세 정보 표시

예상 기능:

```text
render_memory_details()
render_memory_history()
```

---

## MemoryToolbar.tsx

역할:

- timeline filtering
- event focus

예상 기능:

```text
filter_memory_layers()
filter_importance()
reset_timeline()
```

---

## MemorySummaryPanel.tsx

역할:

- 핵심 기억 요약 표시

예상 기능:

```text
render_memory_summary()
render_key_market_memories()
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 발표용 AI Memory 설명
- 시장 이벤트 lifecycle 설명
- importance 변화 설명
- Memory promotion 설명
- Temporal reasoning explainability 강화
```

현재 단계에서는
실시간 Cognitive AI를 구현하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Timeline Rendering 검증

- timeline 표시 여부
- memory layer 표시 여부
- event node 표시 여부

---

## Interaction 검증

- hover 동작 여부
- click detail 동작 여부
- event focus 동작 여부

---

## Promotion 검증

- promotion 표시 여부
- decay 표시 여부
- importance 표시 여부

---

## Summary 검증

- 핵심 기억 요약 표시 여부
- 장기 기억 표시 여부

---

## API 검증

- memory API 연동 여부
- trace API 연동 여부

---

## 구조 검증

- memory-timeline component 구조 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-028/
```

---

# 관련 Logs

```text
logs/TASK-028/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Memory Timeline Visualization 구축 완료
- memory layer rendering 성공
- promotion visualization 성공
- decay visualization 성공
- importance visualization 성공
- summary panel 성공
- 발표 가능한 memory explainability 확보
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-029-build-signal-evaluation-system
- TASK-030-build-portfolio-backtesting-suite
- TASK-031-build-sector-expansion-system

단,
현재 TASK에서는
실시간 Cognitive AI를 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- End-to-End traceability 유지
- Memory lifecycle explainability 유지
- Temporal reasoning 유지
- 발표 가능한 visualization 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지