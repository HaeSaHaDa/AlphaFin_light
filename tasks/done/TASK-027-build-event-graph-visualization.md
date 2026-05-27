# TASK-027-build-event-graph-visualization.md

# TASK-027 Event Graph Visualization 구축

## 상태

DONE

---

# 완료 결과

- React Flow Event Graph 페이지 구축
- propagation · temporal · filtering · node detail 완료

---

# 관련 문서

```text
prompts/TASK-027/prompt-001.md
logs/TASK-027/result-001.md
```

---

# 목표

Financial AI Engine 내부의
기업 관계, 공급망 관계, 시장 이벤트 propagation을
시각적으로 표현하는
Event Graph Visualization을 구축한다.

현재 TASK의 목표는
텍스트 기반 Stock Chain 표시를 넘어,
실제 그래프 형태로:

```text
기업
→ 산업
→ 제품
→ 이벤트
→ 시장 영향
```

연결 구조를 직관적으로 표현하는 것이다.

현재 단계에서는
복잡한 실시간 graph engine보다
발표 가능한 interactive graph visualization에 집중한다.

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
```

현재 시스템은:

```text
Stock Chain 텍스트 조회
```

까지 가능하다.

하지만 현재 구조는:

```text
시장 관계 구조를 직관적으로 표현
```

하지 못한다.

현재 TASK에서는
시장 관계 구조를 Graph 기반으로 시각화한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Event Graph Visualization Component 구현
- Graph Node Renderer 구현
- Graph Edge Renderer 구현
- Propagation Flow Visualization 구현
- Interactive Node Detail Panel 구현
- Relation Tooltip 구현
- Impact Score Visualization 구현
- Graph Filtering 구현
- Entity Highlighting 구현
- Temporal Relation 표시 구현
- 샘플 Graph Visualization 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Neo4j Visualization
- Realtime Graph Streaming
- Cytoscape 고급 최적화
- 대규모 Graph Clustering
- 실시간 시장 Network 분석
- GPU Graph Rendering
- Knowledge Graph Database
- Autonomous Causal Discovery
- Dynamic Graph Learning
- 실시간 투자 추천 Graph
- Multi-user Graph Collaboration

현재 TASK는
발표 가능한 Graph Visualization만 구현한다.

---

# 생성 대상 구조

```text
dashboard-ui/src/components/
├─ event-graph/
│  ├─ EventGraph.tsx
│  ├─ GraphNode.tsx
│  ├─ GraphEdge.tsx
│  ├─ GraphLegend.tsx
│  ├─ NodeDetailPanel.tsx
│  ├─ PropagationPanel.tsx
│  └─ GraphToolbar.tsx
```

---

# 기술 스택

현재 Graph Visualization 기술 스택:

```text
- React Flow
또는
- vis-network
또는
- Recharts 기반 custom graph
```

현재 단계에서는
구현 단순성을 우선한다.

---

# Graph 역할

현재 Event Graph 역할:

- 기업 관계 시각화
- 공급망 propagation 시각화
- 산업 영향 흐름 시각화
- Retrieval reasoning 보조
- 발표용 explainability 강화

---

# Graph Node 대상

현재 Node 대상:

```text
- 기업
- 산업
- 제품
- 시장 이벤트
- 기술
- 가격 요소
```

예시:

```text
NVIDIA
HBM
삼성전자
SK하이닉스
AI 서버
DRAM 가격
```

---

# Graph Edge 대상

현재 Edge 대상:

```text
- demand propagation
- supply chain relation
- price impact
- market influence
- temporal relation
```

---

# Graph 예시

예상 Graph 흐름:

```text
NVIDIA
↓
AI GPU 수요 증가
↓
AI 서버 확대
↓
HBM 수요 증가
↓
삼성전자 수혜 가능성
↓
DRAM 가격 상승
```

---

# Propagation Visualization 역할

현재 Propagation 역할:

- 이벤트 영향 흐름 표시
- 시장 영향 방향 표시
- relation strength 표시
- impact score 표시

---

# Impact Score 목표

예상 표시:

```text
NVIDIA → HBM
impact_score: 0.91

HBM → 삼성전자
impact_score: 0.84
```

---

# Temporal Relation 목표

예상 표시:

```text
2024-01
NVIDIA 실적 발표

↓

2024-02
HBM 공급 부족 심화

↓

2024-03
DRAM 가격 상승
```

---

# UI 레이아웃 목표

예상 레이아웃:

```text
┌────────────────────────────────┐
│ Graph Toolbar                  │
├────────────────────────────────┤
│                                │
│       Event Graph Canvas       │
│                                │
├────────────────┬───────────────┤
│ Node Detail    │ Propagation   │
└────────────────┴───────────────┘
```

---

# Graph 기능 목표

## Node 기능

예상 기능:

```text
- hover highlight
- click detail
- relation focus
- entity type color
```

---

## Edge 기능

예상 기능:

```text
- impact score 표시
- propagation direction 표시
- relation tooltip 표시
```

---

## Toolbar 기능

예상 기능:

```text
- relation filter
- node type filter
- reset graph
- focus entity
```

---

# API 연동 대상

현재 API 연동 대상:

```text
GET /api/stock-chain/latest
GET /api/stock-chain/{ticker}
GET /api/trace/{trace_id}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Stock Chain 재사용
- 기존 Dashboard UI 재사용
- 기존 Retrieval Viewer 유지
- trace_id 기반 조회 유지
- 발표용 readability 우선
- interactive graph 우선
- 작은 component 유지
- 과도한 animation 금지
- 과도한 abstraction 금지

---

# 예상 기능

## EventGraph.tsx

역할:

- 전체 Graph 렌더링
- node/edge 관리

예상 기능:

```text
render_graph()
update_graph()
```

---

## GraphNode.tsx

역할:

- node 표시
- entity rendering

예상 기능:

```text
render_node()
highlight_node()
```

---

## GraphEdge.tsx

역할:

- edge 표시
- propagation rendering

예상 기능:

```text
render_edge()
render_impact_score()
```

---

## NodeDetailPanel.tsx

역할:

- node 상세 정보 표시
- related relation 표시

예상 기능:

```text
render_node_details()
render_related_entities()
```

---

## PropagationPanel.tsx

역할:

- propagation 흐름 표시
- impact sequence 표시

예상 기능:

```text
render_propagation_flow()
render_temporal_chain()
```

---

## GraphToolbar.tsx

역할:

- graph filtering
- entity focus

예상 기능:

```text
filter_relations()
focus_entity()
reset_graph()
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 발표용 market reasoning 시각화
- 공급망 영향 설명
- Event propagation 설명
- Stock Chain explainability 강화
- 시장 관계 구조 설명
```

현재 단계에서는
실시간 시장 Network 분석을 수행하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Graph Rendering 검증

- node 표시 여부
- edge 표시 여부
- graph layout 정상 여부

---

## Interaction 검증

- hover 동작 여부
- click detail 동작 여부
- relation highlight 동작 여부

---

## Propagation 검증

- propagation flow 표시 여부
- impact score 표시 여부
- relation direction 표시 여부

---

## Toolbar 검증

- graph filter 동작 여부
- entity focus 동작 여부
- graph reset 동작 여부

---

## API 검증

- stock-chain API 연동 여부
- trace API 연동 여부

---

## 구조 검증

- event-graph component 구조 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-027/
```

---

# 관련 Logs

```text
logs/TASK-027/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Event Graph Visualization 구축 완료
- node rendering 성공
- edge rendering 성공
- propagation visualization 성공
- node detail panel 성공
- graph filtering 성공
- 발표 가능한 graph visualization 확보
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-028-build-memory-timeline-visualization
- TASK-029-build-signal-evaluation-system
- TASK-030-build-portfolio-backtesting-suite

단,
현재 TASK에서는
실시간 투자 recommendation 시스템을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- End-to-End traceability 유지
- Stock Chain explainability 유지
- Memory lifecycle 유지
- 발표 가능한 visualization 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지