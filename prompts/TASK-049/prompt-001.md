# TASK-049 prompt-001

## 날짜

```text
2026-06-09
```

## 실행 주체

```text
Codex
```

## 목적

Navigation 정리와 Demo/기본값 제거 이후 발생한 Sidebar, Header Search,
selectedTicker, traceId 및 Runtime 실행 회귀를 찾아 기존 동작을 복구한다.

## 수행 범위

- Sidebar 메뉴 route와 section target 점검
- Header 종목 검색, 선택, 분석 실행 복구
- selectedTicker 기반 `/api/query/run` 실행
- 새 traceId의 URL 및 session 동기화
- URL/session trace 진입 시 Dashboard panel 자동 복원
- Runtime, Event, Disclosure 관련 API 응답 확인
- Frontend route 렌더 및 Next.js build 확인

## 제한 사항

- 신규 기능 추가 금지
- Schema 변경 금지
- Backtesting 금지
- Auto Trading 금지
- 대규모 Refactoring 금지
- UI Redesign 금지

## 결과 위치

```text
logs/TASK-049/result-001.md
```
