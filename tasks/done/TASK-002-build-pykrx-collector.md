# TASK-002-build-pykrx-collector.md

# TASK-002 pykrx 주가 수집기 초기 구축

## 상태

DONE

---

# 목표

pykrx 기반 한국 주식 일봉 데이터 수집기의
초기 구조를 구축한다.

현재 TASK의 목표는
단일 종목 기준으로 주가 데이터를 수집하고
Raw Data로 저장하는 최소 Collector를 만드는 것이다.

---

# 범위

현재 TASK에서 포함하는 작업:

- `src/collectors/pykrx/` 구조 생성
- pykrx 기반 단일 종목 일봉 데이터 수집
- 날짜 범위 입력 처리
- CSV 저장
- Raw Data 저장 경로 사용
- 기본 실행 스크립트 작성
- 기본 로그 출력
- 샘플 실행 검증

---

# 현재 제외 범위

현재 TASK에서 제외:

- DB 저장
- MariaDB 연동
- 멀티 종목 수집
- 병렬 처리
- 스케줄러
- RAG 연결
- Embedding 생성
- LLM 분석
- 백테스트
- 성능 최적화

현재 TASK는
단일 종목 주가 수집기 초기 구조만 구현한다.

---

# 생성 대상 구조

```text
src/collectors/pykrx/
├─ __init__.py
├─ collector.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/raw/price/
```

샘플 실행 결과는 위 경로에 CSV로 저장한다.

예상 파일명 예시:

```text
data/raw/price/005930_20240101_20240131.csv
```

---

# 관련 Prompt

```text
prompts/TASK-002/prompt-001.md
```

---

# 관련 Logs

```text
logs/TASK-002/result-001.md
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- pykrx collector 초기 구조 생성 완료
- 단일 종목 일봉 데이터 수집 성공
- CSV 저장 성공
- 샘플 실행 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- 단일 기능 우선 구현
- Raw Data 저장 우선
- 검증 가능한 샘플 우선
- AI 협업 가능한 구조 유지
