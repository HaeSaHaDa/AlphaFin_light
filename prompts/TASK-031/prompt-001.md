# TASK-031 Prompt-001

## 작업

TASK-031-build-company-resolver-and-ingestion-pipeline

## 목표

회사명 입력 → ticker/corp_code 자동 식별 → 수집·chunk·embedding → retrieval 가능 → Engine 분석.

## 구현

- `src/company_resolver/` (registry, alias, resolver)
- `src/ingestion_pipeline/` (news, dart, price, chunk, embedding, runner)
- `POST /api/ingestion/run`, `GET /api/company/search?q=`
- Engine `/api/engine/run` 에 ingestion 자동 연동
- Dashboard `Run Engine` 시 회사명만 입력 (ticker 하드코딩 제거)

## 제외

실시간 전체 시장 ingestion, Broker API, 자동 매매
