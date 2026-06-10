# TASK-030-refine-dashboard-report-ux.md

# TASK-030 Dashboard Report UX 리디자인

## 상태

DONE

---

# 목표

현재 개발자 중심 Dashboard를
한국어 친화적이고
발표 가능한 형태의:

```text
AI 시장 분석 리포트
```

스타일로 리디자인한다.

현재 TASK의 목표는
엔진 내부 기능을 숨기는 것이 아니라,
사용자가:

```text
왜 상승/하락으로 판단했는가
어떤 뉴스가 영향을 줬는가
어떤 기업이 연결돼 있는가
어떤 리스크를 봤는가
AI가 어떻게 분석했는가
```

를 처음 봐도 이해 가능한 구조로
재배치하는 것이다.

현재 단계에서는
새로운 AI 기능 추가보다
정보 구조(UX)와 Explainability 표현 개선에 집중한다.

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
→ Reflection
→ Layered Memory
→ Temporal Market Memory
→ Stock Chain
→ Signal Evaluation
→ Dashboard Visualization
```

현재 시스템은:

```text
개발자 중심 explainability dashboard
```

에 가까운 상태다.

현재 구조는 기능은 충분하지만:

```text
처음 보는 사용자가 이해하기 어렵다
```

는 문제가 존재한다.

현재 TASK에서는:

```text
기능 중심 UI
→
스토리 중심 금융 분석 리포트 UI
```

로 전환한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Dashboard 전체 정보 구조 리디자인
- 한국어 친화적 용어 적용
- 상단 AI 시장 분석 리포트 영역 구축
- 현재 관점 Panel 구축
- 상승 요인 Panel 구축
- 리스크 Panel 구축
- 관련 뉴스 Panel 구축
- 시장 연결 구조 영역 재배치
- AI 분석 과정 Accordion UI 구축
- 시장 기억 변화 Viewer 재배치
- Signal Evaluation Summary 재배치
- 모바일/발표 화면 readability 개선
- 카드 기반 UI 정리
- UX 흐름 개선
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 신규 AI 모델 추가
- 신규 Retrieval 구조 추가
- 신규 Memory 구조 추가
- 신규 Reflection 구조 추가
- Backtesting Engine
- 실시간 Streaming
- Multi-user Dashboard
- HTS 스타일 Trading UI
- Auto Trading UI
- 실시간 주문 기능
- 복잡한 Admin 시스템

현재 TASK는
UX/Explainability 개선만 수행한다.

---

# UX 핵심 방향

현재 방향:

```text
개발자 로그
```

↓

목표 방향:

```text
AI 시장 분석 리포트
```

---

# 핵심 UX 원칙

현재 Dashboard는:

```text
AI 내부 구조를 보여주되,
사람이 이해 가능한 언어로 번역
```

해야 한다.

---

# 최종 화면 구조 목표

```text
┌────────────────────────────────┐
│ AI 시장 분석 리포트            │
├────────────────────────────────┤
│ 현재 관점 / 신뢰도             │
├──────────────┬─────────────────┤
│ 상승 요인    │ 리스크          │
├────────────────────────────────┤
│ 관련 뉴스 / 시장 영향          │
├────────────────────────────────┤
│ 시장 연결 구조(Event Graph)    │
├────────────────────────────────┤
│ AI 분석 과정 ▼                 │
├────────────────────────────────┤
│ AI 참고 자료                   │
│ AI 자기 검토                   │
│ 시장 기억 변화                 │
│ 분석 신뢰도                    │
│ Signal 평가                    │
└────────────────────────────────┘
```

---

# 생성 대상 구조

```text
dashboard-ui/src/components/
├─ report-layout/
│  ├─ MarketReportHeader.tsx
│  ├─ SignalSummaryCard.tsx
│  ├─ BullishFactorsPanel.tsx
│  ├─ RiskFactorsPanel.tsx
│  ├─ RelatedNewsPanel.tsx
│  ├─ MarketImpactPanel.tsx
│  ├─ ExplainabilityAccordion.tsx
│  ├─ AnalysisFlowPanel.tsx
│  └─ DashboardSection.tsx
```

---

# 상단 리포트 역할

현재 역할:

- AI 현재 관점 표시
- 핵심 상승 이유 표시
- 주요 리스크 표시
- 시장 영향 표시
- 사용자 이해도 향상

---

# 현재 관점 Panel 목표

예상 표시:

```text
현재 관점:
긍정

분석 신뢰도:
82%
```

---

# 상승 요인 Panel 목표

예상 표시:

```text
- HBM 수요 증가
- AI 서버 투자 확대
- 메모리 가격 상승 기대
```

---

# 리스크 Panel 목표

예상 표시:

```text
- 글로벌 경기 둔화
- 공급 과잉 가능성
- 경쟁 심화
```

---

# 관련 뉴스 Panel 목표

예상 표시:

```text
NVIDIA 실적 호조
HBM 공급 부족 지속
AI 서버 투자 증가
```

---

# 시장 연결 구조 역할

현재 역할:

- 기업/산업 관계 표시
- 공급망 흐름 표시
- 시장 영향 propagation 표시

현재 TASK에서는:

```text
중단 핵심 영역
```

으로 배치한다.

---

# AI 분석 과정 역할

현재 역할:

- AI 내부 reasoning 설명
- explainability 제공
- 교수/개발자용 내부 구조 표시

---

# Accordion 구조 목표

기본:

```text
접힌 상태
```

↓

필요 시 펼침:

```text
AI 참고 자료
AI 자기 검토
시장 기억 변화
분석 신뢰도
Signal 평가
```

---

# 한국어 친화적 용어 목표

| 기존 용어 | 사용자 표현 |
|---|---|
| Retrieval | AI가 참고한 자료 |
| Reflection | AI 자기 검토 |
| Memory Layer | 시장 기억 |
| Trace | 분석 과정 |
| Stock Chain | 시장 연결 구조 |
| Chunk | 참고 문서 |
| Similarity Score | 관련도 |
| Propagation | 영향 흐름 |
| bullish | 긍정 |
| bearish | 부정 |
| confidence | 분석 신뢰도 |

---

# 모바일/발표 UX 목표

현재 목표:

- 카드 기반 UI
- 큰 제목
- 간결한 설명
- 발표 화면 readability 강화
- 복잡한 개발자 용어 제거
- 중요 정보 우선 배치

---

# API 연동 대상

현재 API 연동 대상:

```text
GET /api/retrieval/{trace_id}
GET /api/reflection/{trace_id}
GET /api/memory/{trace_id}
GET /api/stock-chain/{trace_id}
GET /api/evaluation/{trace_id}
GET /api/signal/{trace_id}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Engine 구조 재사용
- 기존 Dashboard API 재사용
- 기존 Event Graph 재사용
- 기존 Memory Timeline 재사용
- trace_id 기반 유지
- 발표용 readability 우선
- 한국어 UX 우선
- 작은 component 유지
- 과도한 animation 금지
- 과도한 abstraction 금지

---

# 예상 기능

## MarketReportHeader.tsx

역할:

- 상단 분석 요약 표시

예상 기능:

```text
render_market_summary()
render_signal_summary()
```

---

## SignalSummaryCard.tsx

역할:

- 현재 관점 표시

예상 기능:

```text
render_signal()
render_confidence()
```

---

## BullishFactorsPanel.tsx

역할:

- 상승 요인 표시

예상 기능:

```text
render_bullish_factors()
```

---

## RiskFactorsPanel.tsx

역할:

- 리스크 표시

예상 기능:

```text
render_risk_factors()
```

---

## RelatedNewsPanel.tsx

역할:

- 관련 뉴스 표시

예상 기능:

```text
render_related_news()
```

---

## ExplainabilityAccordion.tsx

역할:

- AI 내부 과정 표시

예상 기능:

```text
toggle_analysis_flow()
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 발표용 금융 AI 리포트
- 사용자 이해도 향상
- Explainability UX 강화
- AI 내부 구조 설명
- 스토리 기반 Dashboard 구성
```

현재 단계에서는
Backtesting을 구현하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## 리포트 구조 검증

- 상단 분석 리포트 표시 여부
- 현재 관점 표시 여부
- 상승 요인 표시 여부
- 리스크 표시 여부

---

## UX 검증

- 한국어 친화적 용어 적용 여부
- 발표 화면 readability 여부
- 정보 우선순위 정상 여부

---

## Accordion 검증

- AI 분석 과정 toggle 여부
- 내부 explainability 표시 여부

---

## 구조 검증

- 기존 Event Graph 유지 여부
- 기존 Memory Timeline 유지 여부
- TASK 범위 외 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-030/
```

---

# 관련 Logs

```text
logs/TASK-030/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Dashboard UX 리디자인 성공
- 상단 AI 시장 분석 리포트 구축 성공
- 현재 관점 Panel 구축 성공
- 상승 요인/리스크 Panel 구축 성공
- 시장 연결 구조 재배치 성공
- AI 분석 과정 Accordion 구축 성공
- 한국어 친화적 UX 적용 성공
- 발표 가능한 Dashboard 확보 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-031-build-portfolio-backtesting-suite
- TASK-032-build-sector-expansion-system
- TASK-033-build-context-optimization-system

단,
현재 TASK에서는
Backtesting을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- End-to-End traceability 유지
- 사용자 이해 가능성 우선
- 발표 가능한 UX 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지
