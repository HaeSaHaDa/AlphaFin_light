# AlphaFin LTE 아키텍처 개요

## 문서 목적

이 문서는 현재 구현된 AlphaFin LTE의 전체 구성과 주요 데이터 흐름을 설명한다.

---

# 전체 시스템 구조

```text
Next.js Dashboard
    ↓ HTTP
FastAPI Dashboard API
    ↓
Runtime Query
    ↓
Company Resolve / Ingestion
    ↓
News Retrieval + Disclosure Retrieval
    ↓
Unified Context
    ↓
OpenAI Analysis / Evaluation / Reflection
    ↓
Memory / Event Graph / Stock Chain
    ↓
trace_id 결과 저장
    ↓
Dashboard Panel 조회
```

---

# 주요 구성

## Frontend

위치:

```text
dashboard-ui/
```

역할:

- 종목 선택과 Runtime Query 실행
- trace 기반 Dashboard panel 조회
- News, Disclosure, Event, Graph, Memory, Evaluation 표시
- selectedTicker와 traceId 유지

## Backend API

위치:

```text
src/dashboard_api/
```

역할:

- FastAPI route 등록
- Runtime 실행
- trace 기반 결과 조회
- Retrieval, Memory, Event, Disclosure 응답 조립

## Runtime

위치:

```text
src/runtime_flow/
src/runtime_query/
```

역할:

- company resolve
- ingestion 상태 확인
- 뉴스와 공시 evidence 통합
- unified engine 실행
- trace와 Dashboard bundle 생성

## Retrieval 및 LLM Engine

위치:

```text
src/rag/
```

역할:

- embedding
- ticker filtered retrieval
- context assembly
- LLM analysis
- evaluation과 reflection
- memory, graph, stock chain 생성

## Disclosure

위치:

```text
src/disclosure/
```

역할:

- OpenDART 수집
- disclosure document/chunk/embedding 저장
- selectedTicker 기반 공시 검색

## Event

위치:

```text
src/event_consolidation/
```

역할:

- 뉴스와 공시 중복 제거
- canonical event 생성
- evidence와 confidence 계산
- SHORT/MID/LONG memory layer 연결

---

# 저장 구조

## MariaDB

주요 저장 대상:

- company master
- stock price
- news와 DART 원본
- document chunk와 embedding
- disclosure document/chunk/embedding
- market event, evidence, event memory layer

## 파일 저장

주요 저장 대상:

- raw/processed 데이터
- ingestion cache와 logs
- unified engine result와 trace
- layered/temporal memory
- event graph와 stock chain
- signal evaluation

---

# Navigation 구조

```text
Runtime Header
→ Breadcrumb, selected ticker, trace status, Runtime action

Runtime Sidebar
→ Global navigation 단일 소스

Detail Navigation
→ Dashboard 내부 section 이동
```

global navigation 정의는 `dashboard-ui/src/navigation/`에서 관리한다.

---

# 현재 경계

현재 시스템은 로컬 단일 노드 연구 환경을 기준으로 한다.

제외:

- 실거래 자동화
- 대규모 분산 Retrieval
- MSA
- 멀티 에이전트 오케스트레이션
- 프로덕션 트레이딩
