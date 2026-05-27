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
