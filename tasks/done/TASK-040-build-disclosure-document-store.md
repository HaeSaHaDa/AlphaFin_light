# TASK-040-build-disclosure-document-store.md

# TASK-040 Disclosure Document Store 구축

## 상태

DONE

---

# 목표

현재 시스템은:

```text
뉴스 중심 retrieval
```

비중이 높으며,

금융 분석에서 핵심이 되는:

```text
공시자료
사업보고서
분기보고서
실적발표
IR 자료
```

가 Runtime Memory 및 Retrieval Flow에 충분히 통합되지 않았다.

현재 TASK의 목표는:

```text
Disclosure Document Store
```

를 구축하여:

```text
공시자료 기반 금융 AI Runtime
```

을 강화하는 것이다.

현재 단계에서는:

```text
뉴스 기반 분석
```

보다:

```text
공시 기반 신뢰도
기업 공식 문서 기반 reasoning
실적/사업 구조 기반 retrieval
```

강화에 집중한다.

---

# 배경

현재 프로젝트는 다음 흐름까지 구축 완료되었다.

```text
수집
→ 저장
→ Chunking
→ Embedding
→ Semantic Retrieval
→ Financial Analysis
→ Reflection
→ Layered Memory
→ Temporal Market Memory
→ Stock Chain
→ Signal Evaluation
→ Explainable Dashboard
→ Runtime Query Flow
→ KOSPI200 Company Master
→ Dashboard Runtime Binding
→ Runtime Audit
→ Market Relationship Graph
→ Market Relation Reasoning
→ Persistent Runtime Shell
```

현재 시스템은:

```text
뉴스 retrieval
```

비중이 높고,

공식 기업 문서 기반:

```text
실적
공시
사업 구조
리스크
CAPEX
투자 계획
```

분석이 부족하다.

현재 TASK에서는:

```text
공시 문서 저장소
+
공시 기반 retrieval
```

를 구축한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Disclosure Document Store 구축
- OpenDART 공시 수집 구조 구축
- disclosure_documents 테이블 구축
- disclosure_chunks 테이블 구축
- disclosure_embeddings 구축
- 공시 chunking 구축
- 공시 embedding 구축
- 공시 metadata 저장 구축
- 사업보고서 저장 구축
- 분기보고서 저장 구축
- 실적발표 저장 구축
- 주요사항보고서 저장 구축
- IR 자료 저장 구조 구축
- source_type 구분 구축
- disclosure retrieval 구축
- disclosure semantic search 구축
- selectedTicker 기반 disclosure retrieval 구축
- disclosure summary 구축
- disclosure evidence 구축
- Dashboard Disclosure Panel 구축
- Disclosure Viewer 구축
- Disclosure Timeline 구축
- disclosure source filtering 구축
- disclosure ingestion cache 구축
- Runtime disclosure integration 구축
- Market reasoning에 disclosure evidence 연결
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 신규 AI 모델 추가
- 신규 Retrieval 알고리즘 추가
- Broker API
- Auto Trading
- HTS 기능
- Real-time Streaming
- OCR 파이프라인
- PDF layout reconstruction
- SEC EDGAR 전체 연동
- Kubernetes
- Multi-user SaaS

현재 TASK는:

```text
공시 저장소
+
공시 retrieval
```

만 구축한다.

---

# 현재 문제

현재 문제:

```text
뉴스 중심 분석
```

비중이 너무 높음.

현재 부족 영역:

```text
- 공식 기업 자료 부족
- 실적 기반 reasoning 부족
- 사업 구조 기반 reasoning 부족
- 기업 리스크 기반 reasoning 부족
```

현재 UI 문제:

```text
공시자료 전용 영역 없음
```

---

# 목표 구조

현재 목표 구조:

```text
OpenDART
```

↓

수집:

```text
사업보고서
분기보고서
실적발표
주요사항보고서
```

↓

저장:

```text
disclosure_documents
disclosure_chunks
disclosure_embeddings
```

↓

활용:

```text
retrieval
market reasoning
risk analysis
memory
dashboard
```

---

# 생성 대상 구조

```text
src/disclosure/
├─ dart_collector.py
├─ disclosure_repository.py
├─ disclosure_chunker.py
├─ disclosure_embedder.py
├─ disclosure_retriever.py
├─ disclosure_summary.py
├─ disclosure_cache.py
└─ disclosure_query_builder.py
```

```text
dashboard-ui/src/components/disclosure/
├─ DisclosurePanel.tsx
├─ DisclosureViewer.tsx
├─ DisclosureTimeline.tsx
├─ DisclosureSummaryCard.tsx
├─ DisclosureFilterBar.tsx
└─ DisclosureEvidencePanel.tsx
```

---

# DB 목표

현재 목표 테이블:

```sql
disclosure_documents
disclosure_chunks
disclosure_embeddings
disclosure_events
```

---

# disclosure_documents 목표

예상 컬럼:

```sql
document_id
ticker
corp_code
company_name
report_name
report_type
report_date
source_type
document_url
summary
raw_text
created_at
```

---

# disclosure_chunks 목표

예상 컬럼:

```sql
chunk_id
document_id
chunk_index
chunk_text
section_name
importance_score
```

---

# disclosure_embeddings 목표

예상 컬럼:

```sql
embedding_id
chunk_id
embedding_vector
embedding_model
created_at
```

---

# source_type 목표

현재 목표:

| source_type | 의미 |
|---|---|
| BUSINESS_REPORT | 사업보고서 |
| QUARTER_REPORT | 분기보고서 |
| EARNINGS | 실적발표 |
| MAJOR_ISSUE | 주요사항 |
| IR | IR 자료 |

---

# Disclosure Retrieval 목표

현재 목표:

```text
selectedTicker 기반
공시 semantic retrieval
```

예상 흐름:

```text
삼성전기
↓

MLCC 투자

↓

사업보고서 chunk retrieval

↓

CAPEX 관련 reasoning
```

---

# Market Reasoning 목표

현재 목표:

```text
뉴스 기반 reasoning
+
공시 기반 reasoning
```

통합.

---

# Disclosure Timeline 목표

현재 목표:

```text
기업 공시 흐름 시각화
```

예상:

```text
2025-01:
CAPEX 확대

2025-02:
실적 개선

2025-03:
전장부품 투자 발표
```

---

# Disclosure Evidence 목표

현재 목표:

```text
AI reasoning 근거로
공시자료 연결
```

예상:

```text
"사업보고서 기준 MLCC 생산능력 확대"
```

---

# Dashboard 목표

현재 목표:

```text
뉴스와 공시 구분 표시
```

예상 구조:

```text
News
Disclosure
Memory
Graph
Evaluation
```

---

# Runtime Integration 목표

현재 목표:

```text
disclosure retrieval
→ Runtime reasoning
→ Memory
→ Signal evaluation
```

통합.

---

# API 연동 대상

현재 API 대상:

```text
POST /api/disclosure/collect
GET /api/disclosure/{ticker}
GET /api/disclosure/search
GET /api/disclosure/timeline/{ticker}
GET /api/disclosure/evidence/{traceId}
```

---

# Disclosure Payload 예시

```json
{
  "ticker": "009150",
  "company": "삼성전기",
  "report_type": "BUSINESS_REPORT",
  "summary": "MLCC 생산능력 확대",
  "evidence": [],
  "report_date": "2025-01-20"
}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- selectedTicker 중심 유지
- traceId 기반 유지
- Runtime payload 기반 유지
- explainability 유지
- official document 기반 유지
- 기존 Runtime Flow 유지
- 기존 Retrieval 구조 유지
- OpenAI 호출 최소화 유지
- 발표 가능한 UX 유지
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## dart_collector.py

역할:

- OpenDART 공시 수집

예상 기능:

```text
collect_disclosures()
```

---

## disclosure_chunker.py

역할:

- 공시 chunking

예상 기능:

```text
chunk_disclosure_document()
```

---

## disclosure_retriever.py

역할:

- 공시 semantic retrieval

예상 기능:

```text
retrieve_disclosure_chunks()
```

---

## disclosure_summary.py

역할:

- 공시 요약 생성

예상 기능:

```text
summarize_disclosure()
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 공식 기업 자료 기반 분석 강화
- Explainable Disclosure Reasoning
- 공시 기반 신뢰도 강화
- 발표 가능한 기업 분석 플랫폼 강화
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Disclosure 검증

- 공시 저장 여부
- 공시 chunking 여부
- 공시 embedding 여부

---

## Retrieval 검증

- 공시 semantic retrieval 여부
- selectedTicker 기반 retrieval 여부

---

## Dashboard 검증

- Disclosure Panel 표시 여부
- 뉴스/공시 분리 여부

---

## Runtime 검증

- Runtime reasoning 연결 여부
- disclosure evidence 연결 여부

---

## Timeline 검증

- 공시 timeline 정상 여부
- report_type 분리 여부

---

## UX 검증

- 사용자 이해 가능 여부
- 공식 문서 기반 신뢰도 확보 여부

---

# 관련 Prompt

```text
prompts/TASK-040/
```

---

# 관련 Logs

```text
logs/TASK-040/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Disclosure Document Store 구축 성공
- OpenDART 공시 저장 성공
- disclosure retrieval 구축 성공
- disclosure semantic search 구축 성공
- Runtime disclosure integration 성공
- Disclosure Panel 구축 성공
- 공시 기반 reasoning 강화 성공
- 발표 가능한 Disclosure Intelligence 확보 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-041-build-event-consolidation-and-memory-deduplication
- TASK-042-build-portfolio-backtesting-suite
- TASK-043-build-backtesting-visualization

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- official document 기반 강화
- Runtime consistency 유지
- selectedTicker 중심 유지
- 발표 가능한 UX 유지
- OpenAI 비용 안정성 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지