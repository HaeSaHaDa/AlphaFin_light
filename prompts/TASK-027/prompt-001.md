# TASK-027 Prompt-001

## 작업

TASK-027-build-event-graph-visualization

## 목표

Stock Chain 기반 interactive Event Graph Visualization 구축 (React Flow)

## 수행 내용

- event-graph/ 컴포넌트 7종 (EventGraph, GraphNode, GraphEdge, Legend, Toolbar, NodeDetail, Propagation)
- `/event-graph` 페이지 · Stock Chain + Trace API 연동
- 필터 (entity type, min impact, search, highlight)
- propagation flow · temporal relations 패널

## 기술

- @xyflow/react
- GET /api/stock-chain/latest, GET /api/trace/latest

## 접속

http://localhost:3000/event-graph

## 샘플

- NVIDIA → HBM → 삼성전자 propagation
- trace_id: 20260527_123745

## 제외

- Neo4j · realtime streaming · GPU rendering 금지

---

## 추가 작업 — Dashboard Query Flow 수정

TASK-027 연장선으로 Dashboard Query Flow를 `latest` 기반에서 `query → trace_id` 기반으로 수정.

### 수행 방향

1. 백엔드: `POST /api/engine/run` + memory/stock_chain `/{trace_id}` GET 엔드포인트 추가
2. 프론트: `runEngine()` API 함수 + `runAndLoad()` 훅 + QueryInputPanel Run Engine 버튼

### 핵심 제약

- 기존 `/latest` API는 그대로 유지 (Latest Trace 버튼용)
- multi-user, WebSocket, streaming 금지
- 과도한 추상화 금지
