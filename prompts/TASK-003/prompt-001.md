# TASK-003 Prompt-001

날짜: 2026-05-25
실행 대상: Cursor

---

# 목적

```text
OpenDART 기반 기업 공시 수집기 초기 구조 구현
```

---

# 프롬프트

```text
AGENTS.md와 TASK-003 기준으로 작업해라.

현재 작업:

1. TASK-002-build-pykrx-collector 완료 처리
2. TASK-003-build-opendart-collector 초기 구현

수행 내용:

- TASK-002 완료 조건 검토 및 tasks/done/ 이동
- prompts/TASK-003/ 생성
- logs/TASK-003/ 생성
- src/collectors/opendart/ 생성
- collector.py 생성
- run_sample.py 생성
- .env 기반 DART_API_KEY 로드 구현
- OpenDART 공시 목록 조회 구현
- JSON 저장 구현
- data/raw/dart/ 저장 구조 사용
- 삼성전자 기준 샘플 실행 검증

구현 범위:

- 단일 기업
- 단일 날짜 범위
- JSON 저장
- Raw Data 저장
- 기본 로그 출력

샘플 기준:

- 기업: 삼성전자
- corp_code: 00126380
- 기간: 20240101 ~ 20240131

제외 범위:

- DB 저장, MariaDB, 사업보고서 파싱, PDF, XML 상세,
  Chunking, Embedding, RAG, LLM, 멀티 기업, 병렬, 스케줄러

완료 기준:

- run_sample.py 실행 가능
- OpenDART API 연결 성공
- 삼성전자 공시 목록 수집 성공
- JSON 저장 성공
- data/raw/dart/ 저장 확인
- TASK-002 done 이동 완료
- prompts/TASK-003/prompt-001.md 저장
- logs/TASK-003/result-001.md 기록
```

---

# 결과

```text
- 문서 13개 확인 완료
- TASK-002 → tasks/done/ 이동 완료 (DONE 상태)
- prompts/TASK-003/ 생성 완료
- logs/TASK-003/ 생성 완료
- src/collectors/opendart/ 생성 완료 (__init__.py, collector.py, run_sample.py)
- data/raw/dart/ 생성 완료
- .env에서 DART_API_KEY 로드 성공
- run_sample.py 실행 성공 (exit code 0)
- 삼성전자 공시 15건 수집 완료
- JSON 저장 완료: data/raw/dart/samsung_electronics_disclosures.json
```
