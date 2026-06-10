# TASK-045 Codex Project Audit 및 Runtime Verification

## 상태

DONE

---

# 목표

현재 프로젝트는 Cursor 기반으로 구현되었으며,
이제부터는 Codex를 메인 구현 환경으로 사용한다.

현재 TASK의 목표는

```text
Codex가 프로젝트 전체를 이해하고

현재 상태를 정확히 파악한 뒤

다음 개발을 안전하게 진행할 수 있도록
프로젝트 전체를 Audit하는 것
```

이다.

현재 단계에서는

```text
신규 기능 추가
```

보다:

```text
구조 파악
실행 검증
Runtime 검증
환경 검증
맥락 확인
```

에 집중한다.

---

# 현재 프로젝트 구성

```text
Frontend
→ Next.js

Backend
→ Python

Database
→ MariaDB

AI Engine
→ Python Runtime Pipeline
```

---

# 배경

현재 프로젝트는 다음 영역이 구현되어 있다.

```text
News Retrieval
Disclosure Store
Runtime Query
Event Consolidation
Memory Layer
Market Graph
Explainable Dashboard
Persistent Runtime Shell
Navigation Cleanup
```

기능은 상당 수준 구현되었으나,

현재부터는:

```text
Cursor → Codex
```

환경 전환이 발생한다.

Codex가 현재 구조를 이해하지 못한 상태에서
다음 기능을 추가하면:

```text
중복 구현
기존 구조 파괴
Runtime 오류
```

가 발생할 수 있다.

현재 TASK에서는

```text
Codex Onboarding + Full Audit
```

를 수행한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- 프로젝트 구조 파악
- README 확인
- AGENTS.md 확인
- docs 구조 확인
- tasks 구조 확인
- prompts 구조 확인
- logs 구조 확인
- Runtime 구조 확인
- Retrieval 구조 확인
- Memory 구조 확인
- Disclosure 구조 확인
- Event 구조 확인
- Dashboard 구조 확인
- Navigation 구조 확인
- API 구조 확인
- MariaDB 연결 확인
- 실행 명령 점검
- Frontend 실행 확인
- Python Backend 실행 확인
- Runtime Query 실행 확인
- Route 구조 확인
- selectedTicker 유지 구조 확인
- traceId 유지 구조 확인
- 위험 요소 확인
- 다음 TASK 진행 가능 여부 판단
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

```text
신규 기능 추가
Refactoring
Schema 변경
Backtesting
Auto Trading
```

현재 TASK는

```text
Audit Only
```

를 수행한다.

---

# 반드시 확인할 디렉토리

```text
README.md
AGENTS.md

project/
docs/
tasks/
prompts/
logs/

src/
dashboard-ui/
```

---

# 반드시 확인할 TASK 상태

```text
tasks/done
tasks/todo
```

확인 후

```text
현재 프로젝트 진행 단계
```

를 정리한다.

---

# 반드시 확인할 Python 구조

```text
src/runtime_flow/
src/retrieval/
src/disclosure/
src/event_consolidation/
src/memory/
src/graph/
src/api/
src/collectors/
```

---

# Frontend 실행 검증

```bash
npm run dev
```

정상 실행 여부 확인.

---

# Python Backend 실행 검증

실제 엔트리포인트 확인 후 실행.

예:

```bash
python -m src.main
```

또는

```bash
python -m src.api.main
```

---

# Runtime Query 실행 검증

기존:

```bash
python src/runtime_flow/runtime_query_runner.py
```

실패 여부 확인.

표준:

```bash
python -m src.runtime_flow.runtime_query_runner
```

성공 여부 확인.

---

# Collector 실행 검증

뉴스:

```bash
python -m src.collectors.news_collector
```

공시:

```bash
python -m src.disclosure.dart_collector
```

---

# API 확인

확인 대상:

```text
/api/query
/api/runtime
/api/events
/api/disclosure
```

---

# Dashboard 확인

확인 대상:

```text
Dashboard
News
Disclosure
Graph
Memory
Evaluation
Retrieval
```

---

# Navigation 확인

확인 대상:

```text
Header
Sidebar
Detail Navigation
```

중복 여부 확인.

---

# Runtime Context 확인

다음 유지 여부 확인:

```text
selectedTicker
traceId
Runtime 상태
```

---

# Memory 확인

확인 대상:

```text
SHORT
MID
LONG
```

중복 여부 확인.

---

# Event 확인

확인 대상:

```text
event_id
canonical event
evidence
confidence
```

---

# Disclosure 확인

확인 대상:

```text
OpenDART
disclosure_documents
disclosure retrieval
```

---

# 위험 요소 확인

현재 프로젝트에서:

```text
dead code
unused component
broken route
duplicate logic
```

존재 여부 확인.

---

# 실행 명령 표준화

최종 권장:

```bash
python -m src.runtime_flow.runtime_query_runner
```

기준으로 통일.

---

# 결과 보고

Codex는 다음 내용을 보고한다.

## 현재 구축 완료 영역

```text
...
```

## 발견한 문제

```text
...
```

## Runtime 위험 요소

```text
...
```

## 다음 진행 가능 여부

```text
가능 / 불가능
```

## 추천 다음 TASK

```text
...
```

---

# 관련 Prompt

```text
prompts/TASK-045/
```

---

# 관련 Logs

```text
logs/TASK-045/
```

---

# 완료 조건

- 프로젝트 구조 파악 완료
- Runtime 실행 확인 완료
- Frontend 확인 완료
- Python Backend 확인 완료
- API 확인 완료
- Navigation 확인 완료
- 위험 요소 확인 완료
- 실행 명령 표준화 완료
- Codex 온보딩 완료
- 결과 로그 작성 완료

---

# 완료 후 다음 TASK 후보

```text
TASK-046-build-runtime-end-to-end-verification
TASK-047-build-presentation-demo-scenario
TASK-048-build-portfolio-backtesting-suite
```

---

# 현재 원칙

```text
Explainable AI 유지
Runtime consistency 유지
selectedTicker 중심 유지
기존 구조 존중
OpenAI 비용 안정성 유지
과도한 Autonomous AI 구조 금지
```
