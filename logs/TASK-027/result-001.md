# TASK-027 Result-001

## 실행 일시

2026-05-27

## 실행 결과

### 구현 컴포넌트

| 파일 | 역할 |
|------|------|
| EventGraph.tsx | React Flow 메인 · zoom/pan · minimap |
| GraphNode.tsx | entity type별 노드 · hover/click highlight |
| GraphEdge.tsx | relation tooltip · impact score label |
| GraphLegend.tsx | node type 색상 범례 |
| GraphToolbar.tsx | filter · search · highlight presets |
| NodeDetailPanel.tsx | 클릭 노드 상세 |
| PropagationPanel.tsx | propagation flow + temporal relations |

### 페이지

- `src/app/event-graph/page.tsx`
- Overview / Analysis nav에서 Event Graph 링크

### API 연동

| API | 용도 |
|-----|------|
| GET /api/stock-chain/latest | entities, links |
| GET /api/trace/latest | completed_at → temporal |

### 기능 검증

| 항목 | 결과 |
|------|------|
| node rendering | OK |
| edge rendering + impact badge | OK |
| propagation visualization | OK |
| node detail panel | OK |
| graph filtering | OK |
| entity highlighting | OK |
| temporal relation panel | OK |
| npm run build | OK |
| TASK-026 done | OK |

### 샘플 Graph

- NVIDIA → GPU → AI 서버 → HBM → 삼성전자
- HBM → DRAM → dram price
- impact 0.72–0.88 구간 표시

### 최종 결과

**OK**

---

## 추가 작업 — Dashboard Query Flow 수정 (2026-05-27)

TASK-027 연장선으로 Dashboard의 `latest` 의존을 제거하고
`query → trace_id` 기반 흐름으로 수정.

### 변경 내용

#### 백엔드
| 파일 | 변경 |
|------|------|
| `src/dashboard_api/routes/engine.py` | 신규: `POST /api/engine/run` |
| `src/dashboard_api/routes/memory.py` | 추가: `GET /api/memory/{trace_id}` |
| `src/dashboard_api/routes/stock_chain.py` | 추가: `GET /api/stock-chain/{trace_id}` |
| `src/dashboard_api/services/memory_service.py` | `fetch_memory_by_trace()` 추가 |
| `src/dashboard_api/services/stock_chain_service.py` | `fetch_stock_chain_by_trace()` 추가 |
| `src/dashboard_api/app.py` | engine 라우터 등록 |

#### 프론트엔드
| 파일 | 변경 |
|------|------|
| `dashboard-ui/src/services/api.ts` | `runEngine()` 추가, `getMemory`/`getStockChain` trace_id 기반 전환 |
| `dashboard-ui/src/hooks/use-dashboard-data.ts` | `runAndLoad()`, `engineRunning` 추가 |
| `dashboard-ui/src/components/query/query-input-panel.tsx` | Run Engine 버튼, ticker 자동 추론 |
| `dashboard-ui/src/components/dashboard-client.tsx` | runAndLoad 연결 |

### 검증
- `npm run build`: 성공 (타입 에러 0)
- `run_sample.py`: 모든 /api/*/latest 200 OK
- latest API 의존 제거 (getMemory, getStockChain 포함) 완료
