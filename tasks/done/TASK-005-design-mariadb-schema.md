# TASK-005-design-mariadb-schema.md

# TASK-005 MariaDB 저장 스키마 설계

## 상태

DONE

---

# 목표

MariaDB 초기 스키마 설계.
주가, 공시, 뉴스 데이터를 관계형 DB에 저장할 수 있는
최소 테이블 구조 정의.

---

# 범위

- MariaDB 초기 스키마 설계
- companies, stock_prices, dart_disclosures,
  news_articles, collection_logs 테이블 설계
- SQL DDL 파일 작성
- 스키마 설명 문서 작성

---

# 관련 Prompt

```text
prompts/TASK-005/prompt-001.md
```

---

# 관련 Logs

```text
logs/TASK-005/result-001.md
```

---

# 완료 조건

- MariaDB 초기 스키마 설계 완료
- database/schema.sql 생성 완료
- database/README.md 생성 완료
- 테이블 역할 문서화 완료
- SQL 실행 가능성 검토 완료
- TASK 범위 외 구현 없음
