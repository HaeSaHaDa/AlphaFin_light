# TASK-003-build-opendart-collector.md

# TASK-003 OpenDART 공시 수집기 초기 구축

## 상태

TODO

---

# 목표

OpenDART 기반 기업 공시 수집기의
초기 구조를 구축한다.

현재 TASK의 목표는
단일 기업 기준으로 공시 데이터를 수집하고
Raw Data로 저장하는 최소 Collector를 만드는 것이다.

현재 단계에서는
복잡한 문서 분석보다
기본 수집 구조 안정화에 집중한다.

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

# 현재 제외 범위

현재 TASK에서 제외:

- DB 저장
- MariaDB 연동
- 사업보고서 본문 전문 파싱
- PDF 처리
- XML 상세 파싱
- Chunking
- Embedding 생성
- RAG 연결
- LLM 분석
- 멀티 기업 처리
- 병렬 처리
- 스케줄러
- 성능 최적화

현재 TASK는
공시 목록 수집기 초기 구조만 구현한다.

---

# 생성 대상 구조

```text
src/collectors/opendart/
├─ __init__.py
├─ collector.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/raw/dart/
```

예상 저장 파일 예시:

```text
data/raw/dart/samsung_electronics_disclosures.json
```

---

# 구현 규칙

현재 TASK는 다음 규칙을 따른다.

- 작은 함수 유지
- 단일 책임 유지
- 하드코딩 최소화
- 환경변수 사용
- 예외 무시 금지
- 명확한 오류 메시지 출력
- 과도한 abstraction 금지
- Raw Data 원본 유지
- DB 저장 금지

---

# 환경 변수 사용

사용 환경 변수:

```text
DART_API_KEY
```

`.env` 파일 기준으로 로드한다.

---

# 예상 기능

## collector.py

역할:

- OpenDART API 요청
- 기업 공시 목록 조회
- JSON 데이터 반환
- JSON 저장

예상 함수:

```text
load_api_key()
fetch_disclosures(corp_code, begin_date, end_date)
save_disclosures_json(data, output_path)
```

---

## run_sample.py

역할:

- 샘플 기업 기준 실행
- 공시 목록 수집
- JSON 저장 검증
- 실행 결과 출력

샘플 기준:

```text
기업: 삼성전자
corp_code: 00126380
기간: 20240101 ~ 20240131
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## 실행 검증

- `run_sample.py` 실행 가능 여부
- OpenDART API 연결 성공 여부
- JSON 저장 성공 여부

---

## 데이터 검증

- 공시 목록 데이터 존재 여부
- 공시 날짜 존재 여부
- 공시 제목 존재 여부
- JSON 비어 있지 않은지 확인

---

## 구조 검증

- `src/collectors/opendart/` 구조 정상 여부
- `data/raw/dart/` 저장 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-003/
```

---

# 관련 Logs

```text
logs/TASK-003/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- OpenDART collector 초기 구조 생성 완료
- 단일 기업 공시 목록 수집 성공
- JSON 저장 성공
- 샘플 실행 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-004-build-news-collector
- TASK-005-design-mariadb-schema
- TASK-006-build-chunking-pipeline

단,
Chunking 및 RAG 연결은
현재 TASK에서 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- Raw Data 우선 저장
- 검증 가능한 샘플 우선
- 단일 기능 우선 구현
- AI 협업 가능한 구조 유지
- 재현 가능한 실험 구조 유지