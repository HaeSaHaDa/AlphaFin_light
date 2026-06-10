# TASK-047 prompt-001

## 날짜

```text
2026-06-09
```

## 실행 주체

```text
Codex
```

## 목적

초기 개발 단계의 sample, mock, demo, fallback, placeholder 및 고정 종목 값이
현재 Runtime 경로에 남아 있는지 프로젝트 전체를 재점검한다.

## 수행 범위

- `src/`, `dashboard-ui/src/` 문자열 검색
- Runtime, Retrieval, Disclosure, Event, Memory, Graph, API 호출 경로 확인
- sample/mock 코드와 실제 Runtime 진입 코드 분리
- hardcoded ticker/company와 selectedTicker 기반 처리 비교
- fallback 및 `/latest` 호환 경로의 안전성 판단
- 제거 또는 격리가 필요한 후보 기록

## 제한 사항

- 신규 기능 추가 금지
- Refactoring 금지
- Schema 변경 금지
- Backtesting 금지
- Auto Trading 금지
- UI 변경 금지
- Audit 결과 문서와 TASK 상태 외 코드 수정 금지

## 결과 위치

```text
logs/TASK-047/result-001.md
```
