# TASK-012-verify-embedding-quality.md

# TASK-012 Embedding 품질 검증 및 재생성

## 상태

TODO

---

# 목표

현재 `document_embeddings`에 저장된 Embedding Vector가
실제 OpenAI Embedding 결과인지 검증하고,
필요 시 기존 Chunk 기준으로 Embedding을 재생성한다.

현재 TASK의 목표는
Retrieval score가 비정상적으로 낮게 나오는 원인을 확인하고,
의미 기반 검색 품질을 개선할 수 있는
Embedding 데이터 상태를 확보하는 것이다.

---

# 배경

TASK-009와 TASK-011 실행 결과에서
Retrieval Pipeline과 Financial Analysis Flow는 정상 동작했다.

다만 Retrieval 결과의 similarity score가 낮게 나타났다.

예상 원인:

```text
- document_embeddings에 더미 벡터가 남아 있음
- 실제 OpenAI Embedding이 일부만 저장됨
- embedding_dimension 불일치
- embedding_vector 저장/로드 과정 오류
- cosine similarity 계산 시 vector 파싱 문제
```

따라서 현재 TASK에서는
Embedding 생성 로직이 아니라
저장된 Embedding 품질과 재사용 가능성을 검증한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- `document_embeddings` 저장 데이터 점검
- embedding_vector 파싱 검증
- embedding_dimension 검증
- 더미 벡터 여부 확인
- OpenAI 실제 Embedding 재생성 기능 점검
- 기존 Chunk 기준 Embedding 재생성 스크립트 작성
- 재생성 후 similarity score 개선 여부 확인
- Retrieval 샘플 재검증
- 검증 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Retrieval 구조 전면 재설계
- FAISS 도입
- ChromaDB 도입
- Vector DB 도입
- Hybrid Search
- BM25
- Reranking
- LLM 분석 Prompt 수정
- Financial Analysis Flow 수정
- Chunking 로직 전면 수정
- 대량 Batch 최적화
- 비동기 처리
- Embedding 모델 비교 실험

현재 TASK는
Embedding 품질 검증과 재생성에만 집중한다.

---

# 생성 대상 구조

```text
src/rag/embedding/
├─ inspect_embeddings.py
└─ rebuild_embeddings.py
```

기존 파일은 유지한다.

```text
src/rag/embedding/
├─ embedder.py
├─ storage.py
└─ run_sample.py
```

---

# 사용 대상 테이블

현재 TASK에서 사용하는 테이블:

```text
document_chunks
document_embeddings
```

---

# 검증 대상

## document_embeddings

검증 항목:

```text
- 저장된 row 수
- chunk_id 연결 여부
- embedding_model 값
- embedding_dimension 값
- embedding_vector 길이
- embedding_vector 파싱 가능 여부
- 동일한 vector 반복 여부
- 0 또는 1 등 단순 더미값 여부
```

---

# 재생성 대상

재생성 기준:

```text
document_chunks에 존재하지만
document_embeddings에 정상 Embedding이 없거나
Embedding 품질 검증에 실패한 Chunk
```

현재 단계에서는
전체 재생성보다
샘플 또는 문제 데이터 중심 재생성을 우선한다.

---

# 구현 규칙

현재 TASK는 다음 규칙을 따른다.

- 기존 Chunk 원문 수정 금지
- 기존 document_chunks 삭제 금지
- 문제 있는 Embedding만 재생성 우선
- 필요 시 기존 document_embeddings는 update 또는 delete/insert 방식으로 정리
- OpenAI Embedding 모델은 기존과 동일하게 유지
- 과도한 최적화 금지
- 명확한 검증 로그 출력
- 결과를 logs/TASK-012/에 기록

---

# 사용 모델

현재 기본 Embedding 모델:

```text
text-embedding-3-small
```

현재 TASK에서는
모델 변경 또는 모델 비교를 수행하지 않는다.

---

# 예상 기능

## inspect_embeddings.py

역할:

- document_embeddings 상태 점검
- vector 파싱 검증
- dimension 검증
- 더미 vector 여부 추정
- 문제 row 출력

예상 함수:

```text
load_embeddings()
parse_embedding_vector(vector_text)
inspect_embedding_rows()
detect_invalid_embeddings()
```

---

## rebuild_embeddings.py

역할:

- 문제 Chunk 조회
- OpenAI Embedding 재생성
- document_embeddings 갱신
- 재생성 결과 출력

예상 함수:

```text
load_invalid_chunks()
rebuild_embedding_for_chunk(chunk)
save_rebuilt_embedding(chunk_id, embedding)
```

---

# 검증 흐름

현재 목표 흐름:

```text
document_embeddings 조회
→ vector 파싱 검증
→ dimension 검증
→ 문제 vector 식별
→ 필요 시 OpenAI Embedding 재생성
→ document_embeddings 갱신
→ Retrieval 샘플 재실행
→ score 변화 확인
```

---

# Retrieval 재검증 Query

샘플 Query:

```text
삼성전자 반도체 실적 전망
HBM 수요 증가
AI 메모리 시장 성장
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Embedding 저장 검증

- document_embeddings row 존재 여부
- chunk_id 연결 정상 여부
- embedding_model 정상 여부
- embedding_dimension 정상 여부
- embedding_vector 파싱 가능 여부

---

## Vector 품질 검증

- vector 길이 정상 여부
- 동일 vector 반복 여부
- 0 또는 1 등 단순 더미값 여부
- cosine similarity 계산 가능 여부

---

## 재생성 검증

- 문제 Chunk Embedding 재생성 성공 여부
- OpenAI API 호출 성공 여부
- document_embeddings 갱신 성공 여부

---

## Retrieval 재검증

- Top-K Retrieval 정상 동작 여부
- similarity score가 기존보다 정상 범위로 개선되었는지 확인
- 관련 Chunk 반환 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-012/
```

---

# 관련 Logs

```text
logs/TASK-012/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Embedding 저장 상태 검증 완료
- 잘못된 Embedding 여부 확인 완료
- 필요 시 Embedding 재생성 완료
- Retrieval 재검증 완료
- similarity score 문제 원인 기록 완료
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-013-build-analysis-evaluation
- TASK-014-build-character-layer
- TASK-015-build-memory-layer

단,
현재 TASK에서는
LLM 분석 구조를 확장하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 문제 원인 우선 확인
- 기존 데이터 삭제 최소화
- 재생성 가능 구조 유지
- Metadata 추적 가능성 유지
- Retrieval 품질 검증 우선
- 과도한 구조 변경 금지