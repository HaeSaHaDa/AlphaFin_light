# AlphaFin LTE 저장 구조

## 문서 목적

현재 사용 중인 MariaDB와 파일 기반 저장소의 책임을 정의한다.

---

# 저장 구조 개요

```text
외부 데이터
→ MariaDB 원본/검색 데이터
→ data/ cache와 실행 산출물
→ trace 기반 Dashboard 조회
```

---

# MariaDB

연결:

```text
src/common/db/connection.py
```

기본 Schema:

```text
database/schema.sql
database/schema_company_master.sql
```

주요 테이블:

```text
companies
company_master
stock_prices
dart_disclosures
news_articles
document_chunks
document_embeddings
collection_logs
```

Disclosure Store:

```text
disclosure_documents
disclosure_chunks
disclosure_embeddings
disclosure_events
```

Event Store:

```text
market_events
event_evidence
event_memory_layers
```

---

# data 디렉토리

현재 주요 구조:

```text
data/
├─ raw/
├─ processed/
├─ chunks/
├─ embeddings/
├─ samples/
├─ ingestion_cache/
├─ ingestion_logs/
├─ disclosure_cache/
├─ cost_guard/
├─ memory/
├─ layered_memory/
├─ temporal_memory/
├─ reflection/
├─ event_graph/
├─ stock_chain/
├─ signal_evaluation/
└─ unified_engine/
```

## 원본 및 전처리

- `raw/`: 수집 원본
- `processed/`: 정제 데이터
- `chunks/`: 파일 기반 chunk 산출물
- `embeddings/`: embedding 관련 파일 산출물
- `samples/`: 검증 샘플

## Cache

- `ingestion_cache/`: ticker ingestion 상태
- `disclosure_cache/`: 공시 수집 상태
- `cost_guard/`: embedding hash와 사용량

## Memory 및 Graph

- `memory/`: analysis memory
- `layered_memory/`: SHORT/MID/LONG memory
- `temporal_memory/`: lifecycle와 promotion
- `reflection/`: reflection 기록
- `event_graph/`: ticker별 event graph
- `stock_chain/`: trace별 chain과 propagation log

## Runtime 결과

```text
data/unified_engine/
├─ final_results/
├─ traces/
└─ engine_runs/
```

파일명은 `trace_id`를 기준으로 한다.

---

# Prompt 및 작업 로그

```text
prompts/TASK-XXX/
logs/TASK-XXX/
```

- prompts: 실행 요청 기록
- logs: 결과, 검증, 이슈 기록

TASK-001부터 TASK-046까지 TASK 단위 대응 구조를 유지한다.

---

# 저장 원칙

- Raw 데이터와 Processed 데이터 분리
- MariaDB 연결 정보는 `.env` 사용
- ticker와 trace_id를 검색 및 결과 연결 기준으로 사용
- latest/sample fallback보다 명시적 trace 조회 우선
- 실행 검증이 실제 memory와 graph 파일을 갱신할 수 있음을 인지
- Schema 변경은 별도 TASK에서만 수행
