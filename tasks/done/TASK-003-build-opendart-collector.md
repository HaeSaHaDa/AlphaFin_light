# TASK-003-build-opendart-collector.md

# TASK-003 OpenDART 공시 수집기 초기 구축

## 상태

DONE

---

# 목표

OpenDART 기반 기업 공시 수집기의
초기 구조를 구축한다.

현재 TASK의 목표는
단일 기업 기준으로 공시 데이터를 수집하고
Raw Data로 저장하는 최소 Collector를 만드는 것이다.

---

# 범위

현재 TASK에서 포함하는 작업:

- `src/collectors/opendart/` 구조 생성
- OpenDART API 연동
- 환경변수 기반 API KEY 로드
- 단일 기업 공시 목록 조회
- JSON 저장
- Raw Data 저장 구조 사용
- 샘플 실행 스크립트 작성
- 기본 로그 출력
- 샘플 실행 검증

---

# 관련 Prompt

```text
prompts/TASK-003/prompt-001.md
```

---

# 관련 Logs

```text
logs/TASK-003/result-001.md
```

---

# 완료 조건

- OpenDART collector 초기 구조 생성 완료
- 단일 기업 공시 목록 수집 성공
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
