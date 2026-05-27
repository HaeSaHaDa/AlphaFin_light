# TASK-024 Prompt-001

## 작업

TASK-024-build-dashboard-backend-api

## 목표

Financial AI Engine 내부 상태를 REST API로 노출하는 Dashboard Backend API 구축

## 수행 내용

- TASK-023 완료 처리 및 tasks/done/ 이동
- prompts/TASK-024/, logs/TASK-024/ 생성
- src/dashboard_api/ 생성
  - app.py (FastAPI, CORS, Route 등록, 요청 로깅)
  - routes/ (retrieval, reflection, memory, stock_chain, trace, evaluation)
  - services/ (JSON 저장 구조 기반 조회)
  - schemas/ (Pydantic Response)
- 기존 Unified Engine / Evaluation Suite / Trace JSON 재사용
- 샘플 API 실행 검증 (TestClient)

## 환경

- Python 3.x
- fastapi, uvicorn[standard]
- data/unified_engine/, data/evaluation_suite/, data/layered_memory/, data/stock_chain/

## 샘플 API

```text
GET /api/retrieval/latest
GET /api/reflection/latest
GET /api/memory/latest
GET /api/stock-chain/latest
GET /api/trace/latest
GET /api/evaluation/latest
```

## 실행

```text
uvicorn src.dashboard_api.app:app --host 0.0.0.0 --port 8000
```

Swagger: http://localhost:8000/docs

## 제외 범위

- WebSocket / Realtime Push 금지
- Authentication / Multi-user Session 금지
- GraphQL / Kafka / Kubernetes / Cloud Deployment 금지
- 과도한 abstraction 금지
