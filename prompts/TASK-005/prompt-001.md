# TASK-005 Prompt-001

날짜: 2026-05-26
실행 대상: Cursor

---

# 목적

```text
MariaDB 초기 스키마 설계 (수집 데이터 저장용)
```

---

# 프롬프트

```text
AGENTS.md와 TASK-005 기준으로 작업해라.

현재 작업:

1. TASK-004-build-news-collector 완료 처리
2. TASK-005-design-mariadb-schema 초기 설계

수행 내용:

- TASK-004 완료 조건 검토 및 tasks/done/ 이동
- prompts/TASK-005/ 생성
- logs/TASK-005/ 생성
- database/ 디렉토리 생성
- database/schema.sql 생성
- database/README.md 생성
- MariaDB 기반 초기 스키마 설계
- companies, stock_prices, dart_disclosures,
  news_articles, collection_logs 테이블 설계
- 기본 인덱스 설계
- CREATE TABLE 실행 가능 형태 유지

현재 범위: MariaDB schema.sql 설계,
초기 관계형 구조 정의, Raw 데이터 저장 구조 정의

제외 범위: 실제 DB 연결, pymysql, SQLAlchemy,
ORM, Collector DB 저장, Migration,
RAG/Embedding/Vector DB 테이블
```

---

# 결과

```text
- TASK-004 → tasks/done/ 이동 완료 (DONE 상태)
- prompts/TASK-005/, logs/TASK-005/ 생성 완료
- database/ 디렉토리 생성 완료
- database/schema.sql 생성 완료 (5개 테이블, 12개 인덱스)
- database/README.md 생성 완료
- SQL 구조 검증 완료 (괄호 균형, 키 카운트 정상)
```
