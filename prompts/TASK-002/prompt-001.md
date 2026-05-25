# TASK-002 Prompt-001

날짜: 2026-05-25
실행 대상: Cursor

---

# 목적

```text
pykrx 기반 한국 주식 일봉 데이터 수집기 초기 구조 구현
```

---

# 프롬프트

```text
AGENTS.md와 TASK-002 기준으로 작업해라.

현재 작업:
TASK-002-build-pykrx-collector

목표:
pykrx 기반 한국 주식 일봉 데이터 수집기의
초기 구조를 구현한다.

작업 시작 전 다음 문서를 확인한다.

README.md
AGENTS.md
project/current-status.md
project/alphafin-lte-scope.md
docs/architecture/module-structure.md
docs/architecture/execution-flow.md
docs/architecture/storage-architecture.md
docs/conventions/cursor-workflow.md
docs/conventions/task-template.md
docs/conventions/validation-rules.md
docs/data/data-sources.md
tasks/todo/TASK-002-build-pykrx-collector.md

수행 내용:

- prompts/TASK-002/ 생성
- logs/TASK-002/ 생성
- src/collectors/pykrx/ 생성
- collector.py 생성
- run_sample.py 생성
- pykrx 기반 단일 종목 OHLCV 수집 구현
- CSV 저장 구현
- data/raw/price/ 저장 구조 사용
- 삼성전자(005930) 기준 샘플 실행 검증

구현 범위:

- 단일 종목
- 단일 날짜 범위
- CSV 저장
- Raw Data 저장
- 기본 로그 출력

제외 범위:

- DB 저장 구현 금지
- MariaDB 연동 금지
- 멀티 종목 처리 금지
- 병렬 처리 금지
- 스케줄러 구현 금지
- RAG 연결 금지
- Embedding 생성 금지
- LLM 연동 금지
- 성능 최적화 금지
- 과도한 abstraction 금지

완료 기준:

- run_sample.py 실행 가능
- 삼성전자 005930 데이터 수집 성공
- CSV 저장 성공
- data/raw/price/ 저장 확인
- prompts/TASK-002/prompt-001.md 저장
- logs/TASK-002/result-001.md 기록
```

---

# 결과

```text
- 문서 13개 확인 완료
- prompts/TASK-002/ 생성 완료
- logs/TASK-002/ 생성 완료
- src/collectors/pykrx/ 생성 완료 (__init__.py, collector.py, run_sample.py)
- data/raw/price/ 생성 완료
- run_sample.py 실행 성공 (exit code 0)
- 삼성전자 005930 OHLCV 22행 수집 완료
- CSV 저장 완료: data/raw/price/005930_20240101_20240131.csv
- 컬럼: 날짜, 시가, 고가, 저가, 종가, 거래량, 등락률
```
