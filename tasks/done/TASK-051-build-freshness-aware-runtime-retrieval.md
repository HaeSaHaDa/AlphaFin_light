# TASK-051-build-freshness-aware-runtime-retrieval.md

# TASK-051 최신성 기반 Runtime Retrieval 구축

## 상태

DONE

---

# 목표

현재 Runtime은:

```text
수집된 데이터 중
의미 유사도가 높은 문서 검색
```

구조를 사용한다.

즉 현재는:

```text
관련성 중심 RAG
```

이며,

```text
최신성 보장 RAG
```

는 아니다.

현재 TASK의 목표는:

```text
최신 데이터가 우선 사용되도록

Freshness-aware Retrieval

구조를 구축하는 것
```

이다.

---

# 배경

현재 확인된 상태:

```text
삼성전자 뉴스 캐시
→ 2026-05-27

일부 뉴스
→ 2026-06-09

공시 최신일
→ 2026-06-08

공시 본문 캐시
→ 2026-06-10
```

현재 문제:

```text
오래된 뉴스가 검색될 수 있음
공시 cache TTL 없음
종목별 수집 시점 차이 존재
사용자가 기준 시각을 알 수 없음
```

현재 TASK에서는:

```text
Freshness + Relevance
```

를 함께 사용한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- 뉴스 cache TTL 적용
- 공시 cache TTL 적용
- Runtime 실행 전 최신 데이터 확인
- 필요 시 자동 재수집
- 날짜 기반 필터 적용
- 최신성 가중치 추가
- Retrieval 점수 개선
- Dashboard 기준 시각 표시
- 마지막 수집 시각 표시
- cache 사용 여부 표시
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

```text
신규 AI 모델 추가
Backtesting
Auto Trading
Schema 대규모 변경
```

---

# 현재 문제

현재:

```text
관련성은 높지만
오래된 뉴스가 검색될 수 있음
```

목표:

```text
관련성
+
최신성
```

동시 고려.

---

# 반드시 확인할 영역

```text
src/retrieval/
src/runtime_flow/
src/collectors/
dashboard-ui/
```

---

# News TTL 목표

예:

```text
6시간
12시간
24시간
```

중 기존 구조에 맞게 선택.

목표:

```text
오래된 뉴스 cache 자동 갱신
```

---

# Disclosure TTL 목표

목표:

```text
새 공시 존재 시 cache 재생성
```

---

# Runtime 목표

현재:

```text
DB 검색
```

↓

목표:

```text
TTL 확인
↓
필요 시 재수집
↓
Retrieval
```

---

# Retrieval Score 목표

현재:

```text
similarity score
```

↓

목표:

```text
similarity
+
freshness score
```

---

# Dashboard 목표

표시:

```text
뉴스 기준 시각
공시 기준 시각
마지막 수집 시각
cache 사용 여부
```

예:

```text
News Updated:
2026-06-10 09:30

Disclosure Updated:
2026-06-10 09:25

Cache:
HIT
```

---

# 허용

```text
기존 Retrieval 유지
기존 RAG 유지
```

---

# 금지

```text
기존 Runtime 파괴
기존 News Retrieval 제거
```

---

# 추가 검증 항목

## OpenAI

확인:

```text
.env
API Key
모델명
최소 호출
실패 처리
```

---

## Runtime 안정성

확인:

```text
run_with_timeout
runtime_flow.__init__ 순환 import
```

---

## 공시 본문

확인:

```text
raw_text 저장 여부
chunk 생성 여부
embedding 생성 여부
```

---

# 결과 보고

Codex는 다음을 기록한다.

## 적용된 TTL

```text
...
```

---

## Freshness Score

```text
...
```

---

## Dashboard 표시 내용

```text
...
```

---

## Runtime 영향

```text
...
```

---

## 발견된 위험 요소

```text
...
```

---

# 관련 Prompt

```text
prompts/TASK-051/
```

---

# 관련 Logs

```text
logs/TASK-051/
```

---

# 완료 조건

- News TTL 적용 성공
- Disclosure TTL 적용 성공
- 최신성 가중치 적용 성공
- Dashboard 기준 시각 표시 성공
- cache 상태 표시 성공
- OpenAI 재검증 완료
- Runtime 안정성 확인 완료
- 결과 로그 작성 완료

---

# 완료 후 다음 TASK 후보

```text
TASK-052-runtime-end-to-end-verification
TASK-053-fix-runtime-timeout-and-import-stability
TASK-054-build-real-backtesting-suite
```

---

# 현재 원칙

```text
Explainable AI 유지
Runtime consistency 유지
selectedTicker 중심 유지
Freshness 강화
Grounding 강화
OpenAI 비용 안정성 유지
과도한 Autonomous AI 구조 금지
```
