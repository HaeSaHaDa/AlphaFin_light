# TASK-002-build-pykrx-collector.md

# TASK-002 pykrx 주가 수집기 초기 구축

## 상태

TODO

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

# 구현 규칙

현재 TASK는 다음 규칙을 따른다.

- 작은 함수 유지
- 단일 책임 유지
- 하드코딩 최소화
- 예외 무시 금지
- 실패 시 명확한 오류 메시지 출력
- 과도한 추상화 금지
- DB 연결 금지
- 수집 결과는 Raw Data로 저장

---

# 예상 기능

## collector.py

역할:

- 종목코드 입력
- 시작일 입력
- 종료일 입력
- pykrx로 OHLCV 데이터 수집
- DataFrame 반환
- CSV 저장 함수 제공

예상 함수:

```text
fetch_ohlcv(ticker, start_date, end_date)
save_price_csv(df, ticker, start_date, end_date)
```

---

## run_sample.py

역할:

- 샘플 종목 기준 수집 실행
- CSV 저장 확인
- 실행 결과 출력

샘플 기준:

```text
ticker: 005930
start_date: 20240101
end_date: 20240131
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## 실행 검증

- `run_sample.py` 실행 가능 여부
- 삼성전자 `005930` 데이터 수집 가능 여부
- CSV 파일 생성 여부

---

## 데이터 검증

- CSV 파일이 비어 있지 않은지 확인
- 날짜 컬럼 또는 인덱스 확인
- 시가 / 고가 / 저가 / 종가 / 거래량 데이터 확인

---

## 구조 검증

- `src/collectors/pykrx/` 구조 정상 여부
- `data/raw/price/` 저장 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-002/
```

---

# 관련 Logs

```text
logs/TASK-002/
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

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-003-build-opendart-collector
- TASK-004-build-news-collector
- TASK-005-design-mariadb-schema

단,
DB 저장은 현재 TASK에서 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- 단일 기능 우선 구현
- Raw Data 저장 우선
- 검증 가능한 샘플 우선
- AI 협업 가능한 구조 유지