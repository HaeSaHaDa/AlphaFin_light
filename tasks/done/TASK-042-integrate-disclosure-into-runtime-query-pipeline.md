# TASK-042-integrate-disclosure-into-runtime-query-pipeline.md

# TASK-042 Disclosure Runtime Query Pipeline 통합

## 상태

DONE

---

# 목표

현재 시스템은:

```text
Dashboard Disclosure Panel
```

기준으로 공시를 수집·조회하고 있으나,

핵심 Runtime 흐름인:

```text
runQuery
→ retrieval
→ reasoning
→ signal evaluation
```

에 공시가 완전히 통합되어 있지는 않다.

현재 TASK의 목표는:

```text
뉴스 + 공시
```

를 Runtime Query Pipeline에 완전히 통합하여:

```text
검색 실행 시
공시가 항상 분석 컨텍스트에 포함되는 구조
```

를 구축하는 것이다.

---

# 배경

현재 시스템은:

```text
뉴스 retrieval 중심 Runtime
```

구조를 기반으로 발전해왔고,
TASK-040에서 Disclosure Store가 추가되었다.

하지만 현재 공시는:

```text
Disclosure Panel
Disclosure Viewer
Disclosure Evidence
```

영역 위주로 연결되어 있으며,

실제 핵심 분석 흐름인:

```text
runQuery
```

시점에서는:

```text
뉴스 retrieval 우선
```

구조가 유지되고 있다.

현재 TASK에서는:

```text
공시 retrieval
```

를 Runtime Query의 핵심 컨텍스트로 통합한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Runtime Query Pipeline에 disclosure retrieval 통합
- runQuery 실행 시 disclosure collect 연결
- selectedTicker 기반 disclosure retrieval 강제 연결
- 뉴스 + 공시 통합 retrieval 구축
- disclosure chunk retrieval 통합
- Runtime Context Assembler 구축
- disclosure evidence priority 적용
- disclosure-aware reasoning 구축
- disclosure-aware memory 구축
- disclosure-aware signal evaluation 구축
- disclosure-aware market graph 구축
- disclosure retrieval cache 구축
- disclosure retrieval ranking 구축
- disclosure retrieval timeout 보호 구축
- disclosure fallback handling 구축
- disclosure Runtime logging 구축
- Dashboard Runtime disclosure sync 구축
- canonical event evidence에 disclosure 연결
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
- SEC EDGAR 통합
- OCR 파이프라인
- Multi-agent orchestration
- Kubernetes
- Multi-user SaaS

현재 TASK는:

```text
Disclosure Runtime Integration
```

만 수행한다.

---

# 현재 문제

현재 구조:

```text
Dashboard 진입
↓

DisclosurePanel
↓

공시 collect 수행
```

문제:

```text
runQuery 시점에
공시가 반드시 retrieval에 포함되지 않음
```

즉 현재는:

```text
뉴스 기반 reasoning
+
부분적 disclosure evidence
```

상태.

---

# 목표 구조

현재 목표 흐름:

```text
사용자 검색
```

↓

```text
runQuery
```

↓

```text
뉴스 retrieval
+
공시 retrieval
```

↓

```text
Unified Runtime Context
```

↓

```text
analysis
signal evaluation
market reasoning
memory
graph
```

---

# 생성 대상 구조

```text
src/runtime_query/
├─ runtime_query_pipeline.py
├─ runtime_context_assembler.py
├─ disclosure_runtime_integration.py
├─ unified_retrieval_builder.py
├─ disclosure_retrieval_ranker.py
├─ runtime_evidence_merger.py
└─ disclosure_timeout_guard.py
```

```text
dashboard-ui/src/components/runtime/
├─ RuntimeEvidencePanel.tsx
├─ UnifiedEvidenceViewer.tsx
├─ DisclosureRuntimeBadge.tsx
└─ RuntimeSourceBreakdown.tsx
```

---

# Runtime Context 목표

현재 목표:

```text
news chunks
+
disclosure chunks
+
memory evidence
```

를 하나의 Runtime Context로 통합.

---

# Unified Retrieval 목표

현재 목표:

```text
뉴스 retrieval
공시 retrieval
```

동시 수행.

예상:

```text
삼성전기
+
MLCC 투자
```

↓

```text
뉴스:
MLCC 수요 증가

공시:
MLCC CAPEX 확대
```

↓

```text
통합 reasoning
```

---

# Disclosure Priority 목표

현재 목표:

```text
공식 문서 기반 evidence 우선
```

예상 우선순위:

| source | priority |
|---|---|
| DISCLOSURE | HIGH |
| EARNINGS | HIGH |
| BUSINESS_REPORT | HIGH |
| NEWS | MEDIUM |
| SOCIAL | LOW |

---

# Runtime Evidence 목표

현재 목표:

```text
AI reasoning 근거에
뉴스 + 공시 함께 표시
```

예상:

```text
상승 근거:
- 사업보고서 기준 MLCC CAPEX 확대
- 전장부품 수요 증가 뉴스
```

---

# Memory 목표

현재 목표:

```text
공시 기반 event는
memory importance 강화
```

예상:

```text
공시 포함 event
→ higher importance
→ longer retention
```

---

# Market Graph 목표

현재 목표:

```text
공시 기반 relation 강화
```

예상:

```text
삼성전기
→ MLCC 투자 확대
→ 생산능력 증가
→ 전장부품 공급 확대
```

---

# API 연동 대상

현재 API 대상:

```text
POST /api/query/run
GET /api/runtime/context/{traceId}
GET /api/runtime/evidence/{traceId}
GET /api/disclosure/search
```

---

# Runtime Context Payload 예시

```json
{
  "ticker": "009150",
  "query": "MLCC 투자",
  "news_chunks": [],
  "disclosure_chunks": [],
  "merged_evidence": [],
  "reasoning_context": []
}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- selectedTicker 중심 유지
- traceId 기반 유지
- Runtime payload 기반 유지
- disclosure evidence 우선 유지
- official document 기반 강화
- 기존 Retrieval 구조 유지
- 기존 Runtime Flow 유지
- OpenAI 호출 최소화 유지
- 발표 가능한 Runtime UX 유지
- 과도한 abstraction 금지

---

# 예상 기능

## runtime_context_assembler.py

역할:

```text
뉴스 + 공시 Runtime Context 통합
```

예상 기능:

```text
assemble_runtime_context()
```

---

## disclosure_runtime_integration.py

역할:

```text
runQuery 시 disclosure retrieval 연결
```

예상 기능:

```text
integrate_disclosure_runtime()
```

---

## unified_retrieval_builder.py

역할:

```text
뉴스 + 공시 통합 retrieval
```

예상 기능:

```text
build_unified_retrieval()
```

---

## runtime_evidence_merger.py

역할:

```text
evidence merge 및 ranking
```

예상 기능:

```text
merge_runtime_evidence()
```

---

# 검증 항목

현재 TASK 완료 전 다음 항목을 반드시 검증한다.

## Runtime 검증

- runQuery 시 disclosure retrieval 수행 여부
- selectedTicker 기반 disclosure retrieval 여부
- Runtime Context 통합 여부

---

## Retrieval 검증

- 뉴스 + 공시 통합 retrieval 여부
- disclosure ranking 정상 여부
- timeout fallback 정상 여부

---

## Reasoning 검증

- disclosure-aware reasoning 여부
- disclosure evidence 표시 여부

---

## Memory 검증

- disclosure event importance 반영 여부
- disclosure memory retention 강화 여부

---

## Dashboard 검증

- Runtime Evidence Panel 표시 여부
- 뉴스/공시 evidence 통합 여부

---

## UX 검증

- 공식 문서 기반 신뢰도 강화 여부
- 발표 설득력 강화 여부

---

# 관련 Prompt

```text
prompts/TASK-042/
```

---

# 관련 Logs

```text
logs/TASK-042/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Runtime Query Pipeline disclosure 통합 성공
- 뉴스 + 공시 통합 retrieval 성공
- Unified Runtime Context 구축 성공
- disclosure-aware reasoning 구축 성공
- disclosure-aware memory 구축 성공
- disclosure-aware signal evaluation 구축 성공
- Runtime Evidence Panel 구축 성공
- 발표 가능한 Disclosure Runtime 확보 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후 다음 작업 후보:

- TASK-043-build-portfolio-backtesting-suite
- TASK-044-build-backtesting-visualization
- TASK-045-build-presentation-demo-scenario

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- official document 기반 강화
- Runtime consistency 유지
- selectedTicker 중심 유지
- disclosure-aware reasoning 강화
- OpenAI 비용 안정성 유지
- 과도한 Autonomous AI 구조 금지