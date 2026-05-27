# TASK-017-build-layered-memory.md

# TASK-017 Layered Memory 구조 구축

## 상태

TODO

---

# 목표

금융 분석 Memory를
단기(Short-term),
중기(Mid-term),
장기(Long-term)
계층으로 분리하는
Layered Memory 구조를 구축한다.

현재 TASK의 목표는
모든 Memory를 동일하게 처리하지 않고,
시장 이벤트의 시간성과 중요도에 따라
다르게 유지 및 활용 가능한 구조를 만드는 것이다.

현재 단계에서는
복잡한 자율 Agent Memory보다
명시적이고 추적 가능한 계층형 Memory에 집중한다.

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
```

현재 Memory Layer는:

```text
- Analysis Memory
- Market Event Memory
```

를 저장하고 조회할 수 있다.

하지만 현재 구조는:

```text
모든 Memory를 동일한 중요도로 처리
```

한다.

실제 금융 시장은:

- 단기 뉴스 영향
- 중기 산업 변화
- 장기 시장 구조 변화

가 다르게 작동한다.

현재 TASK에서는
Memory를 시간성과 중요도 기반으로 계층화한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Layered Memory 디렉토리 구조 생성
- Short-term Memory 구조 구현
- Mid-term Memory 구조 구현
- Long-term Memory 구조 구현
- Memory importance score 구조 구현
- 시간 기반 Memory 분류 구현
- Memory expiration 구조 구현
- Layer별 Memory Retrieval 구현
- Layered Context Assembly 구현
- 샘플 Layered Memory 분석 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Reinforcement Learning
- Self-improving Memory
- Reflection Loop
- Autonomous Agent Planning
- Online Learning
- Graph Neural Network
- Knowledge Graph 고도화
- Attention 기반 Memory Weighting
- Memory Compression 최적화
- 실거래 전략 최적화
- 자동 투자 학습
- 벡터 기반 장기 기억 최적화

현재 TASK는
정적 Layered Memory 구조만 구현한다.

---

# 생성 대상 구조

```text
src/rag/layered_memory/
├─ __init__.py
├─ memory_classifier.py
├─ layered_store.py
├─ layered_retriever.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/layered_memory/
├─ short_term/
├─ mid_term/
└─ long_term/
```

예상 저장 파일 예시:

```text
data/layered_memory/short_term/recent_hbm_news.json
data/layered_memory/mid_term/ai_memory_trend.json
data/layered_memory/long_term/semiconductor_cycle.json
```

---

# Layer 역할

## Short-term Memory

역할:

```text
- 최근 뉴스
- 최근 공시
- 단기 이벤트
- 단기 시장 반응
```

예시:

```text
최근 NVIDIA 실적 발표
최근 DRAM 가격 급등
```

---

## Mid-term Memory

역할:

```text
- 산업 변화
- 수요 변화
- 공급망 변화
- 기술 트렌드
```

예시:

```text
HBM 수요 증가 추세
AI 서버 투자 확대
```

---

## Long-term Memory

역할:

```text
- 장기 시장 구조
- 산업 사이클
- 거시 흐름
- 장기 경쟁 구도
```

예시:

```text
반도체 업황 사이클
AI 산업 장기 성장
```

---

# Memory Importance

현재 Memory 중요도 기준:

```text
- 반복 등장 빈도
- 시장 영향 범위
- 이벤트 지속 기간
- retrieval 재사용 빈도
- Character 분석 영향도
```

현재 단계에서는
단순 score 기반으로 관리한다.

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Memory Layer 재사용
- 기존 Event Graph 재사용
- 기존 Retrieval 재사용
- Layer별 저장 구조 분리 유지
- Metadata 추적 가능성 유지
- Memory source 추적 가능성 유지
- 작은 함수 유지
- 과도한 abstraction 금지
- 자율 Agent 구조 금지

---

# Layered Memory 흐름

현재 목표 흐름:

```text
새로운 분석 생성
→ Memory importance 계산
→ 시간 기반 분류
→ Short/Mid/Long-term 분리 저장
→ Layer별 Retrieval 수행
→ Layered Context 생성
→ Financial Analysis 강화
```

---

# Layered Context 목표

예상 흐름:

```text
[Short-term]
최근 NVIDIA 실적 발표

[Mid-term]
HBM 수요 증가 지속

[Long-term]
AI 산업 장기 성장 추세
```

---

# 예상 Memory 구조

예상 반환 형태:

```json
{
  "memory_layer": "mid_term",
  "importance_score": 0.84,
  "summary": "...",
  "source": "...",
  "timestamp": "2026-05-27"
}
```

---

# 예상 기능

## memory_classifier.py

역할:

- Memory Layer 분류
- importance score 계산
- 시간 기반 분류

예상 함수:

```text
classify_memory_layer(memory)
calculate_importance_score(memory)
```

---

## layered_store.py

역할:

- Layer별 Memory 저장
- expiration 관리

예상 함수:

```text
save_short_term_memory(memory)
save_mid_term_memory(memory)
save_long_term_memory(memory)
```

---

## layered_retriever.py

역할:

- Layer별 Retrieval
- Layered Context 생성

예상 함수:

```text
retrieve_short_term_memories(query)
retrieve_mid_term_memories(query)
retrieve_long_term_memories(query)
```

---

## run_sample.py

역할:

- 샘플 Query 실행
- Layer 분류 검증
- Layered Context 검증
- JSON 저장 검증

샘플 Query 예시:

```text
HBM 시장 성장
AI 메모리 수요 증가
삼성전자 반도체 전망 분석
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Memory Layer 검증

- Short-term 저장 성공 여부
- Mid-term 저장 성공 여부
- Long-term 저장 성공 여부

---

## Importance 검증

- importance_score 생성 여부
- score 기반 Layer 분류 여부

---

## Retrieval 검증

- Layer별 Retrieval 성공 여부
- Layered Context 생성 여부

---

## Context 검증

- Layer별 Context 포함 여부
- 시간 기반 흐름 유지 여부
- Character Layer 연동 여부

---

## 구조 검증

- `src/rag/layered_memory/` 생성 여부
- `data/layered_memory/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-017/
```

---

# 관련 Logs

```text
logs/TASK-017/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Layered Memory 구축 완료
- Layer별 Memory 저장 성공
- importance_score 생성 성공
- Layer별 Retrieval 성공
- Layered Context 생성 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-018-build-reflection-layer
- TASK-019-build-memory-importance-system
- TASK-020-build-temporal-market-memory

단,
현재 TASK에서는
자율 투자 Agent를 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 시간 기반 Memory 구조 유지
- Retrieval 기반 분석 유지
- Layer별 추적 가능성 유지
- Context 강화 가능성 유지
- AI 협업 가능한 구조 유지
- 과도한 Agent 구조 금지