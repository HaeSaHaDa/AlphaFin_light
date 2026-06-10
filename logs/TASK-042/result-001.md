# TASK-042 result-001

## 수행 요약

- TASK-041 `tasks/done/` DONE 확인
- TASK-042 `tasks/doing/` 전환
- `src/runtime_query/` 모듈 7종 구현
  - `runtime_query_pipeline.py` — runQuery disclosure-aware 오케스트레이션
  - `runtime_context_assembler.py`, `disclosure_runtime_integration.py`
  - `unified_retrieval_builder.py`, `disclosure_retrieval_ranker.py`
  - `runtime_evidence_merger.py`, `disclosure_timeout_guard.py`
- `run_runtime_query_selected` → `run_disclosure_aware_query` 연동
- `engine_runner.run_unified_pipeline(preloaded_chunks, runtime_context)` 확장
- unified result에 `runtime_context` 저장
- API
  - `GET /api/runtime/context/{trace_id}`
  - `GET /api/runtime/evidence/{trace_id}`
  - `POST /api/query/run` 응답에 disclosure counts + runtime_context
- Signal evaluation disclosure-aware confidence 보정
- Event consolidator runtime_context disclosure_chunks 우선 사용
- Dashboard `RuntimeEvidencePanel`, `UnifiedEvidenceViewer`, `DisclosureRuntimeBadge`

## 검증

- `python -c "from src.runtime_query.runtime_query_pipeline import run_disclosure_aware_query"` import OK
- `from src.dashboard_api.app import create_app` OK

## 남은 확인

- OpenDART 키 환경에서 collect prefetch E2E
- 실제 runQuery 후 unified result `runtime_context.has_disclosure=true` 확인
