# TASK-016 Prompt 001

## 작업

TASK-016-build-market-event-graph 초기 구현

## 수행 내용

- TASK-015 완료 처리 및 tasks/done/ 이동
- prompts/TASK-016/, logs/TASK-016/ 생성
- src/rag/event_graph/ 디렉토리 구조 생성
- event_extractor.py 구현 (Event Node 추출, Market Entity 분류)
- relation_builder.py 구현 (규칙 기반 Relation 생성, Impact Relation 추출)
- graph_store.py 구현 (Graph 저장/로드/조회, Graph Context 생성)
- run_sample.py 구현 (6-Phase 통합 검증)
- 삼성전자 Query 기준 Event Graph 생성 검증

## 환경

- openai (gpt-4o-mini Chat API)
- text-embedding-3-small (Embedding)
- MariaDB finance_study

## 샘플 Query

- 삼성전자 반도체 전망 분석
