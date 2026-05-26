# TASK-007 Prompt-001

날짜: 2026-05-26
실행 대상: Cursor

---

# 목적

```text
문서 Chunking 파이프라인 초기 구축
```

---

# 프롬프트

```text
AGENTS.md와 TASK-007 기준으로 작업해라.

현재 작업:

1. TASK-006-connect-collectors-to-mariadb 완료 처리
2. TASK-007-build-chunking-pipeline 초기 구현

수행 내용:

- TASK-006 완료 조건 검토 및 tasks/done/ 이동
- prompts/TASK-007/, logs/TASK-007/ 생성
- src/preprocess/chunking/ 생성
- chunker.py, metadata.py, run_sample.py 생성
- document_chunks 테이블 추가
- 뉴스/공시 데이터 Chunking 구현
- Metadata 생성 구현
- JSON + DB 저장 검증

Chunk 기준: 약 800자, overlap 100자, 문장 경계 유지
Metadata: ticker, source, published_at, chunk_index, document_type

제외 범위: Embedding, Vector DB, Retrieval,
Semantic Chunking, LLM 요약, OpenAI API
```

---

# 결과

```text
- TASK-006 → tasks/done/ 이동 완료
- src/preprocess/chunking/ 생성 완료
  - chunker.py (고정 길이 + 문장 경계 Chunking)
  - metadata.py (뉴스/공시 Metadata 생성)
  - run_sample.py (통합 검증)
- document_chunks 테이블 schema.sql 추가 + DB 생성 완료
- 뉴스 13 chunks, 공시 10 chunks 생성 성공
- JSON 저장 + DB 저장 모두 성공
- 중복 방지 UNIQUE KEY 동작 확인
```
