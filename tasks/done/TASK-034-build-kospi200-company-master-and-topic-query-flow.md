# TASK-034-build-kospi200-company-master-and-topic-query-flow.md

# TASK-034 KOSPI200 Company Master & Topic Query Flow 구축

## 상태

DONE

---

# 목표

현재 검색 구조의:

```text
삼성전기 → 삼성전자 오매칭
부분 문자열 검색 충돌
검색어 기반 종목 혼동
불안정한 resolver
```

문제를 해결하기 위해:

```text
KOSPI200 종목 마스터 기반 선택 구조
+
종목 선택과 분석 키워드 분리
```

방식으로 Query Flow를 재구성한다.

현재 TASK의 목표는:

```text
사용자가 명확하게 종목을 선택하고,
시스템은 확정된 ticker 기준으로
retrieval/reasoning/dashboard를 수행
```

하는 안정적인 Runtime Query 구조를 구축하는 것이다.

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
→ Company Resolver
→ Dynamic Ingestion Pipeline
→ Cost Guard
→ Runtime Query Flow
```

현재 시스템은:

```text
검색어 기반 company resolver
```

를 사용하고 있다.

하지만 현재 구조는:

```text
삼성전기 → 삼성전자 오매칭
부분 문자열 충돌
query ambiguity
dashboard mismatch
```

문제가 존재한다.

현재 TASK에서는:

```text
종목 선택
+
주제 키워드 분석
```

구조로 전환한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- KOSPI200 Company Master 구축
- company master DB schema 구축
- ticker 기반 종목 선택 구조 구축
- company alias 구조 구축
- 종목 자동완성 UI 구축
- 종목 선택 Dropdown 구축
- topic keyword 입력 구조 구축
- 종목 선택과 keyword 입력 분리
- selectedTicker 기반 Runtime Flow 구축
- 뉴스 검색 query builder 구축
- ticker + company + keyword 조합 검색 구축
- Dashboard selectedTicker 상태 관리 구축
- selectedTicker 기반 query execution 구축
- 종목 변경 시 runtime refresh 구축
- 검색 정확도 개선
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
- 실시간 Streaming
- 분산 MLOps
- Multi-user SaaS
- Kubernetes

현재 TASK는:

```text
안정적인 검색 구조
```

만 구축한다.

---

# 현재 문제

현재 문제 예시:

```text
삼성전기 검색
↓

삼성전자 retrieval 발생
```

원인:

```text
부분 문자열 기반 resolver
```

문제.

---

# 목표 Query 구조

현재 목표 구조:

```text
[종목 선택]
삼성전기 009150

[분석 키워드]
MLCC 전장부품 반도체

↓

Runtime Query 생성

↓

ticker:
009150

company:
삼성전기

keywords:
MLCC 전장부품 반도체
```

---

# 생성 대상 구조

```text
src/company_master/
├─ kospi200_loader.py
├─ company_master_repository.py
├─ company_search_service.py
├─ ticker_selection_service.py
└─ query_builder.py
```

```text
dashboard-ui/src/components/
├─ company-selector/
│  ├─ CompanySearchInput.tsx
│  ├─ CompanyDropdown.tsx
│  ├─ TopicKeywordInput.tsx
│  ├─ SelectedCompanyCard.tsx
│  └─ QueryExecutionPanel.tsx
```

---

# Company Master 역할

현재 역할:

- KOSPI200 종목 관리
- ticker 관리
- corp_code 관리
- alias 관리
- 검색 정확도 개선

---

# Topic Query 역할

현재 역할:

- 분석 주제 입력
- retrieval relevance 강화
- 뉴스 검색 품질 개선

---

# Query Builder 역할

현재 역할:

- ticker/company/topic 조합 query 생성

예상 생성:

```text
삼성전기 MLCC
삼성전기 전장부품
009150 실적
삼성전기 반도체
```

---

# KOSPI200 DB 목표

현재 목표:

```text
KOSPI200 종목 전체 저장
```

예상 컬럼:

```sql
company_name
ticker
market
corp_code
sector
industry
aliases
```

---

# 검색 UX 목표

현재 목표:

```text
검색어 입력
↓

자동완성 Dropdown

↓

종목 선택 확정
```

예상 UX:

```text
삼성 입력

↓

삼성전자 005930
삼성전기 009150
삼성SDI 006400
```

사용자 선택 기반 진행.

---

# Runtime Flow 목표

현재 목표:

```text
selectedTicker
+
topicKeyword
```

기준 Runtime 실행.

예상 흐름:

```text
selectedTicker:
009150

↓

topic:
MLCC 전장부품

↓

retrieval query 생성

↓

runtime retrieval

↓

dashboard rendering
```

---

# Dashboard 상태 목표

현재 목표:

```text
모든 패널이
selectedTicker 기준 동작
```

예상 상태:

```text
Signal
News
Event Graph
Memory
Evaluation
```

모두 동일 ticker 기준.

---

# 검색 정확도 목표

현재 목표:

```text
정확 일치 우선
ticker 우선
선택 기반 확정
```

현재 제거 대상:

```text
부분 문자열 fallback
```

---

# API 연동 대상

현재 API 대상:

```text
GET /api/company/search?q=
GET /api/company/{ticker}
POST /api/query/run
```

---

# API 응답 예시

```json
[
  {
    "company_name": "삼성전기",
    "ticker": "009150",
    "sector": "전자부품"
  }
]
```

---

# Query 실행 예시

```json
{
  "ticker": "009150",
  "company": "삼성전기",
  "keywords": [
    "MLCC",
    "전장부품",
    "반도체"
  ]
}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Runtime Flow 재사용
- 기존 Retrieval 구조 재사용
- 기존 Dashboard UI 재사용
- selectedTicker 기반 상태 유지
- explainability 유지
- OpenAI 호출 최소화 유지
- 발표 가능한 UX 유지
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## kospi200_loader.py

역할:

- KOSPI200 종목 로딩

예상 기능:

```text
load_kospi200_companies()
```

---

## company_search_service.py

역할:

- 종목 검색

예상 기능:

```text
search_companies()
autocomplete_companies()
```

---

## ticker_selection_service.py

역할:

- ticker 확정

예상 기능:

```text
select_company_ticker()
```

---

## query_builder.py

역할:

- retrieval query 생성

예상 기능:

```text
build_news_queries()
build_retrieval_queries()
```

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 발표 가능한 종목 선택 UX
- 안정적인 Runtime Query
- ticker 기반 정확한 Retrieval
- Dashboard 일관성 확보
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Company Master 검증

- KOSPI200 저장 여부
- ticker 조회 여부
- alias 조회 여부

---

## 검색 검증

- 자동완성 동작 여부
- 삼성전기/삼성전자 분리 여부
- ticker 선택 정상 여부

---

## Query 검증

- ticker 기반 retrieval 여부
- keyword 기반 retrieval 여부
- query builder 정상 여부

---

## Dashboard 검증

- selectedTicker 상태 유지 여부
- 종목 변경 시 dashboard 변경 여부

---

## Runtime 검증

- selectedTicker 기반 runtime 실행 여부
- topic keyword 기반 retrieval 여부

---

## 구조 검증

- 기존 Runtime 구조 유지 여부
- 기존 Retrieval 구조 유지 여부
- TASK 범위 외 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-034/
```

---

# 관련 Logs

```text
logs/TASK-034/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- KOSPI200 Company Master 구축 성공
- ticker 기반 종목 선택 성공
- topic keyword 분리 성공
- query builder 구축 성공
- 검색 정확도 개선 성공
- 삼성전기/삼성전자 분리 성공
- selectedTicker 기반 Runtime 성공
- Dashboard ticker 일관성 확보 성공
- 발표 가능한 종목 검색 UX 확보 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-035-connect-dashboard-panels-to-runtime-trace
- TASK-036-build-portfolio-backtesting-suite
- TASK-037-build-presentation-demo-scenario

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- ticker 기반 정확성 우선
- Runtime Query 안정성 우선
- End-to-End traceability 유지
- 발표 가능한 UX 유지
- OpenAI 비용 안정성 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지