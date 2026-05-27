# TASK-025 Result-001

## 실행 일시

2026-05-27

## 실행 결과

### 구현 구조

```text
dashboard-ui/
├─ src/app/          # layout, page, globals (dark theme)
├─ src/components/   # retrieval, reflection, memory, stock-chain, trace, evaluation, query
├─ src/services/api.ts
├─ src/hooks/use-dashboard-data.ts
├─ src/types/dashboard.ts
└─ README.md
```

### Viewer 구현

| 컴포넌트 | 역할 |
|----------|------|
| QueryInputPanel | 질문 입력 · Load Dashboard · Latest Trace · trace_id |
| RetrievalViewer | chunk · similarity score · document_type |
| ReflectionViewer | summary · missing_risks · overconfidence |
| MemoryTimelineViewer | short/mid/long layer · temporal evolution |
| StockChainViewer | propagation graph (vertical chain) |
| EngineTraceViewer | pipeline_flow · trace steps |
| EvaluationScorePanel | overall_score · Recharts bar chart · hallucination |

### API 연동

| 엔드포인트 | 용도 |
|------------|------|
| GET /api/retrieval/latest | Retrieval Viewer |
| GET /api/reflection/latest | Reflection Viewer |
| GET /api/memory/latest | Memory Timeline |
| GET /api/stock-chain/latest | Stock Chain |
| GET /api/trace/latest | Engine Trace |
| GET /api/evaluation/latest | Evaluation Panel |

trace_id 입력 시 retrieval/reflection/trace/evaluation은 `/{trace_id}` 경로 사용.

### 검증 항목

| 항목 | 결과 |
|------|------|
| dashboard-ui 프로젝트 생성 | OK |
| Next.js 15 + TS + Tailwind | OK |
| shadcn/ui 스타일 컴포넌트 | OK |
| API service + hook | OK |
| loading / error UI | OK |
| 다크 테마 | OK |
| Recharts score chart | OK |
| TASK-024 done 확인 | OK |

### 로컬 실행 (사용자 환경)

```bash
# Terminal 1 — Backend
uvicorn src.dashboard_api.app:app --host 0.0.0.0 --port 8000

# Terminal 2 — Frontend
cd dashboard-ui
npm install
npm run dev
```

접속: http://localhost:3000

### 비고

- 샘플 검증 시 Node/npm PATH 필요 (Cursor 내장 node만 있는 환경에서는 사용자 로컬 Node 설치 후 `npm install` 실행)
- 엔진 실행은 UI에서 트리거하지 않음 — Unified Engine 실행 후 Dashboard에서 latest 조회
- 발표 데모: Load Dashboard → 6개 패널 동시 갱신

### 최종 결과

**OK** — Dashboard UI 초기 구현 완료
