# Hardcoded Data Report — TASK-036

## Summary

**Runtime Purity:** Dashboard UI는 traceId 기반만 렌더링. TASK-036에서 잔여 demo/hardcoded UI 경로 제거.

## Removed / Fixed

1. `stock-chain-viewer.tsx` — `preferred = [NVIDIA, 삼성전자, ...]`
2. `engine-step-timeline.tsx` — `DEMO_FLOW`
3. `event-graph/transform.ts` — layout seeds NVIDIA/삼성전자/HBM
4. `GraphToolbar.tsx` — `HIGHLIGHT_PRESETS`
5. `ExplainabilityAccordion` / `AccuracyPanel` — "(샘플)" labels
6. API routes — `/latest` disabled (400)
7. `signal_service.fetch_latest_signal` — no cross-trace cache

## Not Hardcoded (Verified)

- `RuntimeQueryProvider` + `loadRuntimePanels`
- `requireTracePath` in `api.ts`
- `runtime-session.ts` for sub-pages
- `company_search_service` exact match scoring (no auto-pick 삼성전자)

## Residual (Acceptable)

- `query-input-panel.tsx` — legacy, not used on main dashboard
- `run_sample.py` — dev script only
- Empty states — user-facing messages, not fake data

## Demo Verification

```text
삼성전기 선택 + MLCC 키워드 → 분석 실행
→ traceId T
→ 모든 패널 GET /*/T
→ sessionStorage에 T 저장
→ Event Graph / Memory / Signal ?trace_id=T
```

현대자동차 동일 절차 시 **다른 traceId**, payload 분리.
