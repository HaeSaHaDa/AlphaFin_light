# TASK-008-build-embedding-pipeline.md

# TASK-008 Embedding 파이프라인 구축

## 상태

TODO

---

# 목표

생성된 Chunk 데이터를
Embedding Vector로 변환하는
초기 Embedding 파이프라인을 구축한다.

현재 TASK의 목표는
Chunk 데이터를 OpenAI Embedding API 기반으로
Vector화하고 저장 가능한 구조를 만드는 것이다.

현재 단계에서는
Retrieval 품질 최적화보다
안정적이고 재현 가능한 Embedding 생성에 집중한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Embedding 디렉토리 구조 생성
- OpenAI API 연동
- `.env` 기반 API KEY 로드
- Chunk 조회 구현
- Embedding 생성 구현
- Embedding 저장 구현
- Embedding Metadata 저장
- 샘플 Embedding 생성 검증
- 실행 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Retrieval 구현
- Vector Search 구현
- FAISS 도입
- ChromaDB 도입
- Hybrid Search
- Reranking
- LLM 분석
- Prompt 생성
- Semantic Search 평가
- Embedding 품질 평가
- Embedding 압축 최적화
- Batch 최적화
- 비동기 처리

현재 TASK는
Embedding 생성 파이프라인만 구현한다.

---

# 생성 대상 구조

```text
src/rag/embedding/
├─ __init__.py
├─ embedder.py
├─ storage.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/embeddings/
```

예상 저장 파일 예시:

```text
data/embeddings/news_chunk_embedding_001.json
```

---

# 수정 대상 DB 구조

현재 TASK에서 추가할 테이블:

```text
document_embeddings
```

---

# document_embeddings 역할

Chunk Embedding 저장 테이블.

역할:

- Chunk Vector 저장
- Embedding Metadata 저장
- Embedding 모델 추적
- Retrieval 기반 구조 준비

예상 필드:

```text
id
chunk_id
embedding_model
embedding_dimension
embedding_vector
created_at
```

---

# 환경 변수 사용

사용 환경 변수:

```text
OPENAI_API_KEY
```

`.env` 기준으로 로드한다.

---

# 구현 규칙

현재 TASK는 다음 규칙을 따른다.

- OpenAI 공식 SDK 사용
- 작은 함수 유지
- 단일 책임 유지
- 명확한 오류 메시지 출력
- Embedding 실패 시 로그 기록
- Metadata 추적 가능성 유지
- Chunk 원문 수정 금지
- 과도한 abstraction 금지
- 단순한 저장 구조 우선

---

# 사용 모델

현재 기본 Embedding 모델:

```text
text-embedding-3-small
```

현재 단계에서는
다른 모델 비교를 수행하지 않는다.

---

# 예상 기능

## embedder.py

역할:

- OpenAI Embedding 요청
- Vector 생성
- Embedding 응답 처리

예상 함수:

```text
generate_embedding(text)
generate_embeddings(chunks)
```

---

## storage.py

역할:

- Embedding JSON 저장
- DB 저장
- Metadata 저장

예상 함수:

```text
save_embedding_json(data)
save_embedding_to_db(data)
```

---

## run_sample.py

역할:

- Chunk 샘플 조회
- Embedding 생성
- JSON 저장 검증
- DB 저장 검증

샘플 기준:

```text
- 삼성전자 뉴스 Chunk
- 삼성전자 공시 Chunk
```

---

# 저장 흐름

현재 목표 흐름:

```text
Chunk 조회
→ OpenAI Embedding 요청
→ Vector 생성
→ JSON 저장
→ DB 저장
→ 로그 기록
```

---

# Embedding 저장 기준

현재 저장 대상:

```text
- chunk_id
- embedding_model
- embedding_dimension
- embedding_vector
```

---

# Metadata 추적 기준

현재 추적 대상:

```text
- source_id
- chunk_id
- document_type
- ticker
- embedding_model
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## API 검증

- OpenAI API 연결 성공 여부
- API KEY 로드 성공 여부
- Embedding 응답 정상 여부

---

## Embedding 검증

- Vector 생성 성공 여부
- Vector dimension 정상 여부
- 빈 Vector 여부 확인

---

## 저장 검증

- JSON 저장 성공 여부
- document_embeddings 저장 성공 여부
- chunk_id 연결 정상 여부 확인

---

## 구조 검증

- `src/rag/embedding/` 생성 여부
- `data/embeddings/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-008/
```

---

# 관련 Logs

```text
logs/TASK-008/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Embedding 파이프라인 구축 완료
- OpenAI API 연결 성공
- Embedding 생성 성공
- JSON 저장 성공
- document_embeddings 저장 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-009-build-vector-storage
- TASK-010-build-retrieval-pipeline
- TASK-011-build-rag-analysis-flow

단,
현재 TASK에서는
Retrieval 및 LLM 분석을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- Metadata 추적 가능성 유지
- Chunk 원문 추적 가능성 유지
- 단순한 Embedding 구조 우선
- Retrieval 준비 구조 유지
- AI 협업 가능한 구조 유지
- 과도한 최적화 금지