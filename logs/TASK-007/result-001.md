# TASK-007 실행 결과 (result-001)

날짜: 2026-05-26
실행 대상: Cursor
Prompt: prompts/TASK-007/prompt-001.md

---

# 목적

문서 Chunking 파이프라인 구축 및 샘플 검증

---

# 사전 작업: TASK-006 완료 처리

```text
- tasks/todo/TASK-006-connect-collectors-to-mariadb.md → tasks/done/ 이동
- 상태: DONE
```

---

# 생성 파일

```text
src/preprocess/__init__.py
src/preprocess/chunking/__init__.py
src/preprocess/chunking/chunker.py    (고정 길이 Chunking)
src/preprocess/chunking/metadata.py   (Metadata 생성)
src/preprocess/chunking/run_sample.py (통합 검증)
```

---

# 수정 파일

```text
database/schema.sql     (document_chunks 테이블 추가)
src/common/db/store.py  (insert_document_chunks 함수 추가)
```

---

# 생성 디렉토리

```text
prompts/TASK-007/
logs/TASK-007/
data/chunks/news/
data/chunks/disclosures/
src/preprocess/
src/preprocess/chunking/
```

---

# 모듈 상세

## chunker.py

```text
split_text_into_chunks(text, chunk_size, overlap) → list[str]
create_document_chunks(document, document_type) → list[dict]

- 고정 길이 기반 분할 (기본 800자, overlap 100자)
- 문장 경계 유지 (마침표, 물음표, 느낌표, 줄바꿈)
- 문장 경계 불가 시 강제 분할 (_hard_split)
- 빈 텍스트 처리
```

## metadata.py

```text
build_news_metadata(article, chunk_index) → dict
build_disclosure_metadata(disclosure, chunk_index) → dict

포함 필드: ticker, source, published_at, chunk_index,
document_type, title/url 또는 report_name/receipt_no
```

---

# DB 변경

## document_chunks 테이블

```text
필드: id, document_type, source_table, source_id, ticker,
      chunk_index, chunk_text, chunk_length, metadata_json, created_at
PK: id
UNIQUE: (source_table, source_id, chunk_index)
INDEX: ticker, document_type
```

## store.py 추가 함수

```text
insert_document_chunks(chunks) → int
- INSERT IGNORE 사용 (중복 방지)
```

---

# 실행 검증

## schema.sql 실행

```text
구문 수: 6개 (기존 5 + document_chunks 1)
실행 결과: OK
```

## 뉴스 Chunk 생성

```text
뉴스 원문 조회: 5건
Chunk 생성 결과:
  - 기사 1: 2108자 → 3 chunks
  - 기사 2: 1862자 → 3 chunks
  - 기사 3: 1285자 → 2 chunks
  - 기사 4: 1949자 → 3 chunks
  - 기사 5: 1243자 → 2 chunks
  - 합계: 13 chunks
DB INSERT: 13건 성공
JSON 저장: data/chunks/news/samsung_news_chunks.json
```

## 공시 Chunk 생성

```text
공시 원문 조회: 10건 (DB 기준, 각 raw_json 포함)
Chunk 생성 결과: 10 chunks
DB INSERT: 10건 성공
JSON 저장: data/chunks/disclosures/samsung_disclosure_chunks.json
```

---

# Metadata 검증

```text
뉴스 Metadata 예시:
  ticker: "005930"
  source: "조선일보"
  published_at: "2026-05-25 23:40:19"
  chunk_index: 0
  document_type: "news_article"
  title: "[광화문·뷰] 물 들어올 때 나눠 마시는 나라"
  url: "https://n.news.naver.com/..."

공시 Metadata 예시:
  ticker: "005930"
  source: "opendart"
  document_type: "disclosure"
  report_name: "특수관계인과의내부거래"
```

---

# TASK-007 완료 조건 대비

| 조건 | 상태 |
|------|------|
| Chunking 파이프라인 구축 완료 | 완료 |
| 뉴스 Chunk 생성 성공 | 완료 (13 chunks) |
| 공시 Chunk 생성 성공 | 완료 (10 chunks) |
| Metadata 생성 성공 | 완료 |
| JSON 저장 성공 | 완료 (2 파일) |
| document_chunks DB 저장 성공 | 완료 (23건) |
| 결과 로그 작성 완료 | 완료 |
| TASK 범위 외 구현 없음 | 확인 |
