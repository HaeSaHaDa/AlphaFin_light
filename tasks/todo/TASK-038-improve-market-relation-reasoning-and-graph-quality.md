# TASK-038-improve-market-relation-reasoning-and-graph-quality.md

# TASK-038 Market Relation Reasoning & Graph Quality 개선

## 상태

DOING

---

# 목표

현재 Market Relationship Graph는:

```text
selectedTicker 중심 Runtime Graph
```

구조까지는 확보되었으나,

관계 품질은 아직 일부:

```text
co-occurrence entity graph
retrieval adjacency graph
generic relation graph
```

수준일 가능성이 존재한다.

현재 TASK의 목표는:

```text
금융 시장 관계 reasoning
산업 관계 reasoning
공급망 reasoning
리스크 reasoning
시장 영향 reasoning
```

을 강화하여:

```text
"왜 이 기업이 움직이는가"
```

를 설득력 있게 설명하는
Explainable Market Intelligence Graph를 구축하는 것이다.

현재 단계에서는:

```text
Graph 동작 여부
```

보다:

```text
Graph 품질
Reasoning 품질
Relation 의미
```

개선에 집중한다.

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
→ Ticker-Centered Market Graph
```

현재 Runtime consistency는 확보되었고,
selectedTicker 중심 Graph도 구축되었다.

하지만 현재 Graph는 일부:

```text
단순 entity adjacency
뉴스 동시 등장 관계
약한 relation semantics
```

문제가 존재할 가능성이 있다.

현재 TASK에서는:

```text
시장 관계 reasoning 강화
```

를 수행한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Market Relation Reasoning 강화
- Industry Intelligence 강화
- Supply Chain Reasoning 강화
- Competitor Reasoning 강화
- Risk Exposure Reasoning 강화
- Macro Economic Reasoning 강화
- Theme Relation Reasoning 강화
- Relation Extraction 품질 개선
- Relation Type Classification 구축
- Relation Confidence Scoring 구축
- Relation Directionality 구축
- Market Impact Scoring 구축
- Node Importance Scoring 구축
- Graph Semantic Filtering 구축
- Noise Entity 제거
- Weak Relation 제거
- Graph Explainability 강화
- Relation Evidence 구축
- News-backed Relation 구축
- Retrieval-backed Relation 구축
- Tooltip Explanation 강화
- Graph Narrative 개선
- Dashboard Market Insight 개선
- Explainable Market Story 구축
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
- Neo4j 도입
- 분산 Graph DB
- Multi-agent 구조
- Kubernetes
- Multi-user SaaS

현재 TASK는:

```text
Graph Quality
+
Reasoning Quality
```

만 개선한다.

---

# 현재 문제

현재 Graph 문제:

```text
- 의미 없는 entity 연결
- 단순 동시 등장 relation
- edge 의미 약함
- 방향성 부족
- 시장 영향 구조 약함
- 공급망 설명 부족
- 리스크 설명 부족
- macro relation 부족
```

현재 Narrative 문제:

```text
왜 연결되는지 설명 부족
왜 상승/하락인지 설명 약함
```

---

# 목표 구조

현재 목표 구조:

```text
현대자동차
```

↓

관계 구조:

```text
전기차
배터리
현대모비스
IRA 정책
금리
중국 리스크
테슬라
```

↓

관계 유형:

```text
DEPENDS_ON
AFFECTED_BY
COMPETES_WITH
SUPPLIES
EXPOSED_TO
BENEFITS_FROM
```

↓

관계 설명:

```text
현대자동차는 IRA 정책 수혜 가능성이 존재함
```

---

# 생성 대상 구조

```text
dashboard-ui/src/reasoning/
├─ market-relation-reasoner.ts
├─ industry-intelligence.ts
├─ supply-chain-reasoner.ts
├─ macro-relation-reasoner.ts
├─ risk-exposure-reasoner.ts
├─ competitor-reasoner.ts
├─ relation-confidence.ts
├─ relation-direction.ts
├─ relation-evidence-builder.ts
└─ graph-semantic-filter.ts
```

```text
dashboard-ui/src/components/market-intelligence/
├─ MarketInsightPanel.tsx
├─ RelationExplanationCard.tsx
├─ RiskExposurePanel.tsx
├─ SupplyChainPanel.tsx
├─ MacroImpactPanel.tsx
└─ IndustryRelationPanel.tsx
```

---

# Market Reasoning 역할

현재 역할:

- 시장 영향 reasoning
- 산업 연결 reasoning
- 공급망 reasoning
- 리스크 reasoning
- macro reasoning

---

# Relation Reasoning 목표

현재 목표:

```text
단순 연결
```

이 아니라:

```text
왜 연결되는가
어떤 영향인가
상승 요인인가
하락 요인인가
```

설명 가능하도록 개선.

---

# Relation Type 목표

현재 목표 Relation:

| 유형 | 의미 |
|---|---|
| SUPPLIES | 공급 |
| COMPETES_WITH | 경쟁 |
| DEPENDS_ON | 의존 |
| AFFECTED_BY | 영향 받음 |
| BENEFITS_FROM | 수혜 |
| EXPOSED_TO | 리스크 노출 |
| RELATED_TO | 일반 관계 |

---

# Relation Confidence 목표

현재 목표:

```text
relation confidence score
```

추가.

예상:

```text
IRA 정책
→ 현대차
confidence: 0.82
```

---

# Market Impact 목표

현재 목표:

```text
상승 영향
하락 영향
중립 영향
```

구분.

예상:

```text
금리 상승
→ 자동차 업종 부담
```

---

# Supply Chain 목표

현재 목표:

```text
기업 간 공급망 연결
```

예상:

```text
삼성전기
→ MLCC 공급
→ 애플
→ 전장부품
```

---

# Macro Reasoning 목표

현재 목표:

```text
금리
환율
유가
IRA
중국 리스크
```

시장 관계 연결.

---

# Graph Semantic Filtering 목표

현재 목표:

```text
의미 없는 node 제거
약한 relation 제거
noise entity 제거
```

---

# Relation Evidence 목표

현재 목표:

```text
relation 근거 표시
```

예상:

```text
관련 뉴스
관련 retrieval chunk
관련 signal
```

---

# Tooltip Narrative 목표

현재 목표:

```text
왜 연결되는지 설명
왜 중요한지 설명
```

예상:

```text
중국 리스크:
현대차 중국 판매 둔화 가능성과 연결
```

---

# Market Insight 목표

현재 목표:

```text
AI가 시장을 어떻게 해석하는지
```

사용자 친화적으로 표시.

---

# API 연동 대상

현재 API 대상:

```text
GET /api/market-graph/{traceId}
GET /api/market-insight/{traceId}
GET /api/relation-explanation/{traceId}
GET /api/risk-exposure/{traceId}
```

---

# Relation Payload 예시

```json
{
  "source": "IRA 정책",
  "target": "현대자동차",
  "relation": "BENEFITS_FROM",
  "confidence": 0.82,
  "impact": "positive",
  "evidence": []
}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- selectedTicker 중심 유지
- traceId 기반 유지
- Runtime payload 기반 유지
- explainability 유지
- retrieval evidence 기반 유지
- OpenAI 호출 최소화 유지
- 발표 가능한 UX 유지
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## market-relation-reasoner.ts

역할:

- 시장 관계 reasoning

예상 기능:

```text
reasonMarketRelations()
```

---

## supply-chain-reasoner.ts

역할:

- 공급망 reasoning

예상 기능:

```text
buildSupplyChainRelations()
```

---

## macro-relation-reasoner.ts

역할:

- macro 영향 reasoning

예상 기능:

```text
reasonMacroImpact()
```

---

## relation-confidence.ts

역할:

- relation confidence 계산

예상 기능:

```text
calculateRelationConfidence()
```

---

## graph-semantic-filter.ts

역할:

- 의미 없는 relation 제거

예상 기능:

```text
filterWeakRelations()
removeNoiseEntities()
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- Explainable Market Intelligence
- AI 시장 reasoning 시각화
- 설득력 있는 Market Graph
- 발표 가능한 AI Market Story
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Relation 검증

- relation 의미 정상 여부
- edge direction 정상 여부
- confidence 정상 여부

---

## Reasoning 검증

- 시장 reasoning 품질 여부
- macro reasoning 정상 여부
- 공급망 reasoning 정상 여부

---

## Graph 검증

- noise entity 제거 여부
- weak relation 제거 여부
- graph relevance 정상 여부

---

## Narrative 검증

- tooltip 설명 품질 여부
- relation explanation 품질 여부

---

## Runtime 검증

- selectedTicker 기반 유지 여부
- traceId 기반 유지 여부
- Runtime payload 기반 유지 여부

---

## UX 검증

- 사용자 이해 가능 여부
- 발표 설득력 확보 여부

---

# 관련 Prompt

```text
prompts/TASK-038/
```

---

# 관련 Logs

```text
logs/TASK-038/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Market Relation Reasoning 강화 성공
- Relation Quality 개선 성공
- Graph Semantic Quality 개선 성공
- Supply Chain Reasoning 구축 성공
- Macro Reasoning 구축 성공
- Risk Reasoning 구축 성공
- Relation Explanation 구축 성공
- Explainable Market Intelligence 확보 성공
- 발표 가능한 AI Market Story 확보 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-039-build-portfolio-backtesting-suite
- TASK-040-build-backtesting-visualization
- TASK-041-build-presentation-demo-scenario

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- selectedTicker 중심 유지
- Runtime consistency 유지
- Runtime integrity 유지
- Market reasoning 품질 우선
- 발표 가능한 UX 유지
- OpenAI 비용 안정성 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지