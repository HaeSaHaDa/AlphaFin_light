# TASK-041 result-001

## 수행 요약

- TASK-040 `tasks/done/` 이동 및 DONE 처리
- TASK-041 `tasks/doing/` 전환, `prompts/TASK-041/prompt-001.md` 작성
- Event Consolidation Layer (`src/event_consolidation/`)
  - `event_consolidator.py`, `news_deduplicator.py`, `disclosure_deduplicator.py`
  - `event_similarity.py`, `canonical_event_builder.py`
  - `event_confidence.py`, `event_importance.py`
  - `event_memory_manager.py`, `event_repository.py`
- DB 테이블: `market_events`, `event_evidence`, `event_memory_layers`
- API
  - `GET /api/events/{trace_id}`
  - `GET /api/events/ticker/{ticker}`
  - `GET /api/events/{event_id}/evidence`
  - `GET /api/memory/events/{trace_id}`
- Retrieval/Memory 연동
  - retrieval payload chunk dedup + `canonical_events`
  - memory layer item dedup + `event_memory_layers`
- Dashboard
  - `EventSummaryPanel`, `CanonicalEventCard`, `EventTimeline` 등
  - GlobalSectionNav "이벤트" 섹션

## 검증

- `python src/event_consolidation/event_consolidator.py <trace_id>` (로컬 trace 기준)
- `GET /api/events/{trace_id}` smoke

## 남은 확인

- 실제 DB 연결 환경에서 persist upsert E2E
- memory timeline UI에 event_memory_layers 시각화 고도화
- semantic similarity threshold 튜닝 (현재 title fuzzy 0.72)
