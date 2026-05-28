# TASK-036 Prompt 001

## 목표

Dashboard·Runtime 전수 Audit — hardcoded / sample / latest fallback 제거.

## 수행

- grep 기반 탐지 + 패널별 traceId 바인딩 검증
- `audit/runtime-audit/*.md` 보고서
- UI/API hardcoded 제거 (stock chain, graph, timeline, /latest)

## 검증

- 삼성전기 vs 현대차 trace payload 분리
- /latest → 400
