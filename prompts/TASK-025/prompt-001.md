# TASK-025 Prompt-001

## 작업

TASK-025-build-dashboard-ui

## 목표

Financial AI Engine 내부 흐름을 발표용 Dashboard UI로 시각화

## 수행 내용

- TASK-024 완료 확인 (tasks/done/)
- prompts/TASK-025/, logs/TASK-025/ 생성
- dashboard-ui/ Next.js 15 + TypeScript + Tailwind + shadcn/ui
- Retrieval / Reflection / Memory Timeline / Stock Chain / Trace / Evaluation Viewer
- Query Input Panel · trace_id 조회
- FastAPI Backend API 연동 (NEXT_PUBLIC_API_URL)
- 다크 테마 · loading/error 상태 · Recharts score chart

## 환경

- Node.js 18+ · npm
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## 실행

```bash
uvicorn src.dashboard_api.app:app --host 0.0.0.0 --port 8000
cd dashboard-ui && npm install && npm run dev
```

## 제외 범위

- Auth · WebSocket · 실시간 거래 · TradingView · K8s 금지
