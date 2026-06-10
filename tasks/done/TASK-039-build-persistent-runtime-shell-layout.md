# TASK-039-build-persistent-runtime-shell-layout.md

# TASK-039 Persistent Runtime Shell Layout 구축

## 상태

DONE

---

# 목표

현재 Dashboard 구조는:

```text
page-level layout
local navigation
section-level UI
```

기반으로 동작하고 있으며,

페이지 이동 또는 특정 section 진입 시:

```text
메뉴 위치 변경
검색창 사라짐
현재 종목 정보 사라짐
Runtime context 단절
navigation 초기화
```

문제가 발생하고 있다.

현재 TASK의 목표는:

```text
Persistent Runtime Shell Layout
```

를 구축하여:

```text
어느 화면에서도
Runtime Context가 유지되는
금융 AI 플랫폼 UX
```

를 만드는 것이다.

현재 단계에서는:

```text
기능 추가
```

보다:

```text
플랫폼 UX
탐색성
Runtime Context 유지
발표 안정성
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
→ Runtime Query Flow
→ KOSPI200 Company Master
→ Dashboard Runtime Binding
→ Runtime Audit
→ Market Relationship Graph
→ Market Relation Reasoning
```

현재 Runtime 기능은 상당 수준 구축되었으나,
UI 구조는 여전히:

```text
개발용 Dashboard
```

느낌이 강하다.

현재 TASK에서는:

```text
Persistent Runtime Platform Layout
```

를 구축한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Global Persistent Shell 구축
- Persistent Runtime Header 구축
- Persistent Sidebar 구축
- Runtime Context 유지 구조 구축
- selectedTicker Global Persistence 구축
- traceId Global Persistence 구축
- Global Navigation 구축
- Runtime Search Bar Persistent화
- Runtime Status Bar 구축
- Runtime Footer 구축
- Section Navigation 통합
- Current Page Highlight 구축
- Responsive Sidebar 구축
- Sidebar Collapse 기능 구축
- Page Transition Context 유지
- Layout State Persistence 구축
- Runtime Header Search 구축
- Dashboard Workspace 구조 구축
- Layout Scroll 구조 개선
- Sticky Header 안정화
- z-index hierarchy 정리
- Dashboard 탐색성 개선
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
- UI Full Redesign
- Multi-user SaaS
- Kubernetes

현재 TASK는:

```text
Platform Shell UX
```

만 구축한다.

---

# 현재 문제

현재 문제:

```text
특정 화면 진입 시 메뉴 변경
검색창 사라짐
현재 종목 확인 어려움
navigation 위치 변경
Runtime Context 단절
```

현재 UX 문제:

```text
- 긴 스크롤 페이지 느낌
- section 이동 불편
- 플랫폼 느낌 부족
- 발표 흐름 끊김
```

---

# 목표 구조

현재 목표 구조:

```text
┌──────────────────────────────────────────┐
│ Global Runtime Header                   │
│ 종목선택 | 검색 | Runtime 상태          │
├──────────────┬───────────────────────────┤
│ Sidebar      │ Main Runtime Workspace    │
│              │                           │
│ Dashboard    │ Summary                   │
│ News         │ News                      │
│ Graph        │ Graph                     │
│ Memory       │ Memory                    │
│ Evaluation   │ Evaluation                │
│ Disclosure   │ Disclosure                │
│ Retrieval    │ Retrieval                 │
│              │                           │
├──────────────┴───────────────────────────┤
│ Runtime Footer Status                   │
└──────────────────────────────────────────┘
```

---

# 생성 대상 구조

```text
dashboard-ui/src/layout/
├─ runtime-shell/
│  ├─ RuntimeShellLayout.tsx
│  ├─ RuntimeHeader.tsx
│  ├─ RuntimeSidebar.tsx
│  ├─ RuntimeFooter.tsx
│  ├─ RuntimeWorkspace.tsx
│  ├─ RuntimeShellProvider.tsx
│  └─ RuntimeLayoutState.ts
```

```text
dashboard-ui/src/components/navigation/
├─ SidebarMenu.tsx
├─ SidebarSection.tsx
├─ RuntimeBreadcrumb.tsx
├─ RuntimePageTabs.tsx
├─ RuntimeQuickActions.tsx
└─ RuntimeStatusIndicator.tsx
```

```text
dashboard-ui/src/components/runtime-header/
├─ GlobalTickerSelector.tsx
├─ GlobalRuntimeSearch.tsx
├─ GlobalTraceStatus.tsx
├─ GlobalSectionNav.tsx
└─ GlobalRuntimeActions.tsx
```

---

# Persistent Header 역할

현재 역할:

- 현재 selectedTicker 표시
- Runtime 상태 표시
- 검색창 유지
- traceId 상태 유지
- 빠른 navigation 제공

---

# Persistent Sidebar 역할

현재 역할:

- 전체 Runtime navigation
- 현재 page highlight
- section 이동
- platform 탐색성 강화

---

# Runtime Workspace 역할

현재 역할:

- 실제 Dashboard rendering 영역
- Runtime Context 공유
- Layout consistency 유지

---

# Runtime Footer 역할

현재 역할:

- Runtime 상태 표시
- ingestion 상태 표시
- retrieval 상태 표시
- cache 상태 표시

---

# Sidebar Menu 목표

현재 목표 메뉴:

| 메뉴 | 역할 |
|---|---|
| Dashboard | 전체 요약 |
| News | 뉴스 분석 |
| Graph | Market Graph |
| Memory | Memory Layer |
| Evaluation | Signal 평가 |
| Disclosure | 공시 분석 |
| Retrieval | Retrieval Viewer |
| Settings | Runtime 설정 |

---

# Header 목표

현재 목표 Header:

```text
현재 종목:
삼성전기 (009150)

Runtime:
Active

Trace:
trace_001
```

---

# Runtime Context 목표

현재 목표:

```text
페이지 이동 후에도:
- selectedTicker 유지
- traceId 유지
- 검색 상태 유지
- Runtime 상태 유지
```

---

# Layout Persistence 목표

현재 목표:

```text
sidebar state 유지
current section 유지
workspace state 유지
```

---

# Responsive 목표

현재 목표:

```text
Desktop:
Persistent Sidebar

Tablet:
Collapsible Sidebar

Mobile:
Drawer Sidebar
```

---

# Scroll 구조 목표

현재 목표:

```text
Header 고정
Sidebar 고정
Workspace만 scroll
```

---

# Navigation 목표

현재 목표:

```text
현재 page highlight
현재 section highlight
smooth scroll 이동
```

---

# Runtime Status 목표

현재 목표 상태:

```text
Runtime Active
Retrieval Running
Ingestion Running
Cache Hit
Analysis Complete
```

---

# API 연동 대상

현재 API 대상:

```text
GET /api/runtime-status/{traceId}
GET /api/runtime-context
```

---

# Layout State 예시

```json
{
  "selectedTicker": "009150",
  "traceId": "trace_001",
  "sidebarCollapsed": false,
  "currentSection": "graph",
  "runtimeStatus": "active"
}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- selectedTicker global persistence 유지
- traceId global persistence 유지
- Runtime consistency 유지
- explainability 유지
- 기존 Runtime Flow 유지
- 기존 Retrieval 구조 유지
- OpenAI 호출 최소화 유지
- 발표 가능한 UX 유지
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## RuntimeShellLayout.tsx

역할:

- 전체 Runtime Shell 관리

예상 기능:

```text
renderRuntimeShell()
```

---

## RuntimeHeader.tsx

역할:

- Persistent Runtime Header

예상 기능:

```text
renderGlobalRuntimeHeader()
```

---

## RuntimeSidebar.tsx

역할:

- Persistent Sidebar

예상 기능:

```text
renderRuntimeSidebar()
```

---

## RuntimeShellProvider.tsx

역할:

- Runtime Layout State 관리

예상 기능:

```text
persistRuntimeLayout()
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 금융 AI 플랫폼 느낌 강화
- Runtime 탐색성 강화
- 발표 UX 강화
- Context 유지 강화
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Header 검증

- Header persistent 여부
- 검색창 유지 여부
- selectedTicker 유지 여부

---

## Sidebar 검증

- Sidebar persistent 여부
- 현재 page highlight 여부
- section 이동 여부

---

## Runtime 검증

- traceId 유지 여부
- Runtime 상태 유지 여부
- context 유지 여부

---

## Navigation 검증

- page 이동 시 menu 유지 여부
- scroll 구조 정상 여부

---

## Responsive 검증

- Desktop 정상 여부
- Tablet 정상 여부
- Mobile 기본 동작 여부

---

## UX 검증

- 플랫폼 느낌 강화 여부
- 발표 흐름 개선 여부
- 탐색성 개선 여부

---

# 관련 Prompt

```text
prompts/TASK-039/
```

---

# 관련 Logs

```text
logs/TASK-039/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Persistent Runtime Shell 구축 성공
- Persistent Header 구축 성공
- Persistent Sidebar 구축 성공
- Runtime Context Persistence 성공
- selectedTicker persistence 성공
- traceId persistence 성공
- Dashboard 탐색성 개선 성공
- 발표 가능한 Platform UX 확보 성공
- Runtime consistency 유지 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-040-build-disclosure-document-store
- TASK-041-build-event-consolidation-and-memory-deduplication
- TASK-042-build-portfolio-backtesting-suite

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- Runtime consistency 유지
- Runtime context persistence 유지
- selectedTicker 중심 유지
- 발표 가능한 UX 유지
- OpenAI 비용 안정성 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지