# TASK-010-build-rag-context-assembly.md

# TASK-010 RAG Context 조립 파이프라인 구축

## 상태

TODO

---

# 목표

Retrieval 결과로 검색된 Chunk들을
LLM 분석에 사용할 수 있는
RAG Context 형태로 조립하는 파이프라인을 구축한다.

현재 TASK의 목표는
검색된 뉴스/공시 Chunk를
구조화된 Prompt Context로 변환하는 것이다.

현재 단계에서는
복잡한 Agent 구조보다
단순하고 재현 가능한 Context 조립에 집중한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Context Assembly 디렉토리 구조 생성
- Retrieval 결과 조립 구현
- 뉴스/공시 Context 포맷 구현
- Metadata 포함 구조 구현
- Prompt 입력용 Context 생성
- Context 길이 제한 처리
- Context JSON 저장
- 샘플 Query 기반 Context 생성 검증
- 실행 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 실제 금융 분석 수행
- 투자 판단 생성
- LLM 추론 최적화
- Multi-agent 구조
- Chain-of-Thought 최적화
- Tool Calling
- Prompt 자동 개선
- Hallucination 평가
- Memory Layer
- Character Layer
- Long-term Memory
- Reflection 구조
- 자율 트레이딩 Agent

현재 TASK는
LLM 입력용 Context 조립만 수행한다.

---

# 생성 대상 구조

```text
src/rag/context/
├─ __init__.py
├─ assembler.py
├─ formatter.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/context/
```

예상 저장 파일 예시:

```text
data/context/samsung_analysis_context.json
```

---

# Context 역할

현재 Context의 역할:

- Retrieval 결과 정리
- 뉴스/공시 구조화
- Metadata 포함
- Prompt 입력 준비
- LLM 분석용 정보 압축

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- Retrieval 결과 재사용
- 단순한 Context 구조 우선
- Metadata 유지
- Chunk 원문 추적 가능성 유지
- Context 길이 제한 유지
- 명확한 오류 메시지 출력
- 과도한 Prompt Engineering 금지
- 과도한 abstraction 금지

---

# Context 조립 흐름

현재 목표 흐름:

```text
사용자 Query 입력
→ Retrieval 수행
→ 관련 Chunk 수집
→ 뉴스/공시 분류
→ Metadata 포함
→ Context 문자열 생성
→ JSON 저장
```

---

# Context 포함 정보

현재 포함 대상:

```text
- Query
- Chunk Text
- Similarity Score
- ticker
- source
- document_type
- published_at
```

---

# 예상 Context 구조

예상 생성 형태:

```text
[QUERY]
삼성전자 반도체 전망

[NEWS]
- score: 0.91
- source: news
- date: 2024-01-15
- content:
...

[DISCLOSURE]
- score: 0.88
- source: dart
- date: 2024-01-10
- content:
...
```

---

# Context 길이 기준

현재 기준:

```text
- 최대 Chunk 수 제한
- 최대 문자 수 제한
- score 기준 정렬 유지
```

현재 단계에서는
복잡한 token-aware optimization을 사용하지 않는다.

---

# 예상 기능

## assembler.py

역할:

- Retrieval 결과 조립
- 뉴스/공시 그룹화
- Context 생성

예상 함수:

```text
assemble_context(query, chunks)
group_chunks_by_type(chunks)
limit_context_length(context)
```

---

## formatter.py

역할:

- Context 문자열 포맷팅
- Metadata 표시
- Prompt 입력용 구조 생성

예상 함수:

```text
format_news_context(news_chunks)
format_disclosure_context(disclosure_chunks)
build_prompt_context(query, grouped_chunks)
```

---

## run_sample.py

역할:

- 샘플 Query 실행
- Retrieval 수행
- Context 생성
- JSON 저장 검증

샘플 Query 예시:

```text
삼성전자 반도체 실적 전망
HBM 시장 성장
AI 메모리 수요 증가
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Retrieval 검증

- Retrieval 결과 정상 조회 여부
- score 정렬 정상 여부
- 관련 Chunk 존재 여부 확인

---

## Context 검증

- Query 포함 여부
- 뉴스 Context 포함 여부
- 공시 Context 포함 여부
- Metadata 포함 여부
- Context 길이 제한 정상 여부

---

## 저장 검증

- JSON 저장 성공 여부
- Context 파일 생성 여부

---

## 구조 검증

- `src/rag/context/` 생성 여부
- `data/context/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-010/
```

---

# 관련 Logs

```text
logs/TASK-010/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Context Assembly 파이프라인 구축 완료
- Retrieval 결과 조립 성공
- 뉴스/공시 Context 생성 성공
- Metadata 포함 성공
- Context JSON 저장 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-011-build-financial-analysis-flow
- TASK-012-build-analysis-prompt-system
- TASK-013-build-rag-evaluation-pipeline

단,
현재 TASK에서는
실제 LLM 금융 분석을 수행하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- Retrieval 재사용 우선
- Metadata 추적 가능성 유지
- Chunk 원문 추적 가능성 유지
- 단순한 Context 구조 우선
- AI 협업 가능한 구조 유지
- 과도한 Prompt Engineering 금지