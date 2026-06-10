# AlphaFin LTE 현재 프로젝트 상태

## 문서 목적

이 문서는 실제 코드와 TASK 상태를 기준으로 현재 구현 범위와 다음 작업을 기록한다.

기준일:

```text
2026-06-09
```

---

# 현재 프로젝트 단계

현재 단계:

```text
통합 Runtime 구축 완료
→ 프로젝트 상태 및 문서 동기화 완료
→ Runtime 계약과 Event Memory 연결 검증 준비
```

초기 하네스 단계는 종료되었다. 현재는 수집, 검색, LLM 분석, Memory, Event,
Dashboard를 하나의 trace 기반 Runtime으로 연결한 상태이다.

---

# 현재 완료 기능

## 데이터 수집 및 저장

- pykrx 기반 한국 주식 시세 수집
- OpenDART 공시 수집
- 뉴스 수집
- KOSPI200 company master와 종목 선택
- MariaDB 기반 회사, 시세, 뉴스, 공시, chunk, embedding 저장
- Raw, Processed, cache, 실행 산출물 분리

## Retrieval 및 분석

- OpenAI Embedding 기반 뉴스/문서 검색
- selectedTicker 기반 metadata filtering
- 공시 문서 chunk 및 disclosure retrieval
- 뉴스와 공시 evidence 통합
- Context Assembly
- Character 기반 LLM 분석
- Evaluation과 Reflection

## Memory 및 Event

- Analysis Memory
- SHORT, MID, LONG layered memory
- importance와 temporal lifecycle
- Event Graph와 Stock Chain
- 뉴스/공시 중복 제거
- canonical event 생성
- event evidence와 confidence 저장
- event memory layer 매핑 구조

## Runtime

- 회사명 또는 선택 ticker 기반 Runtime Query
- ingestion cache 확인과 필요 시 수집
- Retrieval, Context, LLM, Evaluation, Memory, Graph 실행
- `trace_id` 기반 결과 저장
- Dashboard 응답 bundle 생성
- 표준 실행:

```bash
python -m src.runtime_flow.runtime_query_runner "<회사명이 포함된 질문>"
```

## Backend API

- FastAPI Backend
- Query, Runtime, Retrieval, Memory, Event, Disclosure API
- Graph, Evaluation, Signal, Trace API
- 실제 엔트리포인트:

```bash
python -m uvicorn src.dashboard_api.app:app --host 127.0.0.1 --port 8000
```

## Frontend

- Next.js Dashboard
- Dashboard, Analysis, Event Graph, Memory Timeline, Signal Evaluation route
- News, Disclosure, Event, Evidence, Graph, Memory, Evaluation panel
- persistent Runtime Shell
- Sidebar 중심 global navigation
- Dashboard 내부 detail navigation
- `selectedTicker`, `traceId`, Runtime session 유지

## 프로젝트 운영

- TASK-001부터 TASK-045 완료
- TASK별 prompts와 logs 관리
- TASK 중복 상태 제거
- Codex 기준 프로젝트 Audit 완료

---

# 현재 진행 중 기능

현재 진행 중인 신규 기능은 없다.

TASK-046에서 문서와 TASK 구조를 실제 구현 상태에 맞게 동기화했다.

---

# 다음 예정 기능

우선순위 후보:

1. Event와 SHORT/MID/LONG memory layer의 실제 저장·조회 연결 검증
2. OpenAI/Embedding 실패를 반영하는 Runtime 상태 계약 정리
3. Runtime End-to-End 자동 검증

후보 TASK:

```text
TASK-047-connect-event-memory-layer
TASK-048-runtime-openai-recheck
TASK-049-runtime-end-to-end-verification
```

---

# 현재 Runtime 상태

확인 완료:

- MariaDB 연결
- OpenAI Embedding 호출
- OpenAI Chat 호출
- 뉴스와 공시 통합 retrieval
- 실제 LLM summary와 factor 생성
- Reflection 생성
- trace 결과 저장
- Frontend와 Backend 실행

남은 위험:

- OpenAI 분석 실패 시에도 retrieval chunk가 있으면 `completed`가 될 수 있다.
- `python -m src.runtime_flow.runtime_query_runner` 실행 시 package 선행 import warning이 발생한다.
- event memory layer 테이블과 실제 canonical event 연결 데이터는 추가 검증이 필요하다.

---

# 문서 및 TASK 상태

```text
tasks/done  : TASK-001 ~ TASK-046
tasks/doing : 비어 있음
tasks/todo  : 비어 있음
```

Prompt와 log는 TASK-001부터 TASK-046까지 TASK 단위로 관리한다.

---

# 현재 제외 범위

- 실거래 자동화
- HFT
- 대규모 분산 시스템
- MSA
- 복잡한 Agent Orchestration
- 원본 AlphaFin 완전 재현
- 프로덕션 트레이딩 시스템

---

# 현재 원칙

- 문서와 실제 구현 상태 일치
- selectedTicker 중심 흐름 유지
- traceId 기반 결과 조회
- Explainable AI 유지
- 작은 TASK와 작은 변경 유지
- 검증 없는 완료 처리 금지
- 과도한 자율화 및 인프라 확장 금지
