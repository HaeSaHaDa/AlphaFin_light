# TASK-048-remove-runtime-demo-signal-and-hardcoded-stock-chain-entrypoints.md

# TASK-048 Runtime Demo Signal 및 Hardcoded Stock Chain 제거

## 상태

DONE

---

# 목표

TASK-047 Audit 결과 다음 문제가 발견되었다.

```text
Demo Signal Evaluation 존재
Hardcoded Stock Chain 존재
Default ticker 존재
Default query 존재
Pipeline fallback 중복 존재
```

현재 TASK의 목표는:

```text
실제 Runtime처럼 보이는

Demo 코드와

Hardcoded Entry Point를 제거하여

Runtime 신뢰성을 확보하는 것
```

이다.

현재 단계에서는:

```text
신규 기능 추가
```

보다:

```text
Demo 제거
Runtime 정합성 확보
```

에 집중한다.

---

# 배경

Audit 결과 다음 문제가 발견되었다.

## Signal Evaluation

현재:

```text
bullish → +3.5%
neutral → +0.5%
bearish → -2.8%
```

고정값 사용.

즉:

```text
실제 평가
X

Demo 평가
O
```

상태.

---

## Stock Chain

현재:

```text
NVIDIA
HBM
삼성전자
SK하이닉스
```

고정 연결 존재.

---

## Runtime 기본값

현재:

```text
005930
현대자동차 전기차 전망
```

기본값 존재.

---

## Pipeline Fallback

현재:

```text
DEFAULT_PIPELINE
defaultPipeline()
legacy normalize
```

중복 존재.

---

# 범위

현재 TASK에서 포함하는 작업:

- Demo Signal 제거
- Demo Outcome 제거
- Demo Timeline 제거
- Hardcoded Stock Chain 제거
- Default ticker 제거
- Default query 제거
- Runtime Entry Point 정리
- Pipeline fallback 통합
- Legacy normalize 정리
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

```text
Backtesting
실제 수익률 계산
신규 기능 추가
Refactoring
Schema 변경
Auto Trading
```

---

# 반드시 확인할 디렉토리

```text
src/
dashboard-ui/
```

특히:

```text
src/evaluation/
src/runtime_flow/
src/graph/
src/retrieval/

dashboard-ui/src/
```

---

# 제거 대상

## Demo Signal

금지:

```text
bullish → +3.5%
neutral → +0.5%
bearish → -2.8%
```

---

## Demo Timeline

금지:

```text
DEMO_TIMELINE
```

---

## Demo Outcome

금지:

```text
DEMO_OUTCOMES
```

---

## Hardcoded Stock Chain

금지:

```text
NVIDIA
HBM
삼성전자
SK하이닉스
```

고정 연결.

---

## Default Ticker

금지:

```text
005930
```

기본 Runtime 입력.

---

## Default Query

금지:

```text
현대자동차 전기차 전망
```

자동 query.

---

# 허용되는 것

허용:

```text
selectedTicker 기반
Runtime query 기반
retrieval 기반
event 기반
```

---

# Pipeline 목표

현재 목표:

```text
단 하나의 Pipeline fallback만 유지
```

금지:

```text
DEFAULT_PIPELINE
defaultPipeline()
legacy normalize
```

중복 유지.

---

# 결과 보고

Codex는 다음을 기록한다.

## 제거된 Demo 코드

```text
...
```

---

## 제거된 Hardcoded 코드

```text
...
```

---

## 통합된 Pipeline

```text
...
```

---

## 남겨둔 안전한 fallback

```text
...
```

---

## Runtime 위험 요소

```text
...
```

---

# 관련 Prompt

```text
prompts/TASK-048/
```

---

# 관련 Logs

```text
logs/TASK-048/
```

---

# 완료 조건

- Demo Signal 제거 완료
- Demo Timeline 제거 완료
- Demo Outcome 제거 완료
- Hardcoded Stock Chain 제거 완료
- Default ticker 제거 완료
- Default query 제거 완료
- Pipeline fallback 통합 완료
- 결과 로그 작성 완료

---

# 완료 후 다음 TASK 후보

```text
TASK-049-runtime-openai-recheck
TASK-050-runtime-end-to-end-verification
TASK-051-build-real-backtesting-suite
```

---

# 현재 원칙

```text
Explainable AI 유지
Runtime consistency 유지
selectedTicker 중심 유지
Demo 코드 제거 유지
OpenAI 비용 안정성 유지
과도한 Autonomous AI 구조 금지
```
