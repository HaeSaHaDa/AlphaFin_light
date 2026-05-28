# TASK-036 Extension — selectedTicker 중심 Event Graph / Stock Chain

## 규칙
- `build_ticker_centric_chain` (backend) / `buildTickerCentricChain` (frontend): 동일 로직
- 다른 `company` ticker(예: 005930 삼성전자)는 오염 chain에서 제거
- layout/propagation BFS 루트 = center entity (`is_center`)
- 링크 없을 때만 `referenced_chunks` / retrieval `chunks`로 최소 graph 생성

## 검증 (`scripts/verify_ticker_centric_chain.py`)
- 오염 sample(삼성전자 005930) chain 입력 시:
  - 삼성전기 009150 → center `삼성전기/009150`, 삼성전자 노드 없음
  - 현대자동차 005380 → center `현대자동차/005380`, 삼성전자 노드 없음

## 연동
- API: `GET /api/stock-chain/{trace_id}` → `center_name`, `center_ticker`, filtered `chain`
- UI: Event Graph (`use-event-graph` + retrieval chunks), Stock Chain viewer 중심 배지
