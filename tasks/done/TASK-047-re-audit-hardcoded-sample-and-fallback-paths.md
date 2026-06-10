# TASK-047-re-audit-hardcoded-sample-and-fallback-paths.md

# TASK-047 Hardcoded / Sample / Fallback 경로 재점검

## 상태

DONE

---

# 목표

초기 개발 단계에서 사용했던:

```text
sample data
mock data
hardcoded ticker
fallback payload
placeholder response
demo graph
```

가 현재 Runtime에 남아 있을 가능성이 있다.

현재 TASK의 목표는:

```text
실제 Runtime과 관계없는

초기 개발용 코드가 남아있는지

프로젝트 전체를 다시 점검하는 것
```

이다.

현재 단계에서는:

```text
신규 기능 추가
```

보다:

```text
Audit
정리
Runtime 신뢰성 확보
```

에 집중한다.

---

# 배경

초기 구현 단계에서는:

```text
삼성전자
현대자동차
sample payload
mock graph
default trace
placeholder data
```

등을 사용하여 개발하였다.

TASK-036에서 일부 제거했으나,

현재까지 기능이 많이 추가되면서:

```text
새로운 fallback
새로운 sample
legacy path
```

가 다시 생겼을 가능성이 있다.

현재 TASK에서는:

```text
Hardcoded Audit
```

를 다시 수행한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- sample code 점검
- mock data 점검
- fallback payload 점검
- placeholder response 점검
- default ticker 점검
- hardcoded company 점검
- demo graph 점검
- latest fallback 점검
- default trace 점검
- runtime default 값 점검
- unused sample 제거 후보 확인
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

Audit Only 수행.

---

# 반드시 점검할 디렉토리

```text
src/
dashboard-ui/
```

특히:

```text
src/runtime_flow/
src/retrieval/
src/disclosure/
src/event_consolidation/
src/memory/
src/graph/
src/api/

dashboard-ui/src/
```

---

# 검색 키워드

다음 문자열 검색:

```text
sample
mock
demo
fallback
latest
default
dummy
placeholder
```

---

# 종목 관련 검색

다음 문자열 검색:

```text
삼성전자
현대자동차
005930
005380
NVDA
NVIDIA
HBM
MLCC
```

---

# 확인 대상

## Runtime

확인:

```text
selectedTicker 사용 여부
```

금지:

```text
hardcoded ticker
```

---

## Graph

확인:

```text
runtime graph 생성
```

금지:

```text
sample graph
```

---

## Memory

확인:

```text
event 기반 memory
```

금지:

```text
placeholder memory
```

---

## Event

확인:

```text
runtime event 생성
```

금지:

```text
sample event
```

---

## Disclosure

확인:

```text
runtime disclosure
```

금지:

```text
default disclosure
```

---

## Dashboard

확인:

```text
runtime payload 기반
```

금지:

```text
sample card
mock panel
```

---

# 결과 보고

Codex는 다음을 기록한다.

## 발견된 hardcoded 코드

```text
...
```

---

## 발견된 fallback

```text
...
```

---

## 발견된 sample

```text
...
```

---

## 제거가 필요한 코드

```text
...
```

---

## 즉시 위험한 코드

```text
...
```

---

## 안전한 fallback

```text
...
```

---

# 관련 Prompt

```text
prompts/TASK-047/
```

---

# 관련 Logs

```text
logs/TASK-047/
```

---

# 완료 조건

- sample 코드 점검 완료
- mock 코드 점검 완료
- hardcoded ticker 점검 완료
- fallback 경로 점검 완료
- placeholder 점검 완료
- 결과 로그 작성 완료

---

# 완료 후 다음 TASK 후보

```text
TASK-048-connect-event-memory-layer
TASK-049-runtime-openai-recheck
TASK-050-runtime-end-to-end-verification
```

---

# 현재 원칙

```text
Explainable AI 유지
Runtime consistency 유지
selectedTicker 중심 유지
Hardcoded 제거 유지
OpenAI 비용 안정성 유지
과도한 Autonomous AI 구조 금지
```
