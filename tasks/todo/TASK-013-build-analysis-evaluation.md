# TASK-013-build-analysis-evaluation.md

# TASK-013 금융 분석 평가 파이프라인 구축

## 상태

TODO

---

# 목표

현재 구축된 RAG 금융 분석 시스템의
Retrieval 품질과 분석 품질을 평가하는
초기 Evaluation Pipeline을 구축한다.

현재 TASK의 목표는
LLM 분석 결과가
실제 Retrieval Context를 기반으로 생성되었는지 검증하고,
분석 품질을 추적 가능한 형태로 기록하는 것이다.

현재 단계에서는
복잡한 자동 평가보다
명시적이고 재현 가능한 평가 구조에 집중한다.

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
```

TASK-012에서
실제 OpenAI Embedding 재생성을 통해
Semantic Retrieval 품질이 정상화되었다.

현재 단계에서는
RAG 결과 품질과 근거 기반 분석 여부를 검증한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Evaluation 디렉토리 구조 생성
- Retrieval 품질 평가 구현
- 분석 결과 평가 구현
- Context 기반 응답 여부 검증
- Hallucination 추정 검증
- Similarity score 기록
- 분석 결과 비교 저장
- Evaluation JSON 저장
- Evaluation 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 자동 투자 성과 평가
- 백테스트 자동화
- RLHF
- Fine-tuning
- Human Preference Learning
- Multi-agent 평가
- Reinforcement Learning
- 실시간 운영 평가
- 자동 Prompt 최적화
- 온라인 학습
- A/B 테스트 자동화
- 대규모 벤치마크

현재 TASK는
RAG 분석 품질 검증에만 집중한다.

---

# 생성 대상 구조

```text
src/rag/evaluation/
├─ __init__.py
├─ evaluator.py
├─ metrics.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/evaluation/
```

예상 저장 파일 예시:

```text
data/evaluation/samsung_analysis_eval.json
```

---

# 평가 역할

현재 평가 역할:

- Retrieval relevance 검증
- Context 사용 여부 검증
- 분석 근거 추적
- hallucination 가능성 추정
- score 기록
- 분석 결과 비교

---

# 평가 기준

현재 평가 기준:

```text
- Retrieval score
- Context relevance
- Context 기반 응답 여부
- 근거 포함 여부
- hallucination 추정 여부
- 응답 구조 일관성
```

현재 단계에서는
정량적 금융 성과 평가를 수행하지 않는다.

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Retrieval 결과 재사용
- 기존 Context 재사용
- 기존 Analysis 결과 재사용
- 근거 기반 평가 우선
- 작은 함수 유지
- 명확한 평가 로그 출력
- Metadata 추적 가능성 유지
- 과도한 자동화 금지
- 과도한 abstraction 금지

---

# 평가 흐름

현재 목표 흐름:

```text
Query 입력
→ Retrieval 실행
→ Context 생성
→ Financial Analysis 실행
→ 분석 결과 평가
→ Retrieval score 기록
→ hallucination 여부 추정
→ Evaluation JSON 저장
→ 로그 기록
```

---

# 평가 대상

현재 평가 대상:

```text
- Query
- Retrieved Chunks
- Similarity Scores
- Context
- Analysis Result
- Referenced Chunks
```

---

# 예상 Evaluation 구조

예상 반환 형태:

```json
{
  "query": "...",
  "retrieval_quality": {},
  "analysis_quality": {},
  "hallucination_risk": "...",
  "context_usage": {},
  "scores": {}
}
```

---

# 예상 기능

## evaluator.py

역할:

- 분석 결과 평가
- Context 사용 여부 검증
- Retrieval relevance 평가

예상 함수:

```text
evaluate_analysis_result(result)
evaluate_context_usage(result, context)
evaluate_retrieval_quality(chunks)
```

---

## metrics.py

역할:

- similarity score 계산
- score 정리
- hallucination 추정 기준 관리

예상 함수:

```text
calculate_average_similarity(scores)
detect_possible_hallucination(result, context)
```

---

## run_sample.py

역할:

- 샘플 Query 실행
- Retrieval 수행
- Analysis 수행
- Evaluation 수행
- JSON 저장 검증

샘플 Query 예시:

```text
삼성전자 반도체 전망 분석
HBM 시장 성장 영향
AI 메모리 시장 전망
```

---

# hallucination 판단 기준

현재 기준:

```text
- Context에 없는 정보 사용 여부
- referenced_chunks 미사용 여부
- retrieval relevance 낮은 경우
- 근거 없이 단정 표현 사용 여부
```

현재 단계에서는
정교한 자동 hallucination detection을 구현하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Retrieval 평가 검증

- similarity score 정상 기록 여부
- 관련 Chunk retrieval 여부
- relevance 추정 가능 여부

---

## Analysis 평가 검증

- Context 기반 응답 여부
- 상승 요인 근거 여부
- 하락 요인 근거 여부
- risks 근거 여부

---

## hallucination 검증

- Context 외 정보 사용 여부 추정 가능 여부
- hallucination_risk 생성 여부

---

## 저장 검증

- Evaluation JSON 저장 성공 여부
- Evaluation 로그 기록 여부

---

## 구조 검증

- `src/rag/evaluation/` 생성 여부
- `data/evaluation/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-013/
```

---

# 관련 Logs

```text
logs/TASK-013/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Evaluation Pipeline 구축 완료
- Retrieval 품질 평가 성공
- Analysis 품질 평가 성공
- hallucination 추정 성공
- Evaluation JSON 저장 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-014-build-character-layer
- TASK-015-build-memory-layer
- TASK-016-build-market-event-memory

단,
현재 TASK에서는
자율 투자 Agent를 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 근거 기반 평가 우선
- Retrieval 추적 가능성 유지
- Context 추적 가능성 유지
- 분석 결과 재현 가능성 유지
- AI 협업 가능한 구조 유지
- 과도한 자동화 금지