# AlphaFin LTE Dashboard UI

Financial AI Engine 내부 흐름을 시각화하는 발표용 Dashboard (Next.js 15).

## 기술 스택

- Next.js 15 · TypeScript · Tailwind CSS
- shadcn/ui 스타일 컴포넌트
- Recharts (Evaluation Score Chart)

## 사전 요구

1. **Backend API** 실행 (포트 8000)

```bash
# 프로젝트 루트
uvicorn src.dashboard_api.app:app --host 0.0.0.0 --port 8000
```

2. Node.js 18+ 및 npm

## 설치 및 실행

```bash
cd dashboard-ui
cp .env.local.example .env.local
npm install
npm run dev
```

접속:

- Overview Dashboard: http://localhost:3000
- Retrieval & Analysis Viewer: http://localhost:3000/analysis
- Event Graph Visualization: http://localhost:3000/event-graph

## API 연동

`.env.local`:

```text
NEXT_PUBLIC_API_URL=http://localhost:8000
```

연동 엔드포인트:

- `GET /api/retrieval/latest`
- `GET /api/reflection/latest`
- `GET /api/memory/latest`
- `GET /api/stock-chain/latest`
- `GET /api/trace/latest`
- `GET /api/evaluation/latest`

`trace_id` 입력 시 retrieval / reflection / trace / evaluation은 해당 ID로 조회합니다.

## 발표 데모

1. Backend API 실행
2. `npm run dev` 실행
3. Dashboard에서 **Load Dashboard** 또는 **Latest Trace** 클릭
4. Retrieval → Reflection → Memory → Stock Chain → Trace → Evaluation 순서로 확인

## ngrok (선택)

```bash
ngrok http 3000
```

Backend도 별도 터널 또는 동일 머신에서 CORS `*` 로 연동 가능합니다.
