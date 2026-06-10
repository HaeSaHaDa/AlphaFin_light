# AlphaFin LTE 모듈 구조

## 문서 목적

현재 존재하는 주요 디렉토리와 책임을 정의한다.

---

# Python 구조

```text
src/
├─ analysis/
├─ collectors/
├─ common/
├─ company_master/
├─ company_resolver/
├─ cost_guard/
├─ dashboard_api/
├─ disclosure/
├─ evaluation/
├─ event_consolidation/
├─ ingestion_pipeline/
├─ preprocess/
├─ rag/
├─ runtime_flow/
├─ runtime_query/
└─ signal_evaluation/
```

## collectors

- pykrx 시세 수집
- OpenDART 기본 수집
- 뉴스 수집

## common

- 환경 설정
- MariaDB 연결과 공통 저장 함수
- 공통 유틸리티

## company_master / company_resolver

- KOSPI200 company master
- 회사명과 ticker 해석
- selectedTicker 기반 Runtime Query 생성

## ingestion_pipeline

- ticker별 뉴스/문서 ingestion
- cache와 embedding 준비 상태 관리
- 수집 결과 통계

## disclosure

- OpenDART 공시 수집
- disclosure document/chunk/embedding repository
- 공시 검색과 요약

## runtime_flow

- Runtime 진입점
- resolver, ingestion, retrieval, engine 연결
- trace와 Dashboard bundle 관리

## runtime_query

- 공시 수집 timeout/cache 처리
- 뉴스/공시 retrieval 병합
- Runtime Context와 evidence 조립

## rag

```text
src/rag/
├─ analysis/
├─ character/
├─ context/
├─ embedding/
├─ evaluation/
├─ evaluation_suite/
├─ event_graph/
├─ layered_memory/
├─ memory/
├─ memory_importance/
├─ reflection/
├─ retrieval/
├─ stock_chain/
├─ temporal_memory/
└─ unified_engine/
```

RAG 검색뿐 아니라 LLM 분석, Memory, Graph, 평가 실행을 포함한다.

## event_consolidation

- 뉴스/공시 중복 제거
- canonical event와 event_id 생성
- evidence, confidence, importance 저장
- event memory layer 연결

## dashboard_api

```text
src/dashboard_api/
├─ routes/
├─ schemas/
├─ services/
└─ app.py
```

FastAPI route, response schema, trace 기반 조회 service를 관리한다.

---

# Frontend 구조

```text
dashboard-ui/src/
├─ app/
├─ components/
├─ hooks/
├─ layout/runtime-shell/
├─ navigation/
├─ runtime-state/
├─ services/
├─ styles/
├─ types/
└─ ui/
```

## app

실제 route:

```text
/
/analysis
/event-graph
/memory-timeline
/signal-evaluation
```

## layout/runtime-shell

- RuntimeHeader
- RuntimeSidebar
- RuntimeWorkspace
- RuntimeFooter

## navigation

- global navigation map
- local navigation map
- route visibility
- navigation responsibility

## runtime-state

- selectedTicker
- traceId
- Runtime session
- panel load 상태
- Dashboard response 동기화

---

# 의존 흐름

```text
Dashboard UI
→ dashboard_api
→ runtime_flow
→ runtime_query
→ ingestion / disclosure / rag
→ MariaDB + data artifacts
```

공통 설정과 DB 연결은 `src/common/`을 사용한다.
