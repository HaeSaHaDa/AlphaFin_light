# TASK-007-build-chunking-pipeline.md

# TASK-007 문서 Chunking 파이프라인 구축

## 상태

TODO

---

# 목표

수집된 뉴스 및 공시 데이터를
검색 가능한 문서 단위(Chunk)로 변환하는
초기 Chunking 파이프라인을 구축한다.

현재 TASK의 목표는
긴 문서를 작은 단위로 분할하고
Metadata와 함께 저장 가능한 구조를 만드는 것이다.

현재 단계에서는
복잡한 NLP 처리보다
안정적이고 재현 가능한 Chunk 생성에 집중한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Chunking 디렉토리 구조 생성
- 뉴스 데이터 Chunking 구현
- 공시 데이터 Chunking 구현
- 기본 Metadata 생성
- Chunk JSON 저장
- Chunk DB 저장 구조 구현
- Chunk 로그 기록
- 샘플 Chunk 생성 검증

---

# 현재 제외 범위

현재 TASK에서 제외:

- Embedding 생성
- OpenAI API 호출
- Vector DB 연결
- Retrieval 구현
- Reranking
- Semantic Chunking
- LLM 기반 요약
- 문서 품질 평가
- 문서 중복 제거 최적화
- Chunk 압축 최적화
- Hybrid Search
- Prompt 생성

현재 TASK는
기본 Chunk 생성 파이프라인만 구현한다.

---

# 생성 대상 구조

```text
src/preprocess/chunking/
├─ __init__.py
├─ chunker.py
├─ metadata.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/chunks/
├─ news/
└─ disclosures/
```

예상 저장 파일 예시:

```text
data/chunks/news/samsung_news_chunk_001.json
data/chunks/disclosures/disclosure_chunk_001.json
```

---

# 수정 대상 DB 구조

현재 TASK에서 사용하는 테이블:

```text
news_articles
dart_disclosures
```

추가 예정 테이블:

```text
document_chunks
```

---

# document_chunks 역할

Chunk 데이터를 저장하는 테이블.

역할:

- Chunk 본문 저장
- Chunk Metadata 저장
- 원본 문서 추적
- Retrieval 기반 데이터 준비

예상 필드:

```text
id
document_type
source_table
source_id
ticker
chunk_index
chunk_text
chunk_length
metadata_json
created_at
```

---

# 구현 규칙

현재 TASK는 다음 규칙을 따른다.

- 작은 함수 유지
- 단순한 Chunking 우선
- 고정 길이 기반 Chunking 우선
- 과도한 NLP 사용 금지
- Metadata 추적 가능성 유지
- 원본 문서 추적 가능성 유지
- 명확한 오류 메시지 출력
- Raw 데이터 수정 금지
- Chunk 생성 실패 시 로그 기록

---

# Chunking 기준

현재 기본 Chunk 기준:

```text
- 문자 수 기준 분할
- 약 500 ~ 1000자 기준
- overlap 최소화
- 문장 경계 최대한 유지
```

현재 단계에서는
복잡한 semantic chunking을 사용하지 않는다.

---

# Metadata 생성 기준

현재 생성할 Metadata 예시:

```json
{
  "ticker": "005930",
  "source": "news",
  "published_at": "2024-01-15",
  "chunk_index": 0,
  "document_type": "news_article"
}
```

---

# 예상 기능

## chunker.py

역할:

- 긴 문서 분할
- Chunk 리스트 생성
- Chunk 길이 계산

예상 함수:

```text
split_text_into_chunks(text, chunk_size, overlap)
create_document_chunks(document)
```

---

## metadata.py

역할:

- Metadata 생성
- Chunk Metadata 조합

예상 함수:

```text
build_news_metadata(article)
build_disclosure_metadata(disclosure)
```

---

## run_sample.py

역할:

- 뉴스 Chunking 샘플 실행
- 공시 Chunking 샘플 실행
- Chunk 저장 검증
- DB 저장 검증

샘플 기준:

```text
- 삼성전자 뉴스 데이터
- 삼성전자 공시 데이터
```

---

# 저장 흐름

현재 목표 흐름:

```text
MariaDB 원문 조회
→ Chunk 생성
→ Metadata 생성
→ JSON 저장
→ DB 저장
→ 로그 기록
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Chunk 생성 검증

- 뉴스 Chunk 생성 성공 여부
- 공시 Chunk 생성 성공 여부
- 빈 Chunk 생성 여부 확인
- Chunk 길이 정상 여부 확인

---

## Metadata 검증

- ticker 존재 여부
- source 존재 여부
- chunk_index 존재 여부
- document_type 존재 여부

---

## 저장 검증

- JSON 저장 성공 여부
- document_chunks 저장 성공 여부
- source_id 연결 정상 여부 확인

---

## 구조 검증

- `src/preprocess/chunking/` 생성 여부
- `data/chunks/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-007/
```

---

# 관련 Logs

```text
logs/TASK-007/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Chunking 파이프라인 구축 완료
- 뉴스 Chunk 생성 성공
- 공시 Chunk 생성 성공
- Metadata 생성 성공
- JSON 저장 성공
- document_chunks 저장 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-008-build-embedding-pipeline
- TASK-009-build-vector-storage
- TASK-010-build-retrieval-pipeline

단,
현재 TASK에서는
Embedding 및 Retrieval을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- 단순한 Chunking 우선
- Metadata 추적 가능성 유지
- 원본 문서 추적 가능성 유지
- Retrieval 준비 구조 유지
- AI 협업 가능한 구조 유지
- 과도한 NLP 도입 금지