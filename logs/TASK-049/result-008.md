# TASK-049 메모리 종목 필터 회귀 수정 결과

## 요청

메모리 화면에서 전체 DB 데이터가 아니라 현재 검색한 종목과 관련된 메모리만 표시한다.

## 발견한 원인

- 메모리 API가 전체 SHORT/MID/LONG 저장소를 읽은 뒤 query 또는 ticker가 느슨하게 일치하는 항목을 반환했다.
- 과거 저장 데이터 일부는 실제 질의 회사와 다른 ticker가 연결되어 있었다.
- ticker만 비교하면 삼성전자 `005930` 조회에 현대자동차, 삼성전기, K컬처 관련 메모리가 포함될 수 있었다.
- API 응답 schema에 ticker가 없어 프런트엔드가 현재 메모리 응답의 종목을 확인할 수 없었다.

## 수정 내용

- 활성 trace의 query에서 선택 회사명과 ticker를 확인한다.
- 명시 ticker 또는 referenced chunk ticker가 선택 ticker와 정확히 일치하는 항목만 허용한다.
- 선택 회사명이나 ticker가 메모리 문맥에 없는 과거 오염 항목은 제외한다.
- 현재 trace의 analysis memory에도 동일한 필터를 적용한다.
- 메모리 API 및 프런트 타입에 `ticker` 필드를 추가한다.

## 검증 결과

### 삼성전자

- trace: `20260609_155431`
- query: `삼성전자 005930`
- ticker: `005930`
- SHORT: 2건
- MID: 5건
- LONG: 0건
- 현대자동차, 삼성전기, K컬처 관련 항목이 제거됨을 확인했다.

### 삼성전기

- trace: `20260609_154829`
- query: `삼성전기 009150 MLCC`
- ticker: `009150`
- SHORT: 1건
- MID: 1건
- LONG: 0건
- 삼성전자 메모리와 분리됨을 확인했다.

### 실행 검증

- Python compileall 통과
- `npm.cmd run lint` 통과
- `npx.cmd tsc --noEmit` 통과
- `git diff --check` 통과
- Backend health `200`
- Frontend memory route `200`
- 실제 `/api/memory/{trace_id}` 응답에서 ticker와 종목별 메모리 분리 확인

## 제한 사항

인앱 브라우저 자동화는 Windows 샌드박스 초기화 오류로 실행되지 않았다. 프런트 라우트 HTTP 응답과 실제 API 응답으로 대체 검증했다.

## TASK 파일

이번 수정에서는 `tasks/` 아래 파일을 수정하거나 이동하지 않았다.
