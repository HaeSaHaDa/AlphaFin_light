# TASK-049 추가 회귀 수정 결과 013

## 확인한 문제

- 새 종목을 선택해도 이전 Runtime ticker 동기화 effect가 검색 입력과 선택 상태를 다시 덮어썼다.
- Runtime ticker 변경 시 이전 회사명이 새 query에서 추출한 회사명보다 우선되는 경로가 있었다.
- 과거 Analysis Memory, Reflection, Event Graph, Stock Chain이 새 분석 프롬프트에 재주입되며 기존 반도체 분석을 반복했다.
- ticker 필터가 없는 Layered/Temporal Memory 조회로 다른 기업의 생성 결과가 섞일 수 있었다.

## 수정 내용

- `GlobalRuntimeSearch`의 Runtime hydration 상태를 사용자 선택 상태와 분리했다.
- 새 Runtime query에서 추출한 회사명을 이전 회사명보다 우선하도록 수정했다.
- Layered Memory 조회에 ticker 및 memory type 필터를 추가했다.
- 새 분석 프롬프트에는 ticker가 일치하고 원문 근거가 있는 `event_memory`만 허용했다.
- 과거 생성형 Reflection, Event Graph, Stock Chain은 조회 데이터로 유지하되 새 분석 근거에서는 제외했다.
- Analysis와 Reflection 결과에 ticker가 보존되도록 수정했다.

## 검증

- `npm.cmd run lint`: 성공
- `npx.cmd tsc --noEmit`: 성공
- 변경 Python 모듈 `compileall`: 성공
- Frontend `http://localhost:3000/`: HTTP 200
- Backend `http://localhost:8000/health`: 정상
- NAVER `035420` Runtime trace `20260609_172317`: 성공
- 새 trace의 모든 referenced ticker: `035420`
- 새 분석 Summary/Bearish/Risk의 `반도체`, `HBM`: 없음

## 남은 참고 사항

- 삼성화재처럼 실제 수집 뉴스가 삼성전자 지분과 반도체 시황을 다루는 경우에는 해당 문구가 검색 근거에 포함될 수 있다.
- 과거 저장 데이터의 오염 내용은 삭제하지 않았다. 새 Runtime 분석 프롬프트에서의 재사용만 차단했다.
- 브라우저 자동 클릭 검증은 Windows 브라우저 샌드박스 초기화 실패로 수행하지 못했으며, 정적 검사와 API Runtime 실행으로 검증했다.
- `tasks/` 파일은 수정하지 않았다.
