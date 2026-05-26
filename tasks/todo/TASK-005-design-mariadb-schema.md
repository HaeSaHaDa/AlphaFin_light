# TASK-005-design-mariadb-schema.md

# TASK-005 MariaDB 저장 스키마 설계

## 상태

TODO

---

# 목표

AlphaFin LTE에서 수집한 Raw 데이터를 저장하기 위한
MariaDB 초기 스키마를 설계한다.

현재 TASK의 목표는
주가, 공시, 뉴스 데이터를 관계형 DB에 저장할 수 있는
최소 테이블 구조를 정의하는 것이다.

현재 단계에서는
복잡한 분석 테이블보다
수집 데이터의 안정적 저장 구조에 집중한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- MariaDB 초기 스키마 설계
- 기업 기본 정보 테이블 설계
- 주가 데이터 테이블 설계
- 공시 데이터 테이블 설계
- 뉴스 데이터 테이블 설계
- 수집 로그 테이블 설계
- SQL DDL 파일 작성
- 스키마 설명 문서 작성

---

# 현재 제외 범위

현재 TASK에서 제외:

- 실제 데이터 마이그레이션
- Collector 코드 수정
- DB 저장 로직 구현
- ORM 도입
- RAG 테이블 설계
- Embedding 테이블 설계
- Vector DB 연동
- LLM 분석 결과 테이블 설계
- 백테스트 테이블 설계
- 복잡한 인덱스 최적화
- PostgreSQL / Supabase 전환 작업

현재 TASK는
MariaDB 초기 저장 스키마 설계만 수행한다.

---

# 생성 대상 구조

```text
database/
├─ schema.sql
└─ README.md
```

---

# 설계 대상 테이블

현재 TASK에서 설계할 테이블:

```text
companies
stock_prices
dart_disclosures
news_articles
collection_logs
```

---

# 테이블 역할

## companies

기업 기본 정보 저장 테이블.

역할:

- 종목코드 관리
- 기업명 관리
- OpenDART corp_code 관리
- 시장 구분 관리

예상 필드:

```text
id
ticker
corp_code
company_name
market
created_at
updated_at
```

---

## stock_prices

일봉 주가 데이터 저장 테이블.

역할:

- pykrx 기반 OHLCV 데이터 저장
- 날짜별 주가 데이터 관리

예상 필드:

```text
id
ticker
trade_date
open_price
high_price
low_price
close_price
volume
change_rate
created_at
```

---

## dart_disclosures

OpenDART 공시 데이터 저장 테이블.

역할:

- 공시 목록 저장
- 공시 메타데이터 저장
- 원본 JSON 경로 또는 원본 응답 저장

예상 필드:

```text
id
corp_code
ticker
report_name
receipt_no
receipt_date
disclosure_type
raw_json
raw_file_path
created_at
```

---

## news_articles

뉴스 데이터 저장 테이블.

역할:

- 뉴스 제목 저장
- 뉴스 본문 또는 요약 저장
- 언론사 / URL / 날짜 저장
- 종목 관련 Metadata 저장

예상 필드:

```text
id
ticker
keyword
title
content
source
url
published_at
raw_json
raw_file_path
created_at
```

---

## collection_logs

수집 실행 로그 저장 테이블.

역할:

- Collector 실행 결과 기록
- 성공 / 실패 상태 기록
- 오류 메시지 기록
- 실행 시간 기록

예상 필드:

```text
id
collector_name
target
status
started_at
finished_at
row_count
error_message
created_at
```

---

# MariaDB 설계 원칙

현재 TASK는 다음 원칙을 따른다.

- 단순한 테이블 구조 우선
- 명시적 SQL 사용
- ORM 도입 금지
- 불필요한 추상화 금지
- Raw 데이터 추적 가능성 유지
- 원본 파일 경로 보존 가능 구조 유지
- 향후 PostgreSQL/Supabase 전환 가능성을 고려해 과도한 DB 종속 기능 사용 금지

---

# 타입 설계 기준

현재 기본 타입 기준:

```text
문자열: VARCHAR
긴 본문: TEXT 또는 LONGTEXT
날짜: DATE
날짜시간: DATETIME
정수: BIGINT 또는 INT
소수: DECIMAL
원본 JSON: LONGTEXT
PK: BIGINT AUTO_INCREMENT
```

---

# 제약 조건 기준

현재 제약 조건 기준:

- PK는 `id` 사용
- `ticker`는 문자열로 저장
- `corp_code`는 문자열로 저장
- 날짜 기반 중복 방지 필요
- URL 중복 방지 필요
- 초기에는 FK를 과도하게 사용하지 않는다
- 삭제보다 보존을 우선한다

---

# 인덱스 기준

초기 권장 인덱스:

```text
companies.ticker
companies.corp_code
stock_prices.ticker + trade_date
dart_disclosures.corp_code + receipt_date
news_articles.ticker + published_at
news_articles.url
collection_logs.collector_name + started_at
```

---

# 생성 파일 상세

## database/schema.sql

역할:

- MariaDB에서 실행 가능한 초기 DDL
- 테이블 생성 SQL 포함
- 기본 인덱스 포함
- 필요한 주석 포함

---

## database/README.md

역할:

- 스키마 개요 설명
- 테이블 역할 설명
- 실행 방법 설명
- 현재 제외 범위 설명

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## SQL 검증

- MariaDB 문법 기준으로 작성되었는지 확인
- `CREATE TABLE` 실행 가능 여부 확인
- 중복 실행 시 오류 방지 여부 검토
- 기본 인덱스 생성 여부 확인

---

## 구조 검증

- `database/schema.sql` 생성 여부
- `database/README.md` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

## 설계 검증

- 주가 데이터 저장 가능 여부
- 공시 데이터 저장 가능 여부
- 뉴스 데이터 저장 가능 여부
- 수집 로그 저장 가능 여부
- Raw 파일 경로 추적 가능 여부

---

# 관련 Prompt

```text
prompts/TASK-005/
```

---

# 관련 Logs

```text
logs/TASK-005/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- MariaDB 초기 스키마 설계 완료
- `database/schema.sql` 생성 완료
- `database/README.md` 생성 완료
- 테이블 역할 문서화 완료
- SQL 실행 가능성 검토 완료
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-006-connect-collectors-to-mariadb
- TASK-007-build-chunking-pipeline
- TASK-008-design-document-metadata-schema

단,
현재 TASK에서는
Collector DB 저장 로직을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- 명시적 SQL 우선
- Raw Data 추적 가능성 유지
- 단순한 관계형 구조 우선
- AI 협업 가능한 구조 유지
- 향후 확장 가능성은 열어두되 과설계하지 않음