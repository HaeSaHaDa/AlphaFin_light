# TASK-018-build-reflection-layer.md

# TASK-018 Reflection Layer 구축

## 상태

TODO

---

# 목표

이전 금융 분석 결과를
스스로 검토하고 평가할 수 있는
Reflection Layer를 구축한다.

현재 TASK의 목표는
AI가 생성한 금융 분석을 단순 저장하는 것을 넘어,
과거 분석의 품질과 정확성을 검토하고
개선 가능한 구조를 만드는 것이다.

현재 단계에서는
복잡한 자율 self-improving agent보다
명시적이고 추적 가능한 Reflection 구조에 집중한다.

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
→ Character Layer
→ Memory Layer
→ Market Event Graph
→ Layered Memory
```

현재 시스템은:

```text
분석 생성
→ 저장
```

까지는 가능하다.

하지만 현재 구조는:

```text
과거 분석이 적절했는지
```

를 다시 검토하지 않는다.

실제 금융 시장에서는:

- 잘못된 분석
- 과도한 낙관
- 리스크 누락
- 시장 변화 미반영

등이 발생한다.

현재 TASK에서는
AI가 과거 분석을 재검토하고
reflection memory를 생성할 수 있는 구조를 구축한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Reflection Layer 디렉토리 구조 생성
- 과거 분석 조회 구현
- Reflection Prompt 생성 구현
- 이전 분석 평가 구현
- 리스크 누락 검토 구현
- 과도한 낙관/비관 검토 구현
- Reflection Memory 저장 구현
- Reflection 기반 재분석 구조 구현
- Reflection JSON 저장
- 샘플 Reflection 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Reinforcement Learning
- Autonomous Self-improvement
- Fine-tuning
- Online Learning
- Reward Model
- Human Preference Learning
- 자동 Prompt 최적화
- 자율 투자 전략 생성
- 실거래 최적화
- Self-rewriting Agent
- Recursive Reflection Loop
- Reflection 기반 자동 매매

현재 TASK는
단순 Reflection Layer만 구현한다.

---

# 생성 대상 구조

```text
src/rag/reflection/
├─ __init__.py
├─ reflection_analyzer.py
├─ reflection_store.py
├─ prompt_builder.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/reflection/
```

예상 저장 파일 예시:

```text
data/reflection/samsung_hbm_reflection.json
data/reflection/ai_memory_market_reflection.json
```

---

# Reflection 역할

현재 Reflection 역할:

- 과거 분석 재검토
- 과도한 낙관/비관 탐지
- 리스크 누락 탐지
- Context 부족 여부 검토
- 시장 변화 반영 여부 검토
- Reflection Memory 생성

---

# Reflection 대상

현재 Reflection 대상:

```text
- bullish_factors
- bearish_factors
- risks
- summary
- referenced_chunks
- retrieval_quality
- hallucination_risk
```

---

# Reflection 관점

현재 Reflection 관점:

```text
- 과도한 낙관 여부
- 과도한 비관 여부
- 리스크 누락 여부
- 근거 부족 여부
- Context 부족 여부
- 시장 변화 반영 여부
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Financial Analysis 재사용
- 기존 Evaluation 결과 재사용
- 기존 Memory Layer 재사용
- 기존 Layered Memory 재사용
- Reflection 결과 추적 가능성 유지
- Reflection source 추적 가능성 유지
- 작은 함수 유지
- Recursive Reflection Loop 금지
- 과도한 abstraction 금지

---

# Reflection 흐름

현재 목표 흐름:

```text
과거 분석 조회
→ Evaluation 결과 조회
→ Reflection Prompt 생성
→ Reflection Analysis 수행
→ Reflection Memory 생성
→ Reflection 저장
→ 재분석 Context 강화
```

---

# Reflection Context 목표

예상 흐름:

```text
[Previous Analysis]
HBM 수요 증가 전망

[Reflection]
AI 메모리 수요 증가만 강조되었고
공급 과잉 가능성은 충분히 고려되지 않았음
```

---

# 예상 Reflection 구조

예상 반환 형태:

```json
{
  "query": "...",
  "reflection_summary": "...",
  "missing_risks": [],
  "overconfidence_detected": true,
  "context_gaps": [],
  "improvement_suggestions": []
}
```

---

# 예상 기능

## reflection_analyzer.py

역할:

- Reflection 생성
- 과거 분석 재평가
- Reflection Prompt 실행

예상 함수:

```text
analyze_reflection(result)
detect_overconfidence(result)
detect_missing_risks(result)
```

---

## reflection_store.py

역할:

- Reflection 저장
- Reflection 조회
- Reflection Memory 관리

예상 함수:

```text
save_reflection(reflection)
load_reflections(query)
```

---

## prompt_builder.py

역할:

- Reflection Prompt 생성
- Reflection Context 구성

예상 함수:

```text
build_reflection_prompt(result, evaluation)
```

---

## run_sample.py

역할:

- 샘플 Reflection 실행
- Reflection 저장 검증
- Reflection 기반 재분석 검증

샘플 Query 예시:

```text
HBM 시장 성장
AI 메모리 수요 증가
삼성전자 반도체 전망 분석
```

---

# Reflection 활용 목표

현재 활용 목표:

```text
- 과거 분석 개선
- 리스크 누락 방지
- Context 품질 개선
- 장기 Memory 품질 향상
- Character 편향 완화
```

현재 단계에서는
자동 투자 판단을 수행하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Reflection 생성 검증

- Reflection 생성 성공 여부
- Reflection Prompt 생성 여부
- Reflection JSON 저장 여부

---

## Reflection 품질 검증

- missing_risks 생성 여부
- overconfidence_detected 생성 여부
- context_gaps 생성 여부
- improvement_suggestions 생성 여부

---

## Memory 연동 검증

- Reflection Memory 저장 여부
- Layered Memory 연동 여부
- Character Layer 연동 여부

---

## 재분석 검증

- Reflection 기반 Context 강화 여부
- Reflection 기반 재분석 가능 여부

---

## 구조 검증

- `src/rag/reflection/` 생성 여부
- `data/reflection/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-018/
```

---

# 관련 Logs

```text
logs/TASK-018/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Reflection Layer 구축 완료
- Reflection 생성 성공
- Reflection Memory 저장 성공
- Reflection 기반 재분석 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-019-build-memory-importance-system
- TASK-020-build-temporal-market-memory
- TASK-021-build-stock-chain-layer

단,
현재 TASK에서는
자율 투자 Agent를 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Reflection 기반 개선 유지
- Retrieval 기반 분석 유지
- Context 추적 가능성 유지
- Reflection 추적 가능성 유지
- AI 협업 가능한 구조 유지
- 과도한 Self-improving Agent 구조 금지