# TASK-015 Prompt 001

## 작업

TASK-015-build-memory-layer 초기 구현

## 수행 내용

- TASK-014 완료 처리 및 tasks/done/ 이동
- prompts/TASK-015/, logs/TASK-015/ 생성
- src/rag/memory/ 디렉토리 구조 생성
- memory_store.py 구현 (Analysis Memory 생성, 저장, 로드)
- event_memory.py 구현 (Market Event 추출, 저장, 로드)
- memory_retriever.py 구현 (키워드 기반 Memory 조회, Persona/Ticker 조회, Memory Context 생성)
- run_sample.py 구현 (3-Phase 통합 검증: 분석→저장→Memory 기반 재분석)
- 삼성전자 Query 기준 Memory 기반 분석 검증

## 환경

- openai (gpt-4o-mini Chat API)
- text-embedding-3-small (Embedding)
- MariaDB finance_study

## 샘플 Query

- 삼성전자 반도체 전망 분석
