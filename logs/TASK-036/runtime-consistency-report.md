# Runtime Consistency Report — TASK-036

## Synchronization

| Layer | Mechanism |
|-------|-----------|
| Query run | `POST /api/query/run` → single traceId |
| Dashboard | `loadRuntimePanels(traceId)` parallel fetch |
| Sub-pages | URL `?trace_id=` or `runtime-session` |
| Nav links | `traceQueryHref()` |

## Consistency checks

- [x] Signal/News/Graph/Memory/Eval/Reflection/Retrieval same traceId on home
- [x] No client call to `/latest`
- [x] Memory filtered by trace query/ticker
- [x] Stock chain filtered by trace ticker
- [x] Company search requires explicit selection (no 삼성전자 auto)

## User-reported issue (현대차 vs 삼성)

**Root causes addressed:**

1. Sub-pages without trace_id → session + nav fix (TASK-035/036)
2. Memory API returned global layer files → trace filter (TASK-035)
3. Stock chain showed NVIDIA path → ticker-based links (TASK-036)
4. Graph highlights 삼성전자 preset → runtime entities (TASK-036)
