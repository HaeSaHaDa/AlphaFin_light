# TASK-006 실행 결과 (result-001)

날짜: 2026-05-26
실행 대상: Cursor
Prompt: prompts/TASK-006/prompt-001.md

---

# 목적

Collector와 MariaDB 연결 구조 구축 및 데이터 저장 검증

---

# 사전 작업: TASK-005 완료 처리

```text
- tasks/todo/TASK-005-design-mariadb-schema.md → tasks/done/ 이동
- 상태: DONE
```

---

# 생성 파일

```text
src/common/__init__.py
src/common/db/__init__.py
src/common/db/connection.py    (MariaDB 연결)
src/common/db/init_schema.py   (schema.sql 실행)
src/common/db/store.py         (INSERT 함수 모음)
src/common/db/run_db_sample.py (통합 검증 스크립트)
```

---

# 생성 디렉토리

```text
prompts/TASK-006/
logs/TASK-006/
src/common/
src/common/db/
```

---

# 모듈 상세

## connection.py

```text
get_connection() → pymysql.Connection
- .env 기반 DB 설정 로드
- utf8mb4, DictCursor, autocommit=False
```

## init_schema.py

```text
initialize_database() → bool
- database/schema.sql 파일 읽기
- 주석 제거 후 구문 분리
- CREATE TABLE 실행
```

## store.py

```text
insert_collection_log() → int | None
update_collection_log() → bool
upsert_company() → bool
insert_stock_prices() → int
insert_dart_disclosures() → int
insert_news_articles() → int
```

---

# DB 연결 검증

```text
- .env 로드: OK (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
- MariaDB 연결: OK (localhost:3306, finance_study)
- schema.sql 실행: OK (5개 CREATE TABLE)
```

---

# 데이터 저장 검증

## 1차 실행 결과

| 테이블 | 대상 건수 | INSERT 건수 | 결과 |
|--------|----------|------------|------|
| companies | 1 | 1 | OK (UPSERT) |
| stock_prices | 22 | 22 | OK |
| dart_disclosures | 15 | 15 | OK |
| news_articles | 5 | 5 | OK |
| collection_logs | 3 | 3 | OK |

## 중복 실행 검증 (2차)

| 테이블 | 대상 건수 | INSERT 건수 | 결과 |
|--------|----------|------------|------|
| stock_prices | 22 | 0 | OK (UNIQUE 방지) |
| dart_disclosures | 15 | 0 | OK (UNIQUE 방지) |
| news_articles | 5 | 0 | OK (UNIQUE 방지) |

---

# 이슈 및 수정

## rcept_no 필드명 매핑 오류

```text
원인: OpenDART JSON 필드명이 'rcept_no'인데 'rcpt_no'로 매핑
증상: dart_disclosures.receipt_no가 모두 NULL → UNIQUE 무효화 → 중복 삽입
수정: store.py에서 d.get("rcpt_no") → d.get("rcept_no") 변경
결과: 정상 중복 방지 동작 확인
```

## init_schema.py SQL 파싱 오류

```text
원인: SQL 주석(--) 포함 구문이 통째로 필터링됨
증상: 0개 구문 실행 → 테이블 미생성
수정: 주석 라인을 먼저 제거한 후 구문 분리
결과: 5개 CREATE TABLE 정상 실행
```

---

# 최종 테이블 행 수

```text
companies        : 1
stock_prices     : 22
dart_disclosures : 15
news_articles    : 5
collection_logs  : 10+ (검증 반복 포함)
```

---

# TASK-006 완료 조건 대비

| 조건 | 상태 |
|------|------|
| MariaDB 연결 성공 | 완료 |
| schema.sql 실행 성공 | 완료 |
| pykrx 데이터 저장 성공 | 완료 (22건) |
| OpenDART 데이터 저장 성공 | 완료 (15건) |
| 뉴스 데이터 저장 성공 | 완료 (5건) |
| collection_logs 저장 성공 | 완료 |
| 중복 방지 동작 확인 | 완료 |
| 결과 로그 작성 완료 | 완료 |
| TASK 범위 외 구현 없음 | 확인 |
