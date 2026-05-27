# TASK-024-build-dashboard-backend-api.md

# TASK-024 Dashboard Backend API 구축

## 상태

DONE

---

# 완료 결과

- FastAPI Dashboard API 구현 및 TestClient 검증 완료
- 전 샘플 엔드포인트 200 OK, overall_score 0.8865

---

# 관련 문서

```text
prompts/TASK-024/prompt-001.md
logs/TASK-024/result-001.md
```

---

# 목표

Financial AI Engine 내부 상태를
외부 Dashboard에서 조회 및 시각화할 수 있도록
Dashboard Backend API Layer를 구축한다.

현재 TASK의 목표는
단순 JSON 저장 구조를 넘어,
Retrieval, Reflection, Memory, Stock Chain,
Trace 정보를 API 기반으로 조회 가능한 구조를 만드는 것이다.

현재 단계에서는
복잡한 실시간 streaming보다
명시적이고 추적 가능한 REST API 구조에 집중한다.

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
→ Unified Engine Runner
→ Engine Evaluation Suite
```

현재 시스템은:

```text
JSON/Trace 기반 저장
```

까지 가능하다.

하지만 현재 구조는:

```text
엔진 내부 상태를 외부 UI에서 조회
```

하기 어렵다.

현재 TASK에서는
Dashboard UI와 연결 가능한
Backend API Layer를 구축한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Dashboard API 디렉토리 구조 생성
- Retrieval API 구현
- Reflection API 구현
- Memory API 구현
- Temporal Memory API 구현
- Stock Chain API 구현
- Trace API 구현
- Engine Result API 구현
- Evaluation API 구현
- API Response Schema 구현
- 샘플 API 실행 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- WebSocket Streaming
- Realtime Push
- Authentication/Authorization
- Multi-user Session
- Distributed API Gateway
- GraphQL
- Kafka/Event Streaming
- Kubernetes
- Cloud Deployment
- 실시간 거래 API 연동
- 외부 Broker API 연동
- Autonomous Trading API

현재 TASK는
단일 로컬 Dashboard API만 구현한다.

---

# 생성 대상 구조

```text
src/dashboard_api/
├─ __init__.py
├─ app.py
├─ routes/
│  ├─ retrieval.py
│  ├─ reflection.py
│  ├─ memory.py
│  ├─ stock_chain.py
│  ├─ trace.py
│  └─ evaluation.py
├─ services/
│  ├─ retrieval_service.py
│  ├─ reflection_service.py
│  ├─ memory_service.py
│  ├─ stock_chain_service.py
│  ├─ trace_service.py
│  └─ evaluation_service.py
└─ schemas/
   ├─ retrieval_schema.py
   ├─ reflection_schema.py
   ├─ memory_schema.py
   ├─ stock_chain_schema.py
   └─ evaluation_schema.py
```

---

# 예상 API 구조

## Retrieval API

```text
GET /api/retrieval/latest
GET /api/retrieval/{trace_id}
```

역할:

- retrieval 결과 조회
- similarity score 조회
- chunk 조회

---

## Reflection API

```text
GET /api/reflection/latest
GET /api/reflection/{trace_id}
```

역할:

- reflection 결과 조회
- missing_risks 조회
- overconfidence 조회

---

## Memory API

```text
GET /api/memory/latest
GET /api/memory/{layer}
```

역할:

- layered memory 조회
- importance 조회
- temporal 상태 조회

---

## Stock Chain API

```text
GET /api/stock-chain/latest
GET /api/stock-chain/{ticker}
```

역할:

- stock chain 조회
- propagation 조회
- relation 조회

---

## Trace API

```text
GET /api/trace/latest
GET /api/trace/{trace_id}
```

역할:

- full reasoning trace 조회
- pipeline 단계 조회

---

## Evaluation API

```text
GET /api/evaluation/latest
GET /api/evaluation/{trace_id}
```

역할:

- engine score 조회
- hallucination risk 조회
- consistency score 조회

---

# API 역할

현재 Dashboard API 역할:

- Engine 내부 상태 노출
- Retrieval 결과 시각화 지원
- Reflection 결과 시각화 지원
- Memory lifecycle 시각화 지원
- Stock Chain 시각화 지원
- Full Trace 시각화 지원

---

# 예상 API Response 구조

예상 반환 형태:

```json
{
  "trace_id": "...",
  "query": "...",
  "retrieval_score": 0.82,
  "reasoning_score": 0.79,
  "reflection_score": 0.76,
  "overall_score": 0.80
}
```

---

# Trace API 목표

예상 Trace 흐름:

```text
retrieval
→ context assembly
→ character analysis
→ reflection
→ memory update
→ temporal tracking
→ stock chain propagation
→ final result
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Unified Engine 재사용
- 기존 Evaluation Suite 재사용
- 기존 Trace 재사용
- 기존 JSON 저장 구조 재사용
- API traceability 유지
- API schema 명시성 유지
- 작은 함수 유지
- 과도한 abstraction 금지
- 실시간 streaming 금지

---

# 예상 기능

## app.py

역할:

- Dashboard API 서버 실행
- Route 등록

예상 기능:

```text
create_app()
register_routes()
```

---

## retrieval.py

역할:

- Retrieval API Route 제공

예상 기능:

```text
get_latest_retrieval()
get_retrieval_by_trace(trace_id)
```

---

## reflection.py

역할:

- Reflection API Route 제공

예상 기능:

```text
get_latest_reflection()
get_reflection_by_trace(trace_id)
```

---

## memory.py

역할:

- Memory API Route 제공

예상 기능:

```text
get_latest_memory()
get_memory_by_layer(layer)
```

---

## stock_chain.py

역할:

- Stock Chain API Route 제공

예상 기능:

```text
get_latest_stock_chain()
get_stock_chain_by_ticker(ticker)
```

---

## trace.py

역할:

- Full Trace API Route 제공

예상 기능:

```text
get_latest_trace()
get_trace_by_id(trace_id)
```

---

## evaluation.py

역할:

- Evaluation API Route 제공

예상 기능:

```text
get_latest_evaluation()
get_evaluation_by_trace(trace_id)
```

---

# Dashboard 활용 목표

현재 활용 목표:

```text
- Engine 내부 상태 시각화
- Retrieval debugging
- Reflection debugging
- Memory lifecycle 확인
- Stock Chain propagation 확인
- Full reasoning trace 확인
```

현재 단계에서는
실시간 투자 UI를 구현하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## API 검증

- API 서버 실행 성공 여부
- Route 등록 성공 여부
- JSON Response 정상 반환 여부

---

## Retrieval API 검증

- Retrieval 결과 조회 여부
- similarity score 조회 여부

---

## Reflection API 검증

- Reflection 결과 조회 여부
- missing_risks 조회 여부

---

## Memory API 검증

- Layered Memory 조회 여부
- importance 조회 여부

---

## Stock Chain API 검증

- propagation 조회 여부
- relation 조회 여부

---

## Trace API 검증

- Full Trace 조회 여부
- Pipeline 단계 조회 여부

---

## Evaluation API 검증

- overall_score 조회 여부
- hallucination risk 조회 여부

---

## 구조 검증

- `src/dashboard_api/` 생성 여부
- API route 구조 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-024/
```

---

# 관련 Logs

```text
logs/TASK-024/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Dashboard Backend API 구축 완료
- API Route 등록 성공
- JSON Response 정상 반환 성공
- Trace 조회 성공
- Evaluation 조회 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-025-build-dashboard-ui
- TASK-026-build-retrieval-analysis-viewer
- TASK-027-build-event-graph-visualization

단,
현재 TASK에서는
실시간 투자 플랫폼을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- End-to-End traceability 유지
- Retrieval 기반 분석 유지
- Memory lifecycle 유지
- Reflection 기반 개선 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지