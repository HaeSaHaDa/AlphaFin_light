# TASK-032 Result

## 완료 항목

- `src/cost_guard/` 6모듈 + `limits.py`
- `embedding_pipeline.py` — hash cache, budget guard, presentation/dry-run skip
- `ingestion_runner.py` — `--dry-run`, cache 재사용
- API: `GET /api/cost/today`, `GET /api/cache/status`, `POST /api/presentation-mode/enable|disable`
- Dashboard UI: `dashboard-ui/src/styles/*.css`, `layout.tsx` body/dark shell

## 검증

- `python -m src.ingestion_pipeline.ingestion_runner "현대자동차" --dry-run`
- `npm run build` (dashboard-ui)
- API smoke: cost/cache/presentation endpoints
