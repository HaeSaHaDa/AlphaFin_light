# TASK-022-build-unified-engine-runner.md

# TASK-022 Unified Engine Runner 구축

## 상태

TODO

---

# 목표

지금까지 구축한 모든 금융 AI 엔진 구성 요소를
하나의 End-to-End 실행 파이프라인으로 통합하는
Unified Engine Runner를 구축한다.

현재 TASK의 목표는
개별 모듈 단위 구현을 넘어,
실제 금융 분석 흐름처럼 동작하는
통합 금융 AI 엔진을 만드는 것이다.

현재 단계에서는
복잡한 autonomous orchestration보다
명시적이고 추적 가능한 sequential pipeline에 집중한다.

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
→ Stock Chain
```

현재 시스템은:

```text
각 기능별 모듈
```

은 존재하지만,

```text
전체 엔진을 하나의 흐름으로 실행
```

하는 구조는 아직 없다.

현재 TASK에서는
모든 엔진 구성 요소를 연결하여
End-to-End 금융 AI 파이프라인을 구축한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Unified Engine 디렉토리 구조 생성
- 전체 Pipeline Runner 구현
- Retrieval → Analysis → Reflection 연결 구현
- Memory → Temporal → Stock Chain 연결 구현
- Character 기반 분석 흐름 연결 구현
- Event Graph 연동 구현
- Context Assembly 통합 구현
- Unified Result JSON 생성 구현
- Full Engine Trace Log 생성 구현
- 샘플 End-to-End 실행 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Multi-agent orchestration
- Autonomous planning
- Reinforcement Learning
- Online Learning
- 실시간 자동 투자 시스템
- Distributed orchestration
- Kafka/Event Streaming
- Ray/Spark 분산 처리
- Autonomous Trading Agent
- 실거래 전략 실행
- Auto Prompt Optimization
- Fully Autonomous Financial AI

현재 TASK는
단일 프로세스 기반 Unified Engine만 구현한다.

---

# 생성 대상 구조

```text
src/rag/unified_engine/
├─ __init__.py
├─ engine_runner.py
├─ pipeline_manager.py
├─ context_orchestrator.py
├─ result_builder.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/unified_engine/
├─ engine_runs/
├─ traces/
└─ final_results/
```

예상 저장 파일 예시:

```text
data/unified_engine/final_results/samsung_hbm_analysis.json
data/unified_engine/traces/full_pipeline_trace.json
```

---

# Unified Engine 역할

현재 Unified Engine 역할:

- 전체 금융 AI 흐름 실행
- Retrieval 흐름 통합
- Memory 흐름 통합
- Reflection 흐름 통합
- Temporal 흐름 통합
- Stock Chain 흐름 통합
- Full Pipeline Trace 생성

---

# Unified Pipeline 구성

현재 통합 대상:

```text
- Retrieval
- Context Assembly
- Character Layer
- Financial Analysis
- Evaluation
- Reflection
- Memory Layer
- Memory Importance
- Temporal Memory
- Event Graph
- Stock Chain
```

---

# Unified 흐름

현재 목표 흐름:

```text
사용자 Query 입력
→ Retrieval 수행
→ Context Assembly 수행
→ Character 분석 수행
→ Financial Analysis 수행
→ Evaluation 수행
→ Reflection 수행
→ Memory 저장
→ Importance 계산
→ Temporal Tracking 수행
→ Event Graph 생성
→ Stock Chain 생성
→ Unified Result 저장
→ Full Trace 저장
```

---

# Full Trace 역할

현재 Full Trace 역할:

- 전체 reasoning 흐름 기록
- Retrieval 결과 기록
- Context 기록
- Reflection 기록
- Temporal 이동 기록
- Stock Chain 기록
- 최종 분석 추적 가능성 유지

---

# Trace 예시

예상 Trace 흐름:

```text
Query 입력
→ Retrieval 수행
→ similarity score 계산
→ Context 생성
→ Character 분석
→ Reflection 수행
→ importance 계산
→ Memory promotion 수행
→ Stock Chain propagation 수행
→ 최종 분석 생성
```

---

# Unified Result 목표

예상 결과:

```json
{
  "query": "...",
  "analysis_result": {},
  "reflection_result": {},
  "memory_updates": {},
  "stock_chain": {},
  "trace_id": "..."
}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 모든 모듈 재사용
- Full Trace 유지
- Metadata 추적 가능성 유지
- Pipeline 단계별 log 유지
- 작은 함수 유지
- 과도한 abstraction 금지
- 자율 투자 Agent 구조 금지

---

# 예상 기능

## engine_runner.py

역할:

- 전체 Pipeline 실행
- End-to-End 흐름 제어

예상 함수:

```text
run_financial_engine(query)
```

---

## pipeline_manager.py

역할:

- 단계별 실행 관리
- Pipeline orchestration

예상 함수:

```text
run_pipeline_stage(stage)
execute_pipeline(query)
```

---

## context_orchestrator.py

역할:

- 모든 Context 통합
- Layered Context 생성

예상 함수:

```text
build_unified_context(query)
merge_contexts(contexts)
```

---

## result_builder.py

역할:

- Unified Result 생성
- Final JSON 생성
- Trace metadata 생성

예상 함수:

```text
build_final_result(data)
build_trace_log(trace)
```

---

## run_sample.py

역할:

- 샘플 End-to-End 실행
- Full Trace 검증
- Unified Result 검증

샘플 Query 예시:

```text
삼성전자 반도체 전망 분석
HBM 공급 부족 영향
AI 서버 투자 확대
```

---

# Unified Engine 활용 목표

현재 활용 목표:

```text
- 실제 금융 AI 엔진 실행
- End-to-End reasoning 검증
- Full Trace 분석
- Memory lifecycle 검증
- Stock Chain reasoning 검증
```

현재 단계에서는
자동 투자 판단을 수행하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Pipeline 검증

- End-to-End 실행 성공 여부
- Pipeline 단계별 실행 성공 여부
- 단계별 log 생성 여부

---

## Context 검증

- Unified Context 생성 여부
- Layered Context 통합 여부
- Reflection 연동 여부
- Stock Chain 연동 여부

---

## Trace 검증

- Full Trace 생성 여부
- Trace 저장 여부
- reasoning 흐름 추적 가능 여부

---

## Result 검증

- Unified Result JSON 생성 여부
- Final Result 저장 여부
- metadata 저장 여부

---

## 구조 검증

- `src/rag/unified_engine/` 생성 여부
- `data/unified_engine/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-022/
```

---

# 관련 Logs

```text
logs/TASK-022/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Unified Engine 구축 완료
- End-to-End 실행 성공
- Unified Context 생성 성공
- Full Trace 생성 성공
- Unified Result 저장 성공
- Pipeline log 생성 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-023-build-engine-evaluation-suite
- TASK-024-build-dashboard-backend-api
- TASK-025-build-dashboard-ui

단,
현재 TASK에서는
자율 투자 Agent를 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- End-to-End 추적 가능성 유지
- Retrieval 기반 분석 유지
- Memory lifecycle 유지
- Reflection 기반 개선 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지