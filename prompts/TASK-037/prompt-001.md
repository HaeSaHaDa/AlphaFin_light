# TASK-037 Prompt 001

## 목표

selectedTicker 중심 Market Relationship Graph + Sticky Runtime Header/Section Navigation 구축.

## 수행

- `GET /api/market-graph/{trace_id}`, `GET /api/runtime-status/{trace_id}` 추가
- Event Graph를 시장 관계 그래프로 재구성 (node category, edge type, relevance, tooltip, legend)
- Dashboard에 sticky runtime header + section scroll navigation 연결
- sample/generic fallback 제거, traceId + selectedTicker 기준만 렌더

## 검증

- 삼성전기 선택 시 중심 노드: 삼성전기/009150
- 현대자동차 선택 시 중심 노드: 현대자동차/005380
- 삼성전자 샘플 graph fallback 미노출
- Header 고정, section navigation 클릭 시 스크롤 이동 정상
