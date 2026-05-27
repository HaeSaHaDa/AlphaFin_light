# TASK-021-build-stock-chain-layer.md

# TASK-021 Stock Chain Layer 구축

## 상태

TODO

---

# 목표

기업, 산업, 제품, 공급망, 시장 이벤트 간의
연결 관계를 추적 가능한
Stock Chain Layer를 구축한다.

현재 TASK의 목표는
단순 Event Graph를 넘어,
금융 시장의 공급망 및 산업 연결 구조를
체계적으로 표현하는 것이다.

현재 단계에서는
복잡한 Knowledge Graph보다
명시적이고 추적 가능한 Stock Chain 구조에 집중한다.

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
→ Reflection
→ Memory Importance
→ Temporal Market Memory
```

현재 시스템은:

```text
Event 관계
```

까지는 추적 가능하다.

하지만 실제 금융 시장은:

```text
기업
→ 공급망
→ 산업
→ 제품
→ 수요 변화
→ 가격 변화
```

처럼 복합적인 Chain 구조로 움직인다.

현재 TASK에서는
이러한 시장 구조 연결망을
Stock Chain으로 표현한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Stock Chain 디렉토리 구조 생성
- 기업(Entity) 추출 구현
- 공급망 관계 추출 구현
- 산업 연결 관계 구현
- 제품 기반 Chain 연결 구현
- 영향 propagation 구조 구현
- ticker 기반 Chain 조회 구현
- Stock Chain JSON 저장 구현
- Event Graph 연동 구현
- Temporal Memory 연동 구현
- 샘플 Stock Chain 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Knowledge Graph Database
- Neo4j 도입
- Graph Neural Network
- Reinforcement Learning
- Autonomous Investment Agent
- 실시간 글로벌 공급망 추적
- 대규모 경제 네트워크 분석
- Causal AI
- Dynamic Market Simulation
- 실거래 전략 생성
- 자동 포트폴리오 최적화
- Fully Autonomous Market Reasoning

현재 TASK는
정적 Stock Chain Layer만 구현한다.

---

# 생성 대상 구조

```text
src/rag/stock_chain/
├─ __init__.py
├─ entity_extractor.py
├─ chain_builder.py
├─ propagation_engine.py
├─ chain_store.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/stock_chain/
```

예상 저장 파일 예시:

```text
data/stock_chain/hbm_supply_chain.json
data/stock_chain/ai_server_memory_chain.json
```

---

# Stock Chain 역할

현재 Stock Chain 역할:

- 기업 연결 관계 표현
- 공급망 영향 추적
- 산업 영향 추적
- 시장 이벤트 propagation 표현
- Retrieval Context 강화
- Financial Analysis reasoning 강화

---

# Stock Chain 대상

현재 Chain 대상:

```text
- 기업
- 산업
- 제품
- 공급망
- 기술
- 시장 이벤트
- 가격 변화
```

예시:

```text
NVIDIA
HBM
삼성전자
SK하이닉스
AI 서버
DRAM 가격
```

---

# Chain 예시

예시:

```text
NVIDIA GPU 수요 증가
→ AI 서버 확대
→ HBM 수요 증가
→ 삼성전자 수혜 가능성
→ DRAM 가격 상승
```

---

# Propagation 역할

현재 Propagation 역할:

- 이벤트 영향 전파
- 산업 영향 확산
- 공급망 영향 추적
- 시장 반응 연결

---

# Propagation 예시

예시:

```text
미국 금리 인상
→ 소비 둔화
→ IT 투자 감소
→ 반도체 수요 감소
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Event Graph 재사용
- 기존 Temporal Memory 재사용
- 기존 Memory Importance 재사용
- 기존 Retrieval 재사용
- Chain source 추적 가능성 유지
- propagation log 유지
- 작은 함수 유지
- 과도한 abstraction 금지
- 자율 투자 Agent 구조 금지

---

# Stock Chain 흐름

현재 목표 흐름:

```text
뉴스/공시 입력
→ Entity 추출
→ 산업/제품 연결
→ 공급망 연결
→ Chain 생성
→ propagation 계산
→ Stock Chain 저장
→ Context 강화
```

---

# Stock Chain Context 목표

예상 흐름:

```text
[NVIDIA]
AI GPU 수요 증가

↓

[AI Server]
AI 서버 투자 확대

↓

[HBM]
HBM 수요 증가

↓

[삼성전자]
메모리 수혜 가능성 증가
```

---

# 예상 Chain 구조

예상 반환 형태:

```json
{
  "source": "NVIDIA",
  "target": "HBM",
  "relation_type": "demand_propagation",
  "impact_score": 0.88
}
```

---

# 예상 기능

## entity_extractor.py

역할:

- 기업/산업/제품 추출
- ticker 연결
- Entity 정규화

예상 함수:

```text
extract_market_entities(text)
normalize_entities(entities)
```

---

## chain_builder.py

역할:

- Stock Chain 생성
- 공급망 연결
- 산업 연결 생성

예상 함수:

```text
build_stock_chain(entities)
build_supply_chain_relations(entities)
```

---

## propagation_engine.py

역할:

- 영향 propagation 계산
- 이벤트 영향 전파 계산

예상 함수:

```text
calculate_propagation(chain)
propagate_market_impact(chain)
```

---

## chain_store.py

역할:

- Stock Chain 저장
- Chain 조회
- propagation log 저장

예상 함수:

```text
save_stock_chain(chain)
load_related_chains(ticker)
```

---

## run_sample.py

역할:

- 샘플 Chain 생성
- propagation 검증
- Chain 저장 검증

샘플 Query 예시:

```text
NVIDIA GPU 수요 증가
HBM 공급 부족
AI 서버 투자 확대
```

---

# Stock Chain 활용 목표

현재 활용 목표:

```text
- 시장 구조 이해 강화
- 공급망 영향 추적
- 산업 영향 propagation 이해
- Financial Analysis reasoning 강화
- Retrieval Context 강화
```

현재 단계에서는
자동 투자 판단을 수행하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Entity 검증

- Entity 추출 성공 여부
- ticker 연결 성공 여부
- Entity 정규화 성공 여부

---

## Chain 검증

- Chain 생성 성공 여부
- 공급망 연결 성공 여부
- relation_type 생성 여부
- impact_score 생성 여부

---

## Propagation 검증

- propagation 계산 성공 여부
- 영향 전파 추적 여부
- propagation log 생성 여부

---

## Context 검증

- Stock Chain Context 생성 여부
- Event Graph 연동 여부
- Temporal Memory 연동 여부

---

## 구조 검증

- `src/rag/stock_chain/` 생성 여부
- `data/stock_chain/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-021/
```

---

# 관련 Logs

```text
logs/TASK-021/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Stock Chain 구축 완료
- Entity 추출 성공
- 공급망 연결 성공
- propagation 계산 성공
- Stock Chain 저장 성공
- Context 강화 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-022-build-unified-engine-runner
- TASK-023-build-engine-evaluation-suite
- TASK-024-build-dashboard-backend-api

단,
현재 TASK에서는
자율 투자 Agent를 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 시장 구조 연결 우선
- 공급망 영향 추적 유지
- Retrieval 기반 분석 유지
- Context 강화 가능성 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지