# TASK-017 Prompt 001

## 작업

TASK-017-build-layered-memory 초기 구현

## 수행 내용

- TASK-016 완료 처리 및 tasks/done/ 이동
- prompts/TASK-017/, logs/TASK-017/ 생성
- src/rag/layered_memory/ 디렉토리 구조 생성
- memory_classifier.py 구현 (Layer 분류, importance_score 계산, expiration 관리)
- layered_store.py 구현 (Layer별 저장/로드, 만료 필터링)
- layered_retriever.py 구현 (Layer별 Retrieval, Layered Context 생성)
- run_sample.py 구현 (5-Phase 통합 검증)
- 삼성전자/HBM Query 기준 Layered Memory 검증

## 환경

- openai (gpt-4o-mini Chat API)
- text-embedding-3-small (Embedding)
- MariaDB finance_study

## 샘플 Query

- 삼성전자 반도체 전망 분석
- HBM 시장 성장
