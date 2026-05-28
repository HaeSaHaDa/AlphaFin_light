# Runtime State Audit

## Frontend

| Store | 위치 | 역할 |
|-------|------|------|
| selectedTicker | `runtime-query-context.tsx` | 분석 실행 시 설정 |
| traceId | `runtime-query-context.tsx` | query/run 후 panel load |
| session | `runtime-session.ts` | 서브페이지 trace 연동 |
| panel data | `loadRuntimePanels(traceId)` | 6+1 API 병렬 |

## 제거됨

- `useDashboardData` local latest load on mount
- `api.ts` `/latest` suffix (traceId 필수 throw)
- `loadLatest()` on event-graph / analysis mount

## Loading

- `phase`: idle → running_query → loading_panels → ready
- 패널별 skeleton, sample fallback 없음
