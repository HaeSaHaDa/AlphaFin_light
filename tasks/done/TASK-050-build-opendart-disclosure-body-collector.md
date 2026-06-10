# TASK-050-build-opendart-disclosure-body-collector.md

# TASK-050 OpenDART 공시 본문 수집기 구축

## 상태

DONE

---

# 목표

현재 OpenDART는:

```text
report_name
공시 제목
접수일
```

중심으로 저장되고 있다.

현재 TASK의 목표는:

```text
공시 제목 수준이 아닌

실제 공시 본문을 수집하여

Disclosure RAG 품질을 향상시키는 것
```

이다.

---

# 배경

현재 구조:

```text
OpenDART
↓
report_name 저장
↓
RAG
```

문제:

```text
본문 근거 부족
grounding 약함
summary 품질 저하
```

현재 TASK에서는:

```text
OpenDART 원문 기반 Retrieval
```

을 구축한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- OpenDART 본문 수집
- report_name 유지
- disclosure body 저장
- HTML 정리
- 텍스트 추출
- section chunking
- disclosure chunk 저장
- 기존 Retrieval 연동
- Runtime 연동
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
[공시]

유상증자 결정
```

만 저장되는 경우 존재.

원하는 구조:

```text
[공시]

유상증자 결정

목적:
운영자금 확보

발행주식:
...

납입일:
...
```

본문 근거 확보.

---

# 반드시 확인할 영역

```text
src/disclosure/
src/retrieval/
src/runtime_flow/
```

---

# 수집 목표

저장:

```text
corp_name
ticker
report_name
receipt_date
disclosure_body
```

---

# HTML 처리 목표

제거:

```text
script
style
tag
```

유지:

```text
본문 텍스트
```

---

# Chunk 목표

예상:

```text
chunk 1
chunk 2
chunk 3
```

section 단위 분리.

---

# Retrieval 목표

현재:

```text
report_name 기반
```

↓

목표:

```text
report_name + disclosure body 기반
```

---

# Runtime 목표

현재:

```text
뉴스 중심
```

↓

목표:

```text
뉴스 + 공시 본문
```

---

# 허용

```text
기존 report_name 유지
```

---

# 금지

```text
기존 Runtime 파괴
기존 News Retrieval 제거
```

---

# 결과 보고

Codex는 다음을 기록한다.

## 수집된 본문 예시

```text
...
```

---

## 생성된 chunk 수

```text
...
```

---

## Retrieval 개선 내용

```text
...
```

---

## Runtime 영향

```text
...
```

---

# 관련 Prompt

```text
prompts/TASK-050/
```

---

# 관련 Logs

```text
logs/TASK-050/
```

---

# 완료 조건

- 공시 본문 수집 성공
- HTML 정리 성공
- chunk 생성 성공
- Retrieval 연동 성공
- Runtime 연동 성공
- 결과 로그 작성 완료

---

# 완료 후 다음 TASK 후보

```text
TASK-051-runtime-openai-recheck
TASK-052-runtime-end-to-end-verification
TASK-053-build-real-backtesting-suite
```

---

# 현재 원칙

```text
Explainable AI 유지
Runtime consistency 유지
selectedTicker 중심 유지
Grounding 강화
OpenAI 비용 안정성 유지
과도한 Autonomous AI 구조 금지
```
