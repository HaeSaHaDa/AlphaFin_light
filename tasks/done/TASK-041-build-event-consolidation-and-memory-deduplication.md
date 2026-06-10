# TASK-041-build-event-consolidation-and-memory-deduplication.md

# TASK-041 Event Consolidation & Memory Deduplication 구축

## 상태

DONE

---

# 목표

현재 시스템에서 발생하는:

```text
같은 뉴스 반복 표시
동일 이벤트의 여러 confidence score
뉴스/공시 중복 근거
단기/중기/장기 메모리 중복 저장
중기 승격 후 단기 메모리에 잔존
```

문제를 해결한다.

현재 TASK의 목표는 뉴스와 공시를 개별 문서 단위로만 다루는 것이 아니라:

```text
시장 이벤트 단위
```

로 통합하여:

```text
중복 없는 뉴스/공시 표시
event-level confidence 산출
short/mid/long memory layer 정합성 유지
```

를 구현하는 것이다.

---

# 배경

현재 프로젝트는 다음 흐름까지 구축 완료되었다.

```text
뉴스 수집
→ 공시 수집
→ Chunking
→ Embedding
→ Retrieval
→ Financial Analysis
→ Market Graph
→ Memory Timeline
→ Signal Evaluation
→ Disclosure Store
→ Persistent Runtime Shell
```

하지만 현재는 retrieval 결과와 memory 결과가 chunk/document 단위로 쌓이면서:

```text
동일 뉴스 반복
동일 공시 반복
동일 이벤트 다중 표시
memory layer 간 중복
```

문제가 발생한다.

현재 TASK에서는:

```text
문서 중심
→ 이벤트 중심
```

으로 정제 계층을 추가한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Event Consolidation Layer 구축
- News Deduplication 구축
- Disclosure Deduplication 구축
- News-Disclosure Event Linking 구축
- Canonical Event 생성
- Event Similarity 계산
- Event-Level Confidence 계산
- Event-Level Importance 계산
- Memory Layer Deduplication 구축
- Short/Mid/Long Memory 이동 정합성 구축
- Promotion 시 기존 Layer 제거 처리
- Duplicate Event Filtering 구축
- Dashboard 중복 표시 제거
- Event Timeline 정리
- Memory Timeline 정리
- Retrieval 결과 중복 제거
- Disclosure Evidence 중복 제거
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 신규 AI 모델 추가
- 신규 Retrieval 알고리즘 추가
- Backtesting
- Auto Trading
- Broker API
- HTS 기능
- Real-time Streaming
- Multi-agent Memory
- 장기 자율 학습
- Kubernetes
- Multi-user SaaS

현재 TASK는:

```text
Event 정제
+
Memory 중복 제거
```

만 수행한다.

---

# 현재 문제

현재 문제 예시:

```text
뉴스 A score 0.91
뉴스 A score 0.52
뉴스 A 유사 제목 score 0.76
```

또는:

```text
단기 기억:
MLCC 투자 확대

중기 기억:
MLCC 투자 확대
```

문제 원인:

```text
chunk/document 단위 저장
event_id 기준 통합 부족
memory layer 간 unique constraint 부족
promotion 시 기존 layer 제거 없음
```

---

# 목표 구조

현재 목표 구조:

```text
뉴스/공시/Chunk
```

↓

```text
Event Consolidation
```

↓

```text
Canonical Market Event
```

↓

```text
Event-Level Confidence
```

↓

```text
Memory Layer Assignment
```

↓

```text
Dashboard Rendering
```

---

# 생성 대상 구조

```text
src/event_consolidation/
├─ event_consolidator.py
├─ news_deduplicator.py
├─ disclosure_deduplicator.py
├─ event_similarity.py
├─ canonical_event_builder.py
├─ event_confidence.py
├─ event_importance.py
├─ event_memory_manager.py
└─ event_repository.py
```

```text
dashboard-ui/src/components/events/
├─ EventSummaryPanel.tsx
├─ CanonicalEventCard.tsx
├─ EventEvidenceList.tsx
├─ EventConfidenceBadge.tsx
└─ EventTimeline.tsx
```

---

# DB 목표

필요 시 다음 테이블 또는 기존 테이블 확장:

```sql
market_events
event_evidence
event_memory_layers
```

---

# market_events 목표 컬럼

```sql
event_id
ticker
company_name
canonical_title
event_summary
event_type
event_date
confidence_score
importance_score
impact_direction
created_at
updated_at
```

---

# event_evidence 목표 컬럼

```sql
evidence_id
event_id
source_type
source_id
title
url
published_at
relevance_score
created_at
```

source_type 예시:

```text
NEWS
DISCLOSURE
CHUNK
MEMORY
```

---

# event_memory_layers 목표 컬럼

```sql
event_id
memory_layer
entered_at
promoted_from
importance_score
is_active
```

memory_layer:

```text
SHORT
MID
LONG
```

---

# Deduplication 목표

중복 판단 기준:

```text
title similarity
body similarity
ticker
published_at proximity
source overlap
semantic similarity
```

---

# Canonical Event 예시

입력:

```text
뉴스: 삼성전기 MLCC 증설 추진
뉴스: 삼성전기 전장용 MLCC 투자 확대
공시: MLCC 생산능력 확대 관련 투자
```

출력:

```text
canonical_event:
삼성전기 MLCC 생산능력 확대
```

---

# Event-Level Confidence 목표

기존 문제:

```text
같은 뉴스인데 score 0.52 / 0.91로 반복
```

개선:

```text
event confidence: 0.84
```

산출 기준:

```text
retrieval relevance
source reliability
evidence count
recency
disclosure presence
```

---

# Memory Deduplication 목표

현재 목표:

```text
동일 event_id는 하나의 active memory layer에만 존재
```

예:

```text
SHORT → MID 승격
```

시:

```text
SHORT inactive
MID active
```

---

# Promotion 규칙

```text
short memory
↓

importance 유지
↓

mid memory promotion

↓

short memory inactive 처리
```

---

# Dashboard 목표

현재 목표:

```text
중복 뉴스 제거
중복 공시 제거
event 단위 표시
memory layer 중복 제거
```

---

# API 연동 대상

```text
GET /api/events/{traceId}
GET /api/events/ticker/{ticker}
GET /api/events/{eventId}/evidence
GET /api/memory/events/{traceId}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- selectedTicker 중심 유지
- traceId 기반 유지
- Runtime payload 기반 유지
- 뉴스/공시 source 구분 유지
- event_id 기반 중복 제거
- memory layer unique 유지
- OpenAI 호출 최소화 유지
- embedding cache 재사용
- 발표 가능한 UX 유지
- 과도한 abstraction 금지

---

# 예상 기능

## event_consolidator.py

역할:

```text
뉴스/공시/Chunk를 event 단위로 통합
```

예상 기능:

```text
consolidate_events()
```

---

## news_deduplicator.py

역할:

```text
중복 뉴스 제거
```

예상 기능:

```text
deduplicate_news()
```

---

## disclosure_deduplicator.py

역할:

```text
중복 공시 제거
```

예상 기능:

```text
deduplicate_disclosures()
```

---

## event_memory_manager.py

역할:

```text
event_id 기반 memory layer 관리
```

예상 기능:

```text
promote_event_memory()
deactivate_previous_layer()
```

---

# 검증 항목

현재 TASK 완료 전 다음 항목을 반드시 검증한다.

## Dedup 검증

- 동일 뉴스 중복 제거 여부
- 유사 제목 뉴스 통합 여부
- 공시 중복 제거 여부

---

## Event 검증

- canonical event 생성 여부
- event evidence 연결 여부
- event confidence 산출 여부

---

## Memory 검증

- 동일 event가 short/mid에 동시에 active로 존재하지 않는지
- promotion 시 이전 layer inactive 처리 여부
- memory timeline 중복 제거 여부

---

## Dashboard 검증

- 뉴스 반복 표시 제거 여부
- 공시 반복 표시 제거 여부
- event 단위 표시 여부

---

## Runtime 검증

- selectedTicker 기준 유지 여부
- traceId 기준 유지 여부
- 기존 Runtime Flow 유지 여부

---

# 관련 Prompt

```text
prompts/TASK-041/
```

---

# 관련 Logs

```text
logs/TASK-041/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Event Consolidation Layer 구축 성공
- News Deduplication 성공
- Disclosure Deduplication 성공
- Canonical Event 생성 성공
- Event-Level Confidence 산출 성공
- Memory Layer Deduplication 성공
- Promotion 시 기존 Layer 제거 성공
- Dashboard 중복 표시 제거 성공
- 발표 가능한 Event Timeline 확보 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후 다음 작업 후보:

- TASK-042-build-portfolio-backtesting-suite
- TASK-043-build-backtesting-visualization
- TASK-044-build-presentation-demo-scenario

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- Event-level reasoning 유지
- Runtime consistency 유지
- selectedTicker 중심 유지
- 공시/뉴스 source 구분 유지
- Memory lifecycle 정합성 유지
- OpenAI 비용 안정성 유지
- 과도한 Autonomous AI 구조 금지
