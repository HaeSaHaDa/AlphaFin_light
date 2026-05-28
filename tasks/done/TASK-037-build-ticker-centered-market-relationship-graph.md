# TASK-037-build-ticker-centered-market-relationship-graph.md

# TASK-037 Ticker-Centered Market Relationship Graph 구축

## 상태

DONE

---

# 목표

현재 Event Graph / Stock Chain 구조는:

```text
retrieval entity visualization
```

수준에 가까우며,

실제:

```text
종목 중심 시장 관계 구조
산업 연결 구조
공급망 연결 구조
리스크 연결 구조
시장 영향 구조
```

를 충분히 표현하지 못한다.

현재 TASK의 목표는:

```text
selectedTicker 중심
```

으로:

```text
시장 관계 그래프
```

를 재구성하여:

```text
왜 이 종목이 움직이는가
무엇이 영향을 주는가
어떤 산업과 연결되는가
어떤 리스크가 연결되는가
```

를 사용자 친화적으로 시각화하는 것이다.

동시에:

```text
Sticky Runtime Header
+
Section Navigation
```

를 구축하여 Dashboard 탐색성과 발표 UX를 개선한다.

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
→ Runtime Query Flow
→ KOSPI200 Company Master
→ Dashboard Runtime Binding
→ Runtime Audit
```

현재 Runtime consistency는 확보되었으나,
Graph 구조는 여전히 일부:

```text
sample graph
generic entity graph
retrieval-only relation
```

수준일 가능성이 존재한다.

현재 TASK에서는:

```text
selectedTicker 중심
시장 관계 그래프
```

로 재구성한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- selectedTicker 중심 Event Graph 구축
- selectedTicker 중심 Stock Chain 구축
- Market Relationship Graph 설계
- Industry Relation Graph 구축
- Supply Chain Graph 구축
- Risk Relation Graph 구축
- Competitor Relation Graph 구축
- Entity Relationship Filtering 구축
- selectedTicker node 중심 고정
- traceId 기반 graph filtering 구축
- Runtime entity graph 구축
- News entity relation graph 구축
- Graph node category 시스템 구축
- Graph edge type 시스템 구축
- Graph relevance scoring 구축
- Graph visualization 개선
- Graph legend 구축
- Graph tooltip 구축
- Sticky Runtime Header 구축
- Dashboard Section Navigation 구축
- 현재 종목 상태 Header 구축
- Runtime status indicator 구축
- Section scroll navigation 구축
- Dashboard UX 개선
- 발표 UX 개선
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
- 3D Graph
- Neo4j 도입
- 분산 Graph DB
- Kubernetes
- Multi-user SaaS

현재 TASK는:

```text
시장 관계 시각화
+
Dashboard UX 개선
```

만 수행한다.

---

# 현재 문제

현재 그래프 문제:

```text
- 의미 없는 entity 연결
- node relevance 약함
- edge 의미 불명확
- 산업 관계 부족
- 공급망 관계 부족
- 리스크 관계 부족
- selectedTicker 중심성 부족
```

현재 Dashboard UX 문제:

```text
- 고정 Header 없음
- section 이동 어려움
- 현재 종목 인지 어려움
- 발표 흐름 불편
```

---

# 목표 구조

현재 목표 구조:

```text
selectedTicker:
삼성전기 009150
```

↓

중심 node:

```text
삼성전기
```

↓

관련 구조:

```text
MLCC
전장부품
삼성전자
애플
전기차
중국 리스크
반도체 업황
```

↓

관계 기반 edge 구성.

---

# 생성 대상 구조

```text
dashboard-ui/src/market-graph/
├─ market-graph-builder.ts
├─ relation-extractor.ts
├─ graph-filter.ts
├─ graph-score.ts
├─ graph-node-types.ts
├─ graph-edge-types.ts
├─ graph-tooltip-builder.ts
└─ graph-legend.ts
```

```text
dashboard-ui/src/components/market-graph/
├─ MarketRelationshipGraph.tsx
├─ MarketGraphLegend.tsx
├─ MarketGraphToolbar.tsx
├─ MarketGraphTooltip.tsx
├─ GraphNodeDetailPanel.tsx
└─ GraphEdgeInfoPanel.tsx
```

```text
dashboard-ui/src/components/runtime-header/
├─ StickyRuntimeHeader.tsx
├─ RuntimeStatusBadge.tsx
├─ SelectedTickerInfo.tsx
├─ RuntimeSectionNav.tsx
└─ RuntimeActionBar.tsx
```

---

# Graph 역할

현재 역할:

- 시장 관계 시각화
- 산업 연결 시각화
- 리스크 연결 시각화
- 공급망 연결 시각화
- 영향 구조 시각화

---

# Sticky Header 역할

현재 역할:

- 현재 종목 표시
- 현재 Runtime 상태 표시
- 빠른 section 이동
- 발표 UX 개선

---

# Graph Node 목표

현재 목표 Node 유형:

| 유형 | 예시 |
|---|---|
| Company | 삼성전기 |
| Sector | 반도체 |
| Product | MLCC |
| Risk | 중국 리스크 |
| Theme | 전기차 |
| Macro | 금리 |
| Competitor | 무라타 |
| Customer | 애플 |

---

# Graph Edge 목표

현재 목표 Edge 유형:

| 유형 | 의미 |
|---|---|
| SUPPLIES | 공급 |
| COMPETES | 경쟁 |
| IMPACTS | 영향 |
| DEPENDS_ON | 의존 |
| EXPOSED_TO | 리스크 노출 |
| RELATED_TO | 일반 연결 |

---

# selectedTicker 중심성 목표

현재 목표:

```text
선택 종목은 항상 center node
```

예상 규칙:

```text
삼성전기 선택
↓

삼성전기 중심 그래프
```

현재 제거 대상:

```text
generic sample graph
삼성전자 preset
NVIDIA preset
```

---

# Runtime Filtering 목표

현재 목표:

```text
selectedTicker
+
traceId
```

기준 entity filtering.

---

# Tooltip 목표

현재 목표:

```text
node 의미 설명
연결 이유 설명
관련 뉴스 표시
영향 방향 설명
```

예상:

```text
MLCC
삼성전기의 핵심 제품군
전장부품 수요 증가와 연결
```

---

# Sticky Header 목표

현재 목표 UI:

```text
┌─────────────────────────────────────┐
│ 삼성전기(009150) | Runtime Active │
│ [요약] [뉴스] [그래프] [메모리]   │
└─────────────────────────────────────┘
```

---

# Section Navigation 목표

현재 목표:

```text
클릭 시 해당 section scroll 이동
```

예상 Section:

```text
요약
뉴스
그래프
메모리
평가
Reflection
Retrieval
```

---

# Runtime Status 목표

현재 목표:

```text
Runtime Active
Retrieval Running
Analysis Complete
```

상태 표시.

---

# API 연동 대상

현재 API 대상:

```text
GET /api/stock-chain/{traceId}
GET /api/market-graph/{traceId}
GET /api/runtime-status/{traceId}
```

---

# Graph Payload 예시

```json
{
  "center_ticker": "009150",
  "center_company": "삼성전기",
  "nodes": [],
  "edges": [],
  "risks": [],
  "themes": []
}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- selectedTicker 중심 유지
- traceId 기반 유지
- Runtime payload 기반 유지
- explainability 유지
- OpenAI 호출 최소화 유지
- 발표 가능한 UX 유지
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## market-graph-builder.ts

역할:

- 시장 관계 graph 생성

예상 기능:

```text
buildMarketGraph()
buildTickerCenteredGraph()
```

---

## relation-extractor.ts

역할:

- entity 관계 추출

예상 기능:

```text
extractCompanyRelations()
extractRiskRelations()
```

---

## graph-filter.ts

역할:

- selectedTicker 기반 filtering

예상 기능:

```text
filterGraphByTicker()
```

---

## StickyRuntimeHeader.tsx

역할:

- 고정 Runtime Header

예상 기능:

```text
renderRuntimeHeader()
```

---

## RuntimeSectionNav.tsx

역할:

- section navigation

예상 기능:

```text
scrollToSection()
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 시장 관계 이해 강화
- Explainable Market Graph
- 발표 UX 강화
- Runtime 탐색성 강화
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Graph 검증

- selectedTicker 중심 여부
- graph relevance 정상 여부
- edge 의미 정상 여부
- 산업 연결 정상 여부

---

## Runtime 검증

- traceId 기반 graph 여부
- Runtime entity 기반 graph 여부

---

## Filtering 검증

- 삼성전기 선택 시 삼성전기 중심 여부
- 현대차 선택 시 현대차 중심 여부
- sample graph 제거 여부

---

## Header 검증

- Sticky Header 정상 여부
- 현재 종목 표시 여부
- Runtime 상태 표시 여부

---

## Navigation 검증

- section navigation 정상 여부
- scroll 이동 정상 여부

---

## UX 검증

- 발표 흐름 개선 여부
- Dashboard 탐색성 개선 여부

---

# 관련 Prompt

```text
prompts/TASK-037/
```

---

# 관련 Logs

```text
logs/TASK-037/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- selectedTicker 중심 Graph 구축 성공
- Market Relationship Graph 구축 성공
- Graph relevance 개선 성공
- Sticky Runtime Header 구축 성공
- Section Navigation 구축 성공
- Dashboard UX 개선 성공
- 발표 가능한 Market Graph 확보 성공
- Runtime consistency 유지 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-038-build-portfolio-backtesting-suite
- TASK-039-build-backtesting-visualization
- TASK-040-build-presentation-demo-scenario

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- selectedTicker 중심 유지
- Runtime consistency 유지
- Runtime integrity 유지
- 발표 가능한 UX 유지
- OpenAI 비용 안정성 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지