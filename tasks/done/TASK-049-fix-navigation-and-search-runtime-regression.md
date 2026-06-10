# TASK-049-fix-navigation-and-search-runtime-regression.md

# TASK-049 Navigation 및 Search Runtime Regression 수정

## 상태

DONE

---

# 목표

최근 TASK를 진행하면서:

```text
Navigation 정리
Demo 제거
Pipeline 정리
Fallback 제거
```

가 수행되었다.

그 결과 현재 다음 문제가 발생하였다.

```text
메뉴 클릭 불가
검색 불가
분석 실행 불가
화면 이동 실패
```

현재 TASK의 목표는:

```text
기존 기능이 깨진 부분을 찾아

정상 동작 상태로 복구하는 것
```

이다.

현재 단계에서는:

```text
신규 기능 추가
```

보다:

```text
Regression 수정
Runtime 복구
```

에 집중한다.

---

# 배경

TASK-044:

```text
Navigation 정리
```

TASK-048:

```text
Demo 제거
Fallback 제거
```

이후 일부 연결이 끊어진 것으로 보인다.

현재 TASK에서는:

```text
Regression Audit
+
Regression Fix
```

를 수행한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Sidebar 메뉴 점검
- Header 검색 점검
- 종목 선택 점검
- 분석 실행 버튼 점검
- route 이동 점검
- selectedTicker 유지 점검
- traceId 생성 점검
- API 호출 점검
- Runtime 실행 점검
- 화면 렌더링 점검
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

```text
신규 기능 추가
Schema 변경
Backtesting
Auto Trading
Refactoring
UI Redesign
```

---

# 반드시 확인할 영역

```text
dashboard-ui/
src/api/
src/runtime_flow/
```

---

# Sidebar 확인

확인:

```text
Dashboard
News
Disclosure
Graph
Memory
Evaluation
Retrieval
```

각 메뉴 클릭 시:

```text
정상 route 이동 여부
```

확인.

---

# Header 확인

확인:

```text
검색 입력
종목 선택
분석 실행
```

동작 여부 확인.

---

# Search 확인

확인:

```text
selectedTicker 생성
query 생성
```

여부.

금지:

```text
default ticker
```

자동 사용.

---

# API 확인

확인:

```text
/api/query/run
/api/runtime
/api/events
```

정상 호출 여부.

---

# Runtime 확인

확인:

```text
traceId 생성
Runtime 실행
```

여부.

---

# Route 확인

확인:

```text
broken route
dead navigation
```

존재 여부.

---

# 화면 확인

확인:

```text
빈 화면
로딩 무한 반복
오류 화면
```

발생 여부.

---

# 결과 보고

Codex는 다음을 기록한다.

## 발견된 Regression

```text
...
```

---

## 수정된 코드

```text
...
```

---

## 복구된 기능

```text
...
```

---

## 남아있는 문제

```text
...
```

---

# 관련 Prompt

```text
prompts/TASK-049/
```

---

# 관련 Logs

```text
logs/TASK-049/
```

---

# 완료 조건

- 메뉴 정상 동작
- 검색 정상 동작
- 분석 실행 정상 동작
- route 정상 동작
- Runtime 실행 정상 동작
- 결과 로그 작성 완료

---

# 완료 후 다음 TASK 후보

```text
TASK-050-runtime-openai-recheck
TASK-051-runtime-end-to-end-verification
TASK-052-build-real-backtesting-suite
```

---

# 현재 원칙

```text
Explainable AI 유지
Runtime consistency 유지
selectedTicker 중심 유지
Regression 최소화
OpenAI 비용 안정성 유지
과도한 Autonomous AI 구조 금지
```
