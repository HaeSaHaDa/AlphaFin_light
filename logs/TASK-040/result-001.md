# TASK-040 result-001

## 수행 요약

- TASK-039를 `tasks/done/`으로 이동 및 상태 `DONE` 처리
- TASK-040 상태를 `DOING`으로 전환
- Disclosure Document Store 초기 구현
  - `src/disclosure/dart_collector.py`
  - `src/disclosure/disclosure_repository.py`
  - `src/disclosure/disclosure_chunker.py`
  - `src/disclosure/disclosure_embedder.py`
  - `src/disclosure/disclosure_retriever.py`
  - `src/disclosure/disclosure_summary.py`
  - `src/disclosure/disclosure_cache.py`
  - `src/disclosure/disclosure_query_builder.py`
- Disclosure API 추가
  - `/api/disclosure/collect`
  - `/api/disclosure/{ticker}`
  - `/api/disclosure/search`
  - `/api/disclosure/timeline/{ticker}`
  - `/api/disclosure/evidence/{trace_id}`
- Dashboard Disclosure 컴포넌트 추가
  - `DisclosurePanel`, `DisclosureViewer`, `DisclosureTimeline`,
    `DisclosureSummaryCard`, `DisclosureFilterBar`, `DisclosureEvidencePanel`
- Dashboard 메인 화면에 Disclosure Panel 통합
- market graph evidence에 disclosure 근거 문자열 포함

## 남은 확인

- 실제 OpenDART 키/회사 corp_code로 collect end-to-end 검증
- 공시 embedding 비용/캐시 정책 미세 조정
- disclosure semantic ranking 고도화(현재는 lexical + importance 혼합)
