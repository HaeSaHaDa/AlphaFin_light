# TASK-014-build-character-layer.md

# TASK-014 금융 분석 Character Layer 구축

## 상태

TODO

---

# 목표

동일한 Retrieval 및 Context를 기반으로 하더라도
분석 관점(Persona/Character)에 따라
다른 금융 해석 결과를 생성할 수 있는
Character Layer를 구축한다.

현재 TASK의 목표는
금융 분석 스타일을 구조화하고,
분석 성향 기반 RAG 분석 흐름을 만드는 것이다.

현재 단계에서는
복잡한 Multi-agent 구조보다
단순하고 재현 가능한 Persona 기반 분석에 집중한다.

---

# 배경

현재 프로젝트는 다음 흐름까지 구축 완료되었다.

```text
수집
→ 저장
→ Chunking
→ Embedding
→ Semantic Retrieval
→ Context Assembly
→ Financial Analysis
→ Evaluation
```

현재 시스템은
동일 Query에 대해
단일 분석 스타일만 생성한다.

하지만 실제 금융 분석은:

- 보수적 관점
- 공격적 성장 관점
- 가치 투자 관점
- 리스크 관리 관점

등에 따라
동일 데이터를 다르게 해석한다.

현재 TASK에서는
이러한 분석 성향 Layer를 구조화한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Character Layer 디렉토리 구조 생성
- Persona 정의 구조 생성
- Persona Prompt Layer 구현
- Character 기반 분석 흐름 구현
- Character별 Prompt 분기 구현
- Character별 분석 결과 저장
- Character별 Evaluation 비교
- 샘플 Persona 분석 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Multi-agent Debate
- Agent 간 토론 구조
- Reflection Loop
- Long-term Personality Learning
- Self-improving Character
- 실거래 투자 전략
- 포트폴리오 운영
- Reinforcement Learning
- Fine-tuning
- 온라인 학습
- 자동 Persona 생성
- 감정 분석 Agent
- 실시간 트레이딩 Agent

현재 TASK는
정적 Persona 기반 분석 구조만 구현한다.

---

# 생성 대상 구조

```text
src/rag/character/
├─ __init__.py
├─ personas.py
├─ prompt_builder.py
├─ analyzer.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/character_analysis/
```

예상 저장 파일 예시:

```text
data/character_analysis/samsung_growth_investor.json
data/character_analysis/samsung_risk_averse.json
```

---

# Character 역할

현재 Character 역할:

- 금융 분석 관점 분리
- Prompt 스타일 분기
- 분석 강조 포인트 변경
- 동일 Context의 다른 해석 생성
- Persona 기반 분석 비교

---

# 현재 Persona 대상

현재 기본 Persona:

```text
- growth_investor
- value_investor
- risk_averse_analyst
- aggressive_trader
```

---

# Persona 설명

## growth_investor

관점:

```text
- 성장 가능성 중시
- AI/반도체 성장 강조
- 시장 확대 가능성 중시
```

---

## value_investor

관점:

```text
- 실적 기반 안정성 중시
- 저평가 여부 중시
- 재무 안정성 중시
```

---

## risk_averse_analyst

관점:

```text
- 리스크 우선 분석
- 불확실성 강조
- downside 위험 강조
```

---

## aggressive_trader

관점:

```text
- 단기 이벤트 민감
- 변동성 활용 관점
- 시장 모멘텀 중시
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Retrieval 재사용
- 기존 Context 재사용
- 기존 Financial Analysis Flow 재사용
- Persona Prompt만 변경
- Metadata 추적 가능성 유지
- Character별 결과 비교 가능성 유지
- 작은 함수 유지
- 과도한 Multi-agent 구조 금지
- 과도한 abstraction 금지

---

# 분석 흐름

현재 목표 흐름:

```text
사용자 Query 입력
→ Retrieval 수행
→ Context Assembly 수행
→ Persona 선택
→ Persona Prompt 생성
→ OpenAI Chat API 호출
→ Character 기반 분석 생성
→ JSON 저장
→ Evaluation 비교
```

---

# Prompt 역할

현재 Prompt 역할:

- Persona 관점 부여
- 분석 강조 방향 변경
- 동일 Context의 다른 해석 유도
- 분석 스타일 분리

---

# 예상 Prompt 구조

예상 흐름:

```text
[Persona]
Growth Investor

[Query]
삼성전자 반도체 전망 분석

[Context]
뉴스...
공시...

[분석 요청]
성장 가능성과 시장 확대 관점 중심으로 분석
```

---

# 예상 분석 결과 구조

예상 반환 형태:

```json
{
  "persona": "growth_investor",
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

## personas.py

역할:

- Persona 정의
- Persona 설정 관리

예상 함수:

```text
get_persona_config(name)
list_available_personas()
```

---

## prompt_builder.py

역할:

- Persona 기반 Prompt 생성
- Persona 지시문 구성

예상 함수:

```text
build_character_prompt(persona, query, context)
```

---

## analyzer.py

역할:

- Persona 기반 분석 실행
- OpenAI Chat API 호출
- Character별 결과 저장

예상 함수:

```text
run_character_analysis(persona, query)
```

---

## run_sample.py

역할:

- Persona별 샘플 분석 실행
- 결과 비교 출력
- JSON 저장 검증

샘플 Query 예시:

```text
삼성전자 반도체 전망 분석
HBM 시장 성장 영향
AI 메모리 시장 전망
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Persona 검증

- Persona 로드 성공 여부
- Persona Prompt 생성 성공 여부

---

## 분석 검증

- Character별 분석 결과 생성 여부
- Persona별 관점 차이 존재 여부
- bullish/bearish 차이 존재 여부
- summary 차이 존재 여부

---

## 저장 검증

- Character별 JSON 저장 성공 여부
- Character별 결과 비교 가능 여부

---

## Evaluation 검증

- Persona별 Evaluation 비교 가능 여부
- hallucination_risk 추적 가능 여부

---

## 구조 검증

- `src/rag/character/` 생성 여부
- `data/character_analysis/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-014/
```

---

# 관련 Logs

```text
logs/TASK-014/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Character Layer 구축 완료
- Persona Prompt 생성 성공
- Character별 분석 생성 성공
- Character별 JSON 저장 성공
- Character별 Evaluation 비교 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-015-build-memory-layer
- TASK-016-build-market-event-memory
- TASK-017-build-reflection-layer

단,
현재 TASK에서는
자율 투자 Agent를 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Persona 기반 분석 분리
- Retrieval 기반 분석 유지
- Context 추적 가능성 유지
- Character 비교 가능성 유지
- AI 협업 가능한 구조 유지
- 과도한 Multi-agent 구조 금지