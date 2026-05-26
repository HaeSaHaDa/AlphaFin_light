# TASK-008 Prompt 001

## 작업

TASK-008-build-embedding-pipeline 초기 구현

## 수행 내용

- TASK-007 완료 처리 및 tasks/done/ 이동
- prompts/TASK-008/, logs/TASK-008/ 생성
- src/rag/embedding/ 디렉토리 구조 생성
- embedder.py 구현 (OpenAI Embedding API 연동)
- storage.py 구현 (JSON + DB 저장)
- run_sample.py 구현 (통합 검증 스크립트)
- document_embeddings 테이블 schema.sql 추가
- .env 기반 OPENAI_API_KEY 로드 구현
- 삼성전자 Chunk 기준 Embedding 저장 흐름 검증

## 환경

- openai 2.38.0
- text-embedding-3-small
- MariaDB finance_study
- pymysql

## 비고

- OpenAI API 쿼터 초과 (insufficient_quota) 발생
- 더미 벡터로 JSON + DB 저장 흐름 검증 완료
- API 쿼터 복구 후 실제 Embedding 생성 가능
