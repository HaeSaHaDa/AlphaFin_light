# TASK-006-connect-collectors-to-mariadb.md

# TASK-006 Collector와 MariaDB 연결

## 상태

DONE

---

# 목표

기존 Collector가 수집한 데이터를
MariaDB에 저장할 수 있도록 초기 DB 연결 구조 구축.

---

# 범위

- MariaDB 연결 설정 (.env 기반)
- schema.sql 실행 검증
- companies, stock_prices, dart_disclosures,
  news_articles, collection_logs 저장 구현
- 샘플 데이터 DB 저장 검증

---

# 관련 Prompt

```text
prompts/TASK-006/prompt-001.md
```

---

# 관련 Logs

```text
logs/TASK-006/result-001.md
```

---

# 완료 조건

- MariaDB 연결 성공
- schema.sql 실행 성공
- 각 Collector DB 저장 성공
- collection_logs 기록 성공
- TASK 범위 외 구현 없음
