# TASK-031-build-company-resolver-and-ingestion-pipeline.md

# TASK-031 Company Resolver & Ticker Ingestion Pipeline 구축

## 상태

DONE

---

# 목표

사용자가:

```text
현대자동차
삼성전자
SK하이닉스
LG에너지솔루션
```

같은 회사명을 입력하면,
시스템이 자동으로:

```text
ticker
corp_code
관련 데이터 수집
chunking
embedding
retrieval 등록
```

까지 수행하는
자동 Company Resolver & Ingestion Pipeline을 구축한다.

현재 TASK의 목표는
수동 샘플 데이터 기반 RAG를 넘어,
다양한 종목을 동적으로 분석 가능한 구조로 확장하는 것이다.

현재 단계에서는
완전 실시간 대규모 수집보다
발표 가능한 Dynamic Ingestion Pipeline에 집중한다.

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
```

현재 시스템은:

```text
사전 임베딩된 샘플
