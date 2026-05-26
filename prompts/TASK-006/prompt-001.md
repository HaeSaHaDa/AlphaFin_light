# TASK-006 Prompt-001

날짜: 2026-05-26
실행 대상: Cursor

---

# 목적

```text
Collector와 MariaDB 연결 - DB 저장 구조 구축
```

---

# 프롬프트

```text
AGENTS.md와 TASK-006 기준으로 작업해라.

현재 작업:

1. TASK-005-design-mariadb-schema 완료 처리
2. TASK-006-connect-collectors-to-mariadb 초기 구현

수행 내용:

- TASK-005 완료 조건 검토 및 tasks/done/ 이동
- prompts/TASK-006/ 생성
- logs/TASK-006/ 생성
- src/common/db/ 생성
- connection.py 생성 (pymysql + .env)
- init_schema.py 생성 (schema.sql 실행)
- store.py 생성 (각 테이블 INSERT 함수)
- run_db_sample.py 생성 (통합 검증)
- 기존 Raw 데이터 DB 저장 검증
- 중복 실행 안전성 검증

환경 변수: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
현재 범위: MariaDB 연결, schema.sql 실행, Collector DB 저장
제외 범위: ORM, SQLAlchemy, Migration, 비동기, Connection Pool
```

---

# 결과

```text
- TASK-005 → tasks/done/ 이동 완료
- src/common/db/ 생성 완료
  - connection.py (DB 연결)
  - init_schema.py (스키마 실행)
  - store.py (INSERT 함수)
  - run_db_sample.py (통합 검증)
- MariaDB 연결 성공
- schema.sql 실행 성공 (5개 구문)
- 주가 22건, 공시 15건, 뉴스 5건 저장 성공
- collection_logs 기록 성공
- 중복 실행 안전성 확인 (INSERT IGNORE)
- rcept_no 필드명 매핑 오류 수정 완료
```
