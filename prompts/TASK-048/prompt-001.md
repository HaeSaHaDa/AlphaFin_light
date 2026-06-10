# TASK-048 prompt-001

## 날짜

```text
2026-06-09
```

## 실행 주체

```text
Codex
```

## 목적

Runtime 결과처럼 노출되던 Demo Signal과 고정 Stock Chain 진입점을 제거하고,
selectedTicker, Runtime query, retrieval, event 기반 흐름만 유지한다.

## 수행 범위

- Demo outcome 및 timeline 제거
- 실제 시장 결과 미연동 상태 명시
- 과거 demo signal cache 재사용 차단
- 고정 Stock Chain relation 및 propagation seed 제거
- 과거 고정 chain의 API 노출 차단
- Unified Engine ticker 필수화
- Runtime CLI query 필수화
- Frontend Pipeline fallback 단일화
- 표준 Runtime 실행 명령 문서 반영

## 제한 사항

- 신규 기능 추가 금지
- Schema 변경 금지
- Backtesting 금지
- Auto Trading 금지
- 대규모 Refactoring 금지
- UI Redesign 금지
- 안전한 empty/error/timeout fallback 유지

## 결과 위치

```text
logs/TASK-048/result-001.md
```
