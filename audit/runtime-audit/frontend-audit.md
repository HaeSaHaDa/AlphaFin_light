# Frontend Rendering Audit

## Audit 결과

| 패턴 | 발견 | 조치 |
|------|------|------|
| loadLatest on mount | event-graph, analysis (과거) | 제거됨 (TASK-035) |
| api /latest | api.ts suffix | traceId 필수 |
| DEMO_FLOW timeline | engine-step-timeline | 제거 |
| NVIDIA graph seeds | transform.ts | ticker/query root |
| HIGHLIGHT_PRESETS | GraphToolbar | runtime entities |
| preferred stock links | stock-chain-viewer | ticker links |
| mock news headlines | RelatedNewsPanel | 제거 (TASK-035) |
| Signal fallback 50% | SignalSummaryCard | 제거 (TASK-035) |

## useEffect

- `useSignalEvaluation`: traceId 없으면 idle, fetch 안 함
- `useMemoryTimeline`: 동일
- `useEventGraph`: traceId 필수
- `useCompanySearch`: autocomplete only

## Placeholder

- Input placeholder 텍스트는 UX용 (payload 아님) — 유지
