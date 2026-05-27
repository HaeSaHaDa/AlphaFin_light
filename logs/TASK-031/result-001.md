# TASK-031 Result-001

## 실행 일시

2026-05-27

## 실행 결과

### Company Resolver (`src/company_resolver/`)

| 모듈 | 역할 |
|------|------|
| company_registry.py | 삼성/현대/SK하이닉스/LG엔솔/NAVER/카카오 + corp_code |
| alias_resolver.py | 부분 검색 |
| company_resolver.py | 질문 텍스트 → ticker |

검증: `현대자동차` → 005380, `삼성` → 005930, `SK` → 000660

### Ingestion Pipeline (`src/ingestion_pipeline/`)

| 모듈 | 역할 |
|------|------|
| news_ingestor.py | 네이버 뉴스 → news_articles |
| dart_ingestor.py | OpenDART → dart_disclosures |
| price_ingestor.py | pykrx → stock_prices |
| chunk_pipeline.py | document_chunks |
| embedding_pipeline.py | document_embeddings (중복 INSERT IGNORE) |
| vector_index_manager.py | cache · ingestion 로그 |
| ingestion_runner.py | 오케스트레이션 · CLI |

### API

| 엔드포인트 | 결과 |
|-----------|------|
| GET /api/company/search?q=현대 | 200 OK |
| POST /api/ingestion/run | 구현 완료 |
| POST /api/engine/run | ingestion 자동 연동 |

### Dashboard

- `runEngine(query)` — ticker 하드코딩 제거
- `QueryInputPanel` — 회사명만 입력, "수집·분석 중…" 표시
- Engine 실행 시 `resolve_company` + `run_ingestion_for_company` 후 분석

### 기타 수정

- `engine.py` PROJECT_ROOT `parents[3]` (기존 버그 수정 유지)

### 검증

| 항목 | 결과 |
|------|------|
| Company Resolver | OK |
| npm run build | OK |
| TASK-030 done | OK (이전 완료) |
| TASK-031 → done | OK |

### 실행 예시

```bash
# ingestion only
python -m src.ingestion_pipeline.ingestion_runner "현대자동차"

# API
POST /api/ingestion/run  {"company": "현대자동차"}
GET  /api/company/search?q=현대
```

### 주의

- 첫 ingestion은 뉴스 크롤·OpenAI embedding API 필요 (수 분 소요 가능)
- 완료 종목은 `data/ingestion_cache/{ticker}.json` 으로 재사용
- OPENAI_API_KEY · DART_API_KEY 필요

### 최종 결과

**OK**
