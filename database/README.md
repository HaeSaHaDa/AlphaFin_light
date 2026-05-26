# database/

# AlphaFin LTE MariaDB 스키마

---

# 개요

AlphaFin LTE 프로젝트에서 수집한
Raw 데이터를 저장하기 위한 MariaDB 초기 스키마이다.

현재 목표:

- 주가, 공시, 뉴스 데이터의 관계형 저장
- 수집 로그 추적
- Raw 파일 경로 보존
- 단순한 구조 유지

---

# 대상 DB

```text
MariaDB 10.6+
인코딩: utf8mb4 / utf8mb4_unicode_ci
엔진: InnoDB
```

---

# 파일 구조

```text
database/
├─ schema.sql   (테이블 DDL)
└─ README.md    (이 문서)
```

---

# 테이블 목록

| 테이블 | 역할 |
|--------|------|
| companies | 기업 기본 정보 (종목코드, 기업명, 시장 구분) |
| stock_prices | 일봉 주가 OHLCV 데이터 |
| dart_disclosures | OpenDART 공시 목록 |
| news_articles | 뉴스 기사 데이터 |
| collection_logs | Collector 실행 로그 |

---

# 테이블 상세

## companies

기업 기본 정보를 관리한다.

주요 필드:

- `ticker` - 종목코드 (예: 005930), UNIQUE
- `corp_code` - OpenDART 기업코드 (예: 00126380)
- `company_name` - 기업명
- `market` - 시장 구분 (KOSPI, KOSDAQ)

---

## stock_prices

pykrx 기반 일봉 주가 데이터를 저장한다.

주요 필드:

- `ticker` - 종목코드
- `trade_date` - 거래일
- `open_price`, `high_price`, `low_price`, `close_price` - OHLCV
- `volume` - 거래량
- `change_rate` - 등락률

중복 방지: `(ticker, trade_date)` UNIQUE

---

## dart_disclosures

OpenDART 공시 목록을 저장한다.

주요 필드:

- `corp_code` - OpenDART 기업코드
- `report_name` - 공시 보고서명
- `receipt_no` - 접수번호, UNIQUE
- `receipt_date` - 접수일
- `raw_json` - 원본 API 응답 JSON
- `raw_file_path` - Raw 파일 저장 경로

---

## news_articles

뉴스 기사 데이터를 저장한다.

주요 필드:

- `ticker` - 관련 종목코드 (nullable)
- `keyword` - 검색 키워드
- `title` - 기사 제목
- `content` - 기사 본문
- `source` - 언론사
- `url` - 기사 URL, UNIQUE
- `published_at` - 발행 시각

---

## collection_logs

Collector 실행 이력을 기록한다.

주요 필드:

- `collector_name` - 수집기 이름 (pykrx, opendart, news)
- `target` - 수집 대상
- `status` - 실행 상태 (started, success, failed)
- `row_count` - 수집 건수
- `error_message` - 오류 메시지

---

# 인덱스

| 테이블 | 인덱스 | 대상 |
|--------|--------|------|
| companies | uq_companies_ticker | ticker (UNIQUE) |
| companies | idx_companies_corp_code | corp_code |
| stock_prices | uq_stock_prices_ticker_date | ticker + trade_date (UNIQUE) |
| stock_prices | idx_stock_prices_trade_date | trade_date |
| dart_disclosures | uq_dart_receipt_no | receipt_no (UNIQUE) |
| dart_disclosures | idx_dart_corp_date | corp_code + receipt_date |
| dart_disclosures | idx_dart_ticker | ticker |
| news_articles | uq_news_url | url (UNIQUE, prefix 255) |
| news_articles | idx_news_ticker_published | ticker + published_at |
| news_articles | idx_news_keyword | keyword |
| collection_logs | idx_logs_collector_started | collector_name + started_at |
| collection_logs | idx_logs_status | status |

---

# 실행 방법

MariaDB 클라이언트에서 다음과 같이 실행한다.

```bash
mysql -u <사용자> -p <데이터베이스명> < database/schema.sql
```

또는 MariaDB 쉘 내에서:

```sql
SOURCE database/schema.sql;
```

`IF NOT EXISTS`를 사용하므로 중복 실행해도 오류가 발생하지 않는다.

---

# 현재 제외 범위

- ORM 도입
- Migration 도구
- RAG / Embedding 테이블
- Vector DB 테이블
- 백테스트 결과 테이블
- LLM 분석 결과 테이블
- 복잡한 인덱스 최적화
- FK 과도한 사용

---

# 설계 원칙

- 단순한 테이블 구조 우선
- 명시적 SQL 사용
- Raw 데이터 추적 가능성 유지
- 원본 파일 경로 보존
- 과도한 normalization 금지
- 향후 PostgreSQL/Supabase 전환 가능성 고려

---

# 관련 문서

```text
docs/architecture/storage-architecture.md
docs/data/data-sources.md
tasks/todo/TASK-005-design-mariadb-schema.md
```
