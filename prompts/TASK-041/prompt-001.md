# TASK-041 prompt-001

## 목표

Event Consolidation Layer 및 Memory Deduplication 초기 구현.

## 범위

- `src/event_consolidation/*` 모듈
- `market_events`, `event_evidence`, `event_memory_layers` 테이블
- API: `/api/events/*`, `/api/memory/events/{trace_id}`
- Dashboard `EventSummaryPanel` 및 이벤트 타임라인

## 원칙

- selectedTicker / traceId 유지
- Runtime payload only
- OpenAI 호출 없음 (lexical/fuzzy similarity)
- memory layer active uniqueness
