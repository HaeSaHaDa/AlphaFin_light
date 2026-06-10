# TASK-044-unify-navigation-and-remove-duplicated-menu-structure.md

# TASK-044 Navigation 통합 및 중복 메뉴 구조 제거

## 상태

DONE

---

# 목표

현재 Dashboard 구조는:

```text
Header
Sidebar
Detail Area
```

각 영역에 navigation과 action이 중복 배치되어 있으며:

```text
같은 이동 기능 반복
동일 action 다중 노출
전역 메뉴와 local 메뉴 혼합
```

문제가 발생하고 있다.

현재 TASK의 목표는:

```text
Global Navigation Architecture
```

를 정리하여:

```text
어디서 이동해야 하는지
직관적으로 이해 가능한 Runtime UX
```

를 만드는 것이다.

현재 단계에서는:

```text
신규 기능 추가
```

보다:

```text
Navigation 단순화
메뉴 역할 분리
Runtime UX 정리
플랫폼 탐색성 강화
```

에 집중한다.

---

# 배경

현재 프로젝트는:

```text
Persistent Runtime Shell
```

구조를 기반으로 발전해왔고,

현재:

```text
Header
Sidebar
Detail Panel
```

각각에 navigation/action이 혼합되어 있다.

예시 문제:

```text
Sidebar:
Graph 이동

Header:
Graph 버튼

Detail:
Graph 탭
```

처럼 동일 기능이 여러 위치에 존재한다.

현재 TASK에서는:

```text
Navigation Responsibility
```

를 명확히 분리한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Global Navigation 구조 정리
- 중복 메뉴 제거
- Header Navigation 정리
- Sidebar Navigation 정리
- Detail Local Navigation 정리
- Global Action 구조 정리
- Local Action 구조 정리
- Navigation Responsibility 분리
- Dead Navigation 제거
- Redundant Navigation 제거
- Runtime Navigation Hierarchy 구축
- Section Navigation 통합
- Breadcrumb 구조 정리
- Navigation Visual Priority 개선
- Mobile Navigation 정리
- Responsive Navigation 정리
- Navigation State Consistency 구축
- Current Route Highlight 개선
- selectedTicker Navigation 유지
- Runtime Context 유지
- Navigation UX 개선
- 발표 UX 개선
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 신규 AI 모델 추가
- 신규 Retrieval 알고리즘 추가
- Full UI Redesign
- Router 전체 교체
- Micro Frontend
- Multi-layout Architecture
- Backtesting
- Auto Trading
- Broker API
- HTS 기능
- Real-time Streaming
- Kubernetes
- Multi-user SaaS

현재 TASK는:

```text
Navigation Architecture
```

만 정리한다.

---

# 현재 문제

현재 문제:

```text
- Header와 Sidebar 메뉴 중복
- Detail 내부에도 전역 메뉴 존재
- 같은 action 여러 위치 노출
- navigation 역할 불명확
- 사용자가 어디서 이동해야 하는지 혼란
```

현재 UX 문제:

```text
- 플랫폼 탐색 흐름 불안정
- 발표 시 시선 흐름 분산
- 화면 복잡도 증가
```

---

# 목표 구조

현재 목표:

```text
Header
=
전역 상태 + Runtime 실행
```

```text
Sidebar
=
전역 화면 이동
```

```text
Detail
=
현재 화면 내부 세부 전환
```

---

# 목표 Navigation 구조

## Header 역할

현재 목표:

```text
- 종목 선택
- 검색 입력
- 분석 실행
- Runtime 상태 표시
- trace 상태 표시
```

Header에서는:

```text
전역 화면 이동 제거
```

---

## Sidebar 역할

현재 목표:

```text
전역 navigation 전용
```

예상 메뉴:

```text
Dashboard
News
Disclosure
Graph
Memory
Evaluation
Retrieval
Settings
```

Sidebar는:

```text
전역 화면 이동만 담당
```

---

## Detail 역할

현재 목표:

```text
현재 화면 내부 전환만 담당
```

예상:

```text
Graph View
Evidence View
Timeline View
```

또는:

```text
Short Memory
Mid Memory
Long Memory
```

---

# 생성 대상 구조

```text
dashboard-ui/src/navigation/
├─ navigation-policy.ts
├─ navigation-responsibility.ts
├─ global-navigation-map.ts
├─ local-navigation-map.ts
├─ navigation-priority.ts
└─ route-visibility.ts
```

```text
dashboard-ui/src/components/navigation-cleanup/
├─ GlobalNavigation.tsx
├─ SidebarNavigation.tsx
├─ DetailLocalNavigation.tsx
├─ RuntimeBreadcrumb.tsx
├─ NavigationDivider.tsx
└─ NavigationGroup.tsx
```

---

# Navigation Responsibility 목표

현재 목표:

| 영역 | 책임 |
|---|---|
| Header | Runtime 실행/상태 |
| Sidebar | 전역 이동 |
| Detail | 로컬 전환 |

---

# 제거 대상

현재 제거 대상:

```text
- Header 내 중복 화면 이동 버튼
- Detail 내부 전역 메뉴
- 중복 Graph 버튼
- 중복 News 버튼
- dead navigation
- placeholder route
```

---

# Navigation Priority 목표

현재 목표:

```text
전역 이동
>
현재 화면
>
세부 보기
```

순서 유지.

---

# Current Route 목표

현재 목표:

```text
현재 위치 명확히 강조
```

예상:

```text
active route highlight
```

---

# Mobile Navigation 목표

현재 목표:

```text
모바일에서:
Sidebar Drawer
+
Detail Navigation Collapse
```

---

# Runtime Context 목표

현재 목표:

```text
navigation 이동 시:
selectedTicker 유지
traceId 유지
Runtime 상태 유지
```

---

# Breadcrumb 목표

현재 목표:

```text
현재 위치 표시
```

예상:

```text
Dashboard > Graph > Evidence
```

---

# Navigation UX 목표

현재 목표:

```text
처음 보는 사용자도:
어디서 이동해야 하는지 즉시 이해 가능
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- selectedTicker 유지
- traceId 유지
- Runtime consistency 유지
- Header 역할 최소화
- Sidebar 역할 명확화
- Detail 역할 분리
- 발표 가능한 UX 유지
- 기존 Runtime Flow 유지
- 기존 Retrieval 구조 유지
- OpenAI 호출 최소화 유지
- 과도한 abstraction 금지

---

# 예상 기능

## navigation-policy.ts

역할:

```text
navigation 책임 정의
```

예상 기능:

```text
resolveNavigationScope()
```

---

## global-navigation-map.ts

역할:

```text
전역 메뉴 정의
```

예상 기능:

```text
buildGlobalNavigation()
```

---

## local-navigation-map.ts

역할:

```text
Detail 내부 메뉴 정의
```

예상 기능:

```text
buildLocalNavigation()
```

---

## route-visibility.ts

역할:

```text
현재 route visibility 제어
```

예상 기능:

```text
shouldRenderNavigation()
```

---

# 검증 항목

현재 TASK 완료 전 다음 항목을 반드시 검증한다.

## Navigation 검증

- Header/Sidebar 메뉴 중복 제거 여부
- Detail 내부 전역 메뉴 제거 여부
- dead navigation 제거 여부

---

## UX 검증

- 어디서 이동해야 하는지 직관적인지
- 현재 위치 인지 가능한지
- 발표 시 흐름 안정적인지

---

## Runtime 검증

- selectedTicker 유지 여부
- traceId 유지 여부
- Runtime Context 유지 여부

---

## Responsive 검증

- Desktop 정상 여부
- Mobile navigation 정상 여부

---

# 관련 Prompt

```text
prompts/TASK-044/
```

---

# 관련 Logs

```text
logs/TASK-044/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Navigation Responsibility 분리 성공
- Header/Sidebar 역할 분리 성공
- 중복 메뉴 제거 성공
- dead navigation 제거 성공
- Global Navigation 구조 정리 성공
- Detail Navigation 구조 정리 성공
- 발표 가능한 Navigation UX 확보 성공
- Runtime consistency 유지 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후 다음 작업 후보:

- TASK-045-build-runtime-end-to-end-verification
- TASK-046-build-presentation-demo-scenario
- TASK-047-build-portfolio-backtesting-suite

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- Runtime consistency 유지
- selectedTicker 중심 유지
- Navigation 단순성 유지
- 발표 가능한 UX 유지
- OpenAI 비용 안정성 유지
- 과도한 Autonomous AI 구조 금지
