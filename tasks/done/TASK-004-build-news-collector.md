# TASK-004-build-news-collector.md

# TASK-004 뉴스 수집기 초기 구축

## 상태

DONE

---

# 목표

뉴스 기반 시장 정보 수집기의
초기 구조를 구축한다.

---

# 범위

- `src/collectors/news/` 구조 생성
- 네이버 뉴스 검색 기반 수집
- 뉴스 URL 추출
- 기사 본문 수집
- JSON 저장
- Raw Data 저장 구조 사용
- 샘플 실행 스크립트 작성
- 기본 로그 출력
- 샘플 실행 검증

---

# 관련 Prompt

```text
prompts/TASK-004/prompt-001.md
```

---

# 관련 Logs

```text
logs/TASK-004/result-001.md
```

---

# 완료 조건

- 뉴스 collector 초기 구조 생성 완료
- 뉴스 검색 성공
- 기사 본문 수집 성공
- JSON 저장 성공
- 샘플 실행 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- Raw Data 우선 저장
- 검증 가능한 샘플 우선
- 단일 기능 우선 구현
- AI 협업 가능한 구조 유지
