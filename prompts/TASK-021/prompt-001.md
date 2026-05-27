# TASK-021 Prompt-001

## 작업

TASK-021-build-stock-chain-layer

## 목표

기업·산업·제품·공급망 간 연결 관계를 추적하는 Stock Chain Layer 구축

## 수행 내용

- TASK-020 완료 처리 및 tasks/done/ 이동
- prompts/TASK-021/, logs/TASK-021/ 생성
- src/rag/stock_chain/ 생성
  - entity_extractor.py: Entity 추출·정규화, Event Graph 연동
  - chain_builder.py: 공급망·산업 Chain 생성
  - propagation_engine.py: propagation 경로·영향 전파 계산
  - chain_store.py: 저장/조회, Context 생성
  - run_sample.py: 샘플 검증
- Event Graph, Temporal Memory, Layered Memory 연동
- NVIDIA/HBM/AI 서버 샘플 Stock Chain 검증

## 환경

- Python 3.x
- data/stock_chain/ 저장
- 기존 event_graph, temporal_memory, layered_memory 재사용

## 샘플 Query

```text
NVIDIA GPU 수요 증가
HBM 공급 부족
AI 서버 투자 확대
```

## 제외 범위

- Neo4j/Knowledge Graph DB 금지
- GNN 금지
- Causal AI 금지
- 실거래 전략 생성 금지
- 과도한 abstraction 금지
