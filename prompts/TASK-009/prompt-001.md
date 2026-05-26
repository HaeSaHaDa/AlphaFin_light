# TASK-009 Prompt 001

## 작업

TASK-009-build-retrieval-pipeline 초기 구현

## 수행 내용

- TASK-008 완료 처리 및 tasks/done/ 이동
- prompts/TASK-009/, logs/TASK-009/ 생성
- src/rag/retrieval/ 디렉토리 구조 생성
- similarity.py 구현 (Cosine Similarity 계산, Top-K 정렬)
- retriever.py 구현 (Query Embedding, DB 조회, Metadata 필터링, Retrieval)
- run_sample.py 구현 (5개 검증 단계)
- 삼성전자 Chunk 기준 Retrieval 검증

## 환경

- openai 2.38.0
- text-embedding-3-small
- MariaDB finance_study
- pymysql

## 샘플 Query

- 삼성전자 반도체 실적 전망
- HBM 수요 증가
- AI 반도체 시장 성장
