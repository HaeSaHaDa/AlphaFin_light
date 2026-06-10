# AlphaFin LTE RAG 구조

## 문서 목적

현재 구현된 뉴스·공시 통합 Retrieval과 LLM Context 흐름을 정의한다.

---

# Retrieval 개요

```text
Runtime Query
→ Query Embedding
→ ticker filtered news/document retrieval
→ selectedTicker disclosure retrieval
→ source 정규화
→ score 기반 evidence 병합
→ Runtime Context
→ Unified Context
→ LLM Analysis
```

---

# 뉴스 및 일반 문서 Retrieval

위치:

```text
src/rag/embedding/
src/rag/retrieval/
src/runtime_flow/retrieval_executor.py
```

동작:

- OpenAI `text-embedding-3-small` 사용
- MariaDB `document_embeddings` 조회
- ticker metadata filter 적용
- cosine similarity 기반 ranking
- top_k 결과 반환

---

# Disclosure Retrieval

위치:

```text
src/disclosure/
src/runtime_query/disclosure_runtime_integration.py
```

동작:

- OpenDART 문서 수집 또는 cache 재사용
- `disclosure_documents` 저장
- disclosure chunk 생성
- selectedTicker 기반 후보 조회
- query token overlap와 importance 기반 점수 계산

---

# Unified Retrieval

위치:

```text
src/runtime_query/unified_retrieval_builder.py
src/runtime_query/runtime_evidence_merger.py
```

출력 분류:

```text
news_chunks
disclosure_chunks
merged_evidence
source_breakdown
```

공시 evidence가 있으면 Runtime Context에 `has_disclosure`와
`disclosure_priority`가 포함된다.

---

# Context Assembly

위치:

```text
src/rag/context/
src/rag/unified_engine/context_orchestrator.py
```

기본 retrieval context에 다음 보강 context가 연결된다.

- layered memory
- temporal memory
- reflection
- event graph
- stock chain

Context는 최대 길이를 제한하고 document type별로 정리한다.

---

# LLM 분석

위치:

```text
src/rag/unified_engine/engine_runner.py
```

현재 기본 Chat 모델:

```text
gpt-4o-mini
```

주요 출력:

- bullish factors
- bearish factors
- risks
- summary
- referenced chunks

이후 Evaluation, Reflection, Memory, Graph 단계가 이어진다.

---

# Trace 원칙

- Runtime 결과는 `trace_id`로 저장한다.
- Dashboard API는 명시적 trace 조회를 우선한다.
- selectedTicker와 다른 ticker의 결과를 fallback으로 사용하지 않는다.

---

# 현재 한계

- 뉴스 retrieval embedding과 disclosure retrieval의 scoring 방식이 다르다.
- Context usage 평가는 실제 사용 근거를 충분히 추적하지 못할 수 있다.
- OpenAI 호출 실패와 Runtime completed 상태의 계약을 보강해야 한다.
- 고급 reranker와 분산 vector infrastructure는 범위 밖이다.
