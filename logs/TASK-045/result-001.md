# TASK-045 Codex Project Audit 및 Runtime Verification 결과

## 감사 기준

- 감사일: 2026-06-09
- 범위: Audit Only
- 코드 Refactoring, Schema 변경, 신규 기능 추가 없음
- README, AGENTS, project, docs, tasks, prompts, logs 및 실제 코드/실행 상태 비교

## 1. 현재 구축 완료 영역

### 프로젝트 진행 상태

- TASK-001부터 TASK-043까지 `tasks/done/`에 존재한다.
- TASK-044는 결과 로그와 검증 기록을 확인하고 완료 처리했다.
- TASK-045는 본 감사와 실행 검증을 완료했다.
- 다만 TASK-041, TASK-042 문서가 `done`과 `doing`에 중복 존재한다.

### Backend 및 Runtime

- 실제 Backend 엔트리포인트: `src.dashboard_api.app:app`
- Runtime 표준 엔트리포인트: `python -m src.runtime_flow.runtime_query_runner`
- 회사 식별, ingestion cache, 뉴스/공시 retrieval, unified engine, trace 저장 흐름이 연결되어 있다.
- Runtime 결과는 `trace_id`를 기준으로 dashboard, retrieval, memory, graph, evaluation에 연결된다.

### Retrieval

- 실제 위치는 `src/retrieval/`이 아니라 `src/rag/retrieval/`이다.
- `src/runtime_flow/retrieval_executor.py`가 ticker filter를 적용한다.
- 공시 retrieval은 `src/disclosure/`와 `src/runtime_query/`에서 뉴스 결과와 병합된다.

### Disclosure

- OpenDART 수집기, 문서 저장소, chunk, embedding, retrieval이 구현되어 있다.
- MariaDB의 `disclosure_documents`, `disclosure_chunks`, `disclosure_embeddings`가 존재한다.
- 확인 시 각 테이블에 200행이 저장되어 있었다.

### Event 및 Memory

- canonical event, `event_id`, evidence, confidence 계산 및 저장 구조가 존재한다.
- `market_events` 27행, `event_evidence` 28행을 확인했다.
- SHORT/MID/LONG 계층과 중복 제거 코드가 존재한다.
- event별 active memory layer를 하나로 유지하는 로직이 존재한다.

### Frontend 및 Navigation

- Next.js App Router route:
  - `/`
  - `/analysis`
  - `/event-graph`
  - `/memory-timeline`
  - `/signal-evaluation`
- Dashboard 내 News, Disclosure, Event, Evidence, Graph, Memory, Evaluation section이 존재한다.
- Sidebar가 global navigation source이고 Header는 ticker, trace, action 중심이다.
- Detail navigation은 Dashboard section 이동에 사용된다.
- `selectedTicker`, `traceId`, company, runtime query가 context와 `sessionStorage`에 유지된다.

### API

- `/api/query/run`
- `/api/runtime/run`
- `/api/runtime/context`
- `/api/runtime/dashboard/{trace_id}`
- `/api/runtime/evidence/{trace_id}`
- `/api/events/...`
- `/api/disclosure/...`

요청서의 `/api/query`, `/api/runtime`, `/api/events`, `/api/disclosure`는 route prefix이며,
모든 prefix에 정확한 root handler가 있는 구조는 아니다.

## 2. 실행 검증

### Python 정적 검증

```text
Python 3.13.12
Python 파일 221개 AST 문법 검사 통과
```

`python -m compileall -q src`는 기존 `__pycache__` 파일 쓰기 권한 오류로 실패했다.
문법 오류와 구분하기 위해 파일을 쓰지 않는 AST 검사로 재검증했다.

### Frontend

```text
npx.cmd tsc --noEmit
PASS

npm run dev
PASS
```

HTTP 확인:

```text
/                  200
/analysis          200
/event-graph       200
/memory-timeline   200
/signal-evaluation 200
```

PowerShell에서는 `npx`가 실행 정책으로 차단되므로 `npx.cmd` 사용이 필요하다.

### Python Backend

```text
python -m uvicorn src.dashboard_api.app:app --host 127.0.0.1 --port 8000
PASS

GET /health
200 {"status":"ok","port":"8000"}
```

### MariaDB

```text
연결 성공
database=finance_study
version=10.11.17-MariaDB
```

### Runtime Query

기존 직접 실행:

```text
python src/runtime_flow/runtime_query_runner.py
FAIL
ModuleNotFoundError: No module named 'src'
```

표준 모듈 실행:

```text
python -m src.runtime_flow.runtime_query_runner
프로세스 종료 코드 0
trace_id=20260609_101515
ticker=005380
```

단, OpenAI Embedding과 Chat API는 네트워크 오류로 실패했다. 공시 chunk 5건이 존재한다는
이유로 최종 상태가 `completed`가 되었고, 빈 분석 결과가 저장되었다.

### Collector

뉴스 요청 명령:

```text
python -m src.collectors.news_collector
FAIL: 해당 모듈 없음
```

실제 뉴스 구현 위치:

```text
src/collectors/news/collector.py
src/collectors/news/run_sample.py
```

공시 요청 명령:

```text
python -m src.disclosure.dart_collector
ARGUMENT ERROR: --ticker 필수
```

권장 공시 실행:

```text
python -m src.disclosure.dart_collector --ticker 005930
```

## 3. 발견한 문제

### 높음

1. Runtime 거짓 성공 상태
   - OpenAI Embedding/Chat 실패 후에도 retrieval chunk가 있으면 `completed`를 반환한다.
   - 실제 생성된 `analysis_result.summary`는 빈 문자열이었다.
   - 실패한 분석도 memory, graph, stock chain, signal 파일을 갱신한다.

2. 프로젝트 문서가 실제 구현보다 크게 오래됨
   - `project/current-status.md`는 Collector, Retrieval, LLM 코드가 미구현이라고 기록한다.
   - architecture 문서도 현재 Runtime, Dashboard, Disclosure, Event 구조를 반영하지 않는다.

### 중간

1. Runtime module warning
   - `src/runtime_flow/__init__.py`가 runner를 선행 import하여 `python -m` 실행 시 runpy warning이 발생한다.

2. 실행 경로 불일치
   - `src/retrieval`, `src/memory`, `src/graph`, `src/api`는 실제 최상위 디렉토리가 아니다.
   - 각각 주로 `src/rag/*`, `src/dashboard_api/`에 위치한다.

3. Collector 명령 불일치
   - 문서의 뉴스 Collector 명령이 실제 패키지 구조와 맞지 않는다.
   - `src/collectors/news/run_sample.py`도 package-safe import가 아니라 `from collector import ...`를 사용한다.

4. Event Memory 미적재
   - `event_memory_layers` 테이블은 존재하지만 확인 시 0행이었다.
   - SHORT/MID/LONG 코드가 있어도 canonical event와 실제 memory layer 연결은 검증되지 않았다.

5. Task 상태 중복
   - TASK-041, TASK-042가 `doing`과 `done`에 동시에 존재한다.

### 낮음

1. Navigation 의미 불일치
   - global `Retrieval`이 독립 retrieval 화면이 아니라 `#section-evaluation`로 연결된다.
   - global `Settings`가 설정 화면이 아니라 `#section-summary`로 연결된다.

2. 남은 unused/legacy 후보
   - `SidebarSection`은 import 사용처가 확인되지 않았다.
   - `RuntimeSectionNav` 컴포넌트 자체는 미사용이고 `scrollToSection` helper만 재사용된다.
   - `dashboard_api/run_sample.py`는 비활성화된 `/latest` API를 성공 기준으로 사용하여 현재 정책과 충돌한다.
   - 여러 service에 legacy `fetch_latest_*` 함수가 남아 있다.

3. 예외 가시성
   - memory service 일부 경로는 `except Exception: pass`로 event memory 오류를 숨긴다.

## 4. Runtime Context 확인

### selectedTicker

- 새 query 실행 시 먼저 선택 ticker로 Runtime state를 reset한다.
- query 응답과 panel bundle에서 ticker를 다시 동기화한다.
- sessionStorage에 ticker를 저장한다.

### traceId

- URL `trace_id`를 우선 사용한다.
- sessionStorage에 traceId를 저장한다.
- API와 detail route 링크에 traceId를 전달한다.
- trace 기반 API는 대체로 latest/sample fallback을 금지한다.

### Runtime 상태

- idle, running/loading, active, error 상태 표현이 존재한다.
- 단, Backend의 engine 성공 판정이 LLM 성공 여부를 반영하지 않아 Frontend Runtime Active가
  실제 분석 성공을 과대 표시할 수 있다.

## 5. 실행 명령 표준안

```bash
# Runtime Query
python -m src.runtime_flow.runtime_query_runner

# Backend
python -m uvicorn src.dashboard_api.app:app --host 127.0.0.1 --port 8000

# Frontend
cd dashboard-ui
npm run dev

# TypeScript (Windows PowerShell)
npx.cmd tsc --noEmit

# Disclosure Collector
python -m src.disclosure.dart_collector --ticker 005930
```

뉴스 Collector는 현재 요청된 표준 명령을 제공하지 않으므로 다음 TASK에서 package-safe CLI를
정의하기 전까지 공식 표준으로 선언하지 않는다.

## 6. 다음 진행 가능 여부

```text
조건부 가능
```

Frontend, Backend, MariaDB, trace 기반 route, 공시/이벤트 저장 구조는 동작한다.
그러나 다음 기능 개발 전에 Runtime 성공 판정과 문서/실행 명령의 불일치를 먼저 정리해야 한다.

## 7. 추천 다음 TASK

```text
TASK-046-runtime-status-and-command-contract-verification
```

권장 범위:

- LLM/Embedding 실패 시 completed 금지
- 부분 성공과 분석 성공 상태 분리
- Runtime 실행 시 빈 분석 결과의 memory/graph 저장 차단 검토
- Runtime module warning 제거
- Backend, Runtime, Collector 공식 명령 문서화
- 오래된 current-status와 architecture 문서 현행화
- TASK-041/042 상태 중복 정리

Backtesting이나 신규 분석 기능보다 이 계약 검증을 먼저 수행하는 것이 안전하다.

## 8. OpenAI API Key 재검증

재검증일:

```text
2026-06-09
```

사용자가 `.env`의 API Key를 수정한 뒤 최소 API 호출과 전체 Runtime을 다시 검증했다.
API Key 값 자체는 출력하거나 로그에 기록하지 않았다.

### 최소 호출

```text
Embedding API: PASS
model=text-embedding-3-small
dimension=1536

Chat API: PASS
model=gpt-4o-mini-2024-07-18
response=OK
```

### Runtime 재검증

```bash
python -m src.runtime_flow.runtime_query_runner "현대자동차 전기차 전망"
```

결과:

```text
status=completed
trace_id=20260609_102016
ticker=005380
retrieval chunks=11
summary 생성=성공
bullish factors=2
bearish factors=2
risks=2
reflection 생성=성공
hallucination risk=low
```

OpenAI Embedding, Character Analysis, Reflection 호출 모두 HTTP 200을 확인했다.
따라서 감사 시점에 발생했던 네트워크 연결 실패와 빈 분석 결과 문제는 현재 환경에서 해소되었다.

단, OpenAI 호출이 실패해도 retrieval chunk 수만으로 Runtime을 `completed` 처리할 수 있는
상태 판정 로직 위험은 여전히 남아 있다.
