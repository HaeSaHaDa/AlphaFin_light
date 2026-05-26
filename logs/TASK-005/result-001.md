# TASK-005 실행 결과 (result-001)

날짜: 2026-05-26
실행 대상: Cursor
Prompt: prompts/TASK-005/prompt-001.md

---

# 목적

MariaDB 초기 스키마 설계 및 DDL 파일 생성

---

# 사전 작업: TASK-004 완료 처리

```text
- tasks/todo/TASK-004-build-news-collector.md → tasks/done/ 이동
- 상태: DONE
```

---

# 생성 파일

```text
database/schema.sql   (MariaDB DDL - 5개 테이블)
database/README.md    (스키마 설명 문서)
```

---

# 생성 디렉토리

```text
prompts/TASK-005/
logs/TASK-005/
database/
```

---

# 테이블 설계 결과

| 테이블 | 역할 | PK | UNIQUE | INDEX |
|--------|------|----|--------|-------|
| companies | 기업 기본 정보 | id | ticker | corp_code |
| stock_prices | 일봉 주가 OHLCV | id | ticker+trade_date | trade_date |
| dart_disclosures | OpenDART 공시 | id | receipt_no | corp_code+receipt_date, ticker |
| news_articles | 뉴스 기사 | id | url(255) | ticker+published_at, keyword |
| collection_logs | 수집 실행 로그 | id | - | collector_name+started_at, status |

---

# 설계 상세

## companies

```text
필드 수: 7
주요 필드: ticker, corp_code, company_name, market
UNIQUE: ticker
용도: 종목코드-기업명 매핑, OpenDART corp_code 관리
```

## stock_prices

```text
필드 수: 10
주요 필드: ticker, trade_date, OHLCV, change_rate
UNIQUE: (ticker, trade_date) 중복 방지
용도: pykrx 수집 데이터 저장
```

## dart_disclosures

```text
필드 수: 10
주요 필드: corp_code, report_name, receipt_no, receipt_date
UNIQUE: receipt_no 중복 방지
추가: raw_json (원본 보존), raw_file_path (파일 추적)
용도: OpenDART 공시 목록 저장
```

## news_articles

```text
필드 수: 10
주요 필드: keyword, title, content, source, url, published_at
UNIQUE: url (prefix 255) 중복 방지
추가: raw_file_path (파일 추적)
용도: 뉴스 기사 저장
```

## collection_logs

```text
필드 수: 9
주요 필드: collector_name, target, status, row_count, error_message
용도: Collector 실행 이력 및 오류 추적
```

---

# 인덱스 요약

```text
총 인덱스: 12개
- PRIMARY KEY: 5개
- UNIQUE KEY: 4개
- INDEX: 8개 (일반 인덱스 + 복합 인덱스)
```

---

# SQL 검증 결과

## 구조 검증

```text
- CREATE TABLE 문: 5개 OK
- PRIMARY KEY: 5개 OK
- UNIQUE KEY: 4개 OK
- INDEX: 8개 OK
- 괄호 균형: 5개 테이블 모두 OK
- IF NOT EXISTS: 중복 실행 방지 OK
```

## 설계 원칙 준수

```text
- 단순 테이블 구조: OK
- ORM 미사용: OK
- FK 과도한 사용 없음: OK (FK 미사용)
- Raw 파일 경로 보존: OK (raw_file_path 필드)
- 원본 JSON 보존: OK (raw_json 필드)
- utf8mb4 인코딩: OK
- InnoDB 엔진: OK
```

---

# TASK-005 완료 조건 대비

| 조건 | 상태 |
|------|------|
| MariaDB 초기 스키마 설계 완료 | 완료 |
| database/schema.sql 생성 완료 | 완료 |
| database/README.md 생성 완료 | 완료 |
| 테이블 역할 문서화 완료 | 완료 |
| SQL 실행 가능성 검토 완료 | 완료 |
| 기본 인덱스 포함 | 완료 (12개) |
| 결과 로그 작성 완료 | 완료 |
| TASK 범위 외 구현 없음 | 확인 |
