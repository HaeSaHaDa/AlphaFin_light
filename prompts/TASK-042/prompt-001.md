# TASK-042 prompt-001

## 목표

runQuery 시 뉴스 + 공시 통합 retrieval 및 Unified Runtime Context 구축.

## 범위

- `src/runtime_query/*` 파이프라인
- `run_runtime_query_selected` disclosure-aware 연동
- `engine_runner` preloaded_chunks + runtime_context
- API `/api/runtime/context/{traceId}`, `/api/runtime/evidence/{traceId}`
- Dashboard `RuntimeEvidencePanel`

## 원칙

- selectedTicker 필수
- disclosure collect prefetch (cache, timeout)
- 공시 evidence HIGH priority
- OpenAI 호출 구조 유지 (context만 통합)
