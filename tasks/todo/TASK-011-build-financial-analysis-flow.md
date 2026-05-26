# TASK-011-build-financial-analysis-flow.md

# TASK-011 금융 분석 RAG Flow 구축

## 상태

TODO

---

# 목표

RAG Context를 기반으로
LLM이 금융 문서를 해석하고
분석 결과를 생성하는
초기 금융 분석 Flow를 구축한다.

현재 TASK의 목표는
Retrieval 결과를 단순 검색에서 끝내지 않고
실제 금융 분석 응답으로 연결하는 것이다.

현재 단계에서는
복잡한 Agent 구조보다
단순하고 재현 가능한 분석 흐름에 집중한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Financial Analysis 디렉토리 구조 생성
- OpenAI Chat API 연동
- RAG Context 입력 구현
- 금융 분석 Prompt 구성
- 분석 결과 생성 구현
- 분석 결과 JSON 저장
- 분석 로그 기록
- 샘플 Query 분석 검증

---

# 현재 제외 범위

현재 TASK에서 제외:

- Multi-agent 구조
- 자율 투자 의사결정
- 실거래 연결
- 포트폴리오 관리
- Reflection 구조
- Character Layer
- Long-term Memory
- Self-improvement Loop
- 자동 Prompt 최적화
- Fine-tuning
- RLHF
- 백테스트 자동화
- 투자 성과 평가
- 실시간 스트리밍 분석
- 음성/멀티모달 분석

현재 TASK는
기본 금융 분석 Flow만 구현한다.

---

# 생성 대상 구조

```text
src/rag/analysis/
├─ __init__.py
├─ analyzer.py
├─ prompts.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/analysis/
```

예상 저장 파일 예시:

```text
data/analysis/samsung_financial_analysis.json
```

---

# 분석 역할

현재 분석 역할:

- Retrieval Context 해석
- 상승 요인 분석
- 하락 요인 분석
- 리스크 분석
- 핵심 뉴스 요약
- 핵심 공시 요약
- 금융 관점 설명

---

# 사용 모델

현재 기본 모델:

```text
gpt-4o-mini
```

현재 단계에서는
모델 비교 실험을 수행하지 않는다.

---

# 환경 변수 사용

사용 환경 변수:

```text
OPENAI_API_KEY
```

`.env` 기준으로 로드한다.

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- OpenAI 공식 SDK 사용
- Retrieval 결과 재사용
- 단순 Prompt 구조 우선
- 작은 함수 유지
- 명확한 오류 메시지 출력
- 분석 결과 추적 가능성 유지
- Context 원문 추적 가능성 유지
- 과도한 Prompt Engineering 금지
- 과도한 abstraction 금지

---

# 분석 흐름

현재 목표 흐름:

```text
사용자 Query 입력
→ Retrieval 수행
→ Context Assembly 수행
→ LLM Prompt 생성
→ OpenAI Chat API 호출
→ 금융 분석 생성
→ JSON 저장
→ 로그 기록
```

---

# Prompt 역할

현재 Prompt 역할:

- 금융 분석 요청
- Context 기반 응답 유도
- 근거 기반 분석 유도
- hallucination 최소화

---

# 예상 Prompt 구조

예상 Prompt 흐름:

```text
[질문]
삼성전자 반도체 전망 분석

[Context]
뉴스...
공시...

[분석 요청]
- 상승 요인
- 하락 요인
- 리스크
- 핵심 근거
```

---

# 예상 분석 결과 구조

예상 반환 형태:

```json
{
  "query": "...",
  "bullish_factors": [],
  "bearish_factors": [],
  "risks": [],
  "summary": "...",
  "referenced_chunks": []
}
```

---

# 예상 기능

## analyzer.py

역할:

- Retrieval 실행
- Context Assembly 실행
- Prompt 생성
- OpenAI Chat API 호출
- 분석 결과 반환

예상 함수:

```text
analyze_financial_query(query)
generate_financial_analysis(context)
```

---

## prompts.py

역할:

- 금융 분석 Prompt 생성
- 분석 지시문 관리
- Context 삽입

예상 함수:

```text
build_analysis_prompt(query, context)
```

---

## run_sample.py

역할:

- 샘플 Query 분석 실행
- 분석 결과 출력
- JSON 저장 검증

샘플 Query 예시:

```text
삼성전자 반도체 전망 분석
HBM 시장 성장 영향
AI 메모리 시장 전망
```

---

# 분석 제한 원칙

현재 단계에서는:

```text
- 투자 추천 금지
- 매수/매도 판단 금지
- 확정적 예측 금지
- 금융 자문 형태 금지
```

현재 역할은:

```text
정보 기반 분석 보조
```

수준으로 제한한다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## API 검증

- OpenAI Chat API 연결 성공 여부
- OPENAI_API_KEY 로드 성공 여부

---

## 분석 검증

- 분석 결과 생성 성공 여부
- 상승 요인 포함 여부
- 하락 요인 포함 여부
- 리스크 포함 여부
- summary 생성 여부

---

## Context 검증

- Retrieval Context 정상 포함 여부
- 뉴스/공시 Context 포함 여부
- Metadata 추적 가능 여부

---

## 저장 검증

- JSON 저장 성공 여부
- 분석 결과 파일 생성 여부

---

## 구조 검증

- `src/rag/analysis/` 생성 여부
- `data/analysis/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-011/
```

---

# 관련 Logs

```text
logs/TASK-011/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- 금융 분석 Flow 구축 완료
- OpenAI Chat API 연결 성공
- 금융 분석 생성 성공
- JSON 저장 성공
- 분석 로그 기록 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-012-build-analysis-evaluation
- TASK-013-build-character-layer
- TASK-014-build-memory-layer

단,
현재 TASK에서는
Agent 자율 의사결정을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- Retrieval 기반 분석 유지
- Context 추적 가능성 유지
- 근거 기반 분석 우선
- 단순한 Prompt 구조 우선
- AI 협업 가능한 구조 유지
- 과도한 Agent 구조 금지