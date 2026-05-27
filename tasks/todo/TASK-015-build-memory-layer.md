# TASK-015-build-memory-layer.md

# TASK-015 금융 분석 Memory Layer 구축

## 상태

TODO

---

# 목표

이전 금융 분석 결과와
과거 시장 이벤트를 저장하고 재사용할 수 있는
Memory Layer를 구축한다.

현재 TASK의 목표는
단발성 RAG 분석을 넘어,
과거 분석과 시장 흐름을 참조 가능한
Memory 기반 분석 구조를 만드는 것이다.

현재 단계에서는
복잡한 자율 Agent Memory보다
단순하고 추적 가능한 분석 메모리에 집중한다.

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
```

현재 시스템은
매 Query마다
독립적으로 분석을 수행한다.

즉:

```text
과거 분석 결과
과거 시장 이벤트
이전 Retrieval 결과
```

를 기억하지 않는다.

현재 TASK에서는
이전 분석과 시장 이벤트를 저장하고
재사용 가능한 Memory Layer를 구축한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Memory Layer 디렉토리 구조 생성
- Analysis Memory 저장 구조 구현
- Market Event Memory 저장 구조 구현
- 과거 분석 조회 기능 구현
- Memory Retrieval 구현
- Memory 기반 Context 추가 구현
- Character 기반 Memory 연결 구현
- Memory JSON 저장
- 샘플 Memory 기반 분석 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Long-term Autonomous Agent
- Self-improving Memory
- Reflection Loop
- Episodic Planning
- Reinforcement Learning
- Online Learning
- Multi-agent Shared Memory
- 실거래 전략 최적화
- 자동 투자 성과 학습
- Memory Importance Scoring 고도화
- Graph Memory
- Knowledge Graph
- 벡터 기반 장기 메모리 최적화

현재 TASK는
단순 금융 분석 Memory Layer만 구현한다.

---

# 생성 대상 구조

```text
src/rag/memory/
├─ __init__.py
├─ memory_store.py
├─ memory_retriever.py
├─ event_memory.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/memory/
├─ analysis_memory/
└─ market_events/
```

예상 저장 파일 예시:

```text
data/memory/analysis_memory/samsung_analysis_memory.json
data/memory/market_events/hbm_market_event.json
```

---

# Memory 역할

현재 Memory 역할:

- 과거 분석 결과 저장
- 과거 Retrieval 결과 저장
- 주요 시장 이벤트 저장
- 이전 시장 흐름 재사용
- Character 기반 분석 연속성 제공
- 분석 Context 강화

---

# Memory 종류

## Analysis Memory

저장 대상:

```text
- query
- persona
- bullish_factors
- bearish_factors
- risks
- summary
- referenced_chunks
- timestamp
```

---

## Market Event Memory

저장 대상:

```text
- ticker
- event_name
- event_summary
- related_news
- related_disclosures
- event_date
- impact_type
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Retrieval 재사용
- 기존 Context Assembly 재사용
- 기존 Financial Analysis 재사용
- 기존 Character Layer 재사용
- Metadata 추적 가능성 유지
- Memory 원문 추적 가능성 유지
- Memory 저장/조회 분리 유지
- 작은 함수 유지
- 과도한 Agent 구조 금지
- 과도한 abstraction 금지

---

# Memory 흐름

현재 목표 흐름:

```text
사용자 Query 입력
→ Retrieval 수행
→ Context Assembly 수행
→ 기존 Memory 조회
→ 관련 Memory 선택
→ Memory Context 추가
→ Financial Analysis 수행
→ 새로운 Analysis Memory 저장
→ Event Memory 저장
```

---

# Memory Retrieval 역할

현재 역할:

- 유사 Query 기반 Memory 조회
- ticker 기반 과거 이벤트 조회
- persona 기반 과거 분석 조회
- 최근 분석 흐름 유지

---

# 예상 Memory Context 구조

예상 흐름:

```text
[Previous Analysis]
지난 분석:
- HBM 수요 증가 지속
- AI 서버 투자 확대

[Market Event]
- DRAM 가격 반등
- AI 메모리 공급 부족

[Current Context]
뉴스...
공시...
```

---

# 예상 Memory 저장 구조

예상 반환 형태:

```json
{
  "memory_type": "analysis_memory",
  "query": "...",
  "persona": "growth_investor",
  "summary": "...",
  "timestamp": "2026-05-27"
}
```

---

# 예상 기능

## memory_store.py

역할:

- Analysis Memory 저장
- Event Memory 저장
- JSON 저장 관리

예상 함수:

```text
save_analysis_memory(result)
save_market_event_memory(event)
```

---

## memory_retriever.py

역할:

- 관련 Memory 조회
- 유사 Query 기반 Memory 검색
- persona 기반 Memory 조회

예상 함수:

```text
retrieve_related_memories(query)
retrieve_persona_memories(persona)
```

---

## event_memory.py

역할:

- 주요 시장 이벤트 저장
- 이벤트 추출
- ticker 기반 이벤트 관리

예상 함수:

```text
extract_market_events(result)
build_event_memory(event_data)
```

---

## run_sample.py

역할:

- 샘플 Query 실행
- Memory 저장 검증
- Memory Retrieval 검증
- Memory 기반 분석 검증

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

## Memory 저장 검증

- Analysis Memory 저장 성공 여부
- Event Memory 저장 성공 여부
- JSON 저장 성공 여부

---

## Memory Retrieval 검증

- 관련 Memory 조회 성공 여부
- persona 기반 Memory 조회 여부
- ticker 기반 Event 조회 여부

---

## Memory Context 검증

- 이전 분석 Context 포함 여부
- Event Memory 포함 여부
- Character 기반 연속성 여부

---

## 분석 검증

- Memory 기반 분석 결과 생성 여부
- 이전 분석과 연결성 존재 여부

---

## 구조 검증

- `src/rag/memory/` 생성 여부
- `data/memory/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-015/
```

---

# 관련 Logs

```text
logs/TASK-015/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Memory Layer 구축 완료
- Analysis Memory 저장 성공
- Event Memory 저장 성공
- Memory Retrieval 성공
- Memory 기반 분석 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-016-build-market-event-memory-enhancement
- TASK-017-build-reflection-layer
- TASK-018-build-dashboard-layer

단,
현재 TASK에서는
자율 투자 Agent를 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Memory 기반 분석 연속성 유지
- Retrieval 기반 분석 유지
- Context 추적 가능성 유지
- Event 추적 가능성 유지
- Character 기반 Memory 유지
- AI 협업 가능한 구조 유지
- 과도한 Agent 구조 금지