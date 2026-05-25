# rag-architecture.md

# AlphaFin LTE RAG 구조

## 문서 목적

이 문서는 AlphaFin LTE 프로젝트의
RAG(Retrieval-Augmented Generation) 구조를 정의한다.

목표는 다음과 같다.

- Retrieval 흐름 정의
- 검색 구조 정의
- Context 생성 구조 정의
- LLM 입력 흐름 정의
- AI 구현 방향 통일

현재 문서는
경량형 연구 구조를 기준으로 작성한다.

---

# RAG 개요

현재 프로젝트의 RAG 구조는
다음 흐름을 기준으로 구성된다.

```text
문서 수집
→ 전처리
→ Chunk 생성
→ Embedding 생성
→ Vector 저장
→ Retrieval
→ Context Assembly
→ Prompt 구성
→ LLM 분석
```

---

# 현재 RAG 목표

현재 프로젝트의 목표:

- 검색 가능한 금융 문서 구조 구축
- 뉴스 기반 Retrieval
- 공시 기반 Retrieval
- Metadata 기반 검색
- LLM 기반 금융 분석 지원

현재 프로젝트는
실험 가능한 수준의 단순 구조를 우선한다.

---

# 현재 RAG 범위

## 포함 범위

현재 포함:

- Chunk 기반 검색
- Embedding 기반 검색
- Metadata Filtering
- Context Assembly
- Prompt 기반 분석

---

## 제외 범위

현재 제외:

- 대규모 분산 Retrieval
- 초대형 Vector 인프라
- 복잡한 Multi-Agent Retrieval
- 실시간 검색 최적화
- 대규모 Reranking Cluster

---

# Chunk 구조

## 목적

문서를 검색 가능한 단위로 분할한다.

## 예상 대상

- 뉴스 기사
- 공시 문서
- 재무 설명 텍스트

## 현재 원칙

- 작은 단위 유지
- 의미 단위 유지
- 검색 가능한 구조 유지

## Chunk 포함 가능 정보

- 본문 텍스트
- 종목코드
- 날짜
- 뉴스 출처
- 공시 종류
- 문서 타입

---

# Embedding 구조

## 목적

텍스트를 벡터 형태로 변환한다.

## 역할

- 의미 기반 검색 지원
- Similarity Search 지원
- Retrieval 지원

## 현재 원칙

- 경량 구조 우선
- 실험 가능한 구조 우선
- 단일 노드 기반 구조 우선

---

# Vector Store 구조

## 목적

Embedding 데이터를 저장한다.

## 현재 후보 기술

- FAISS
- ChromaDB

## 현재 원칙

- 단순한 구조 유지
- 빠른 실험 가능 구조 유지
- 로컬 기반 구조 우선

---

# Retrieval 구조

## 목적

질문과 관련된 문서를 검색한다.

## 포함 가능 요소

- Similarity Search
- Metadata Filtering
- 날짜 기반 검색
- 종목 기반 검색

## Retrieval 입력

예시:

```text
사용자 질문
+ 종목코드
+ 날짜 정보
+ 검색 조건
```

## Retrieval 출력

예시:

```text
관련 뉴스
관련 공시
관련 Chunk
Metadata
```

---

# Metadata 구조

## 목적

검색 정확도를 향상한다.

## 포함 가능 정보

- 종목코드
- 날짜
- 뉴스 출처
- 공시 종류
- 문서 타입

## 사용 목적

- 검색 필터링
- Context 정렬
- 실험 추적

---

# Context Assembly 구조

## 목적

검색 결과를
LLM 입력 가능한 형태로 조합한다.

## 현재 예상 구성

```text
질문
+ Retrieval 결과
+ 뉴스 정보
+ 공시 정보
+ Metadata
```

## 현재 원칙

- 너무 긴 Context 방지
- 관련성 우선
- 명시적 구조 유지

---

# Prompt 연결 구조

## 목적

RAG 결과를 Prompt에 연결한다.

## 포함 가능 요소

- System Prompt
- 사용자 질문
- Retrieval 결과
- 금융 문맥 정보

## 예상 흐름

```text
Retrieval
→ Context 생성
→ Prompt 구성
→ LLM 분석
```

---

# 현재 예상 모듈 구조

```text
src/rag/
├─ embedding/
├─ retrieval/
├─ vectorstore/
└─ context/
```

---

# 현재 구조 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 단순성 우선
- 작은 모듈 유지
- 명시적 흐름 유지
- 추적 가능한 Retrieval 유지
- AI 협업 가능한 구조 유지

---

# 현재 제외 범위

현재 제외:

- Hybrid Search 최적화
- 고급 Reranking
- 멀티 노드 Vector DB
- Agentic Retrieval
- 초대형 검색 클러스터

현재 프로젝트는
경량형 연구 구조를 목표로 한다.

---

# 향후 확장 가능 영역

향후 확장 가능 영역:

- reranking
- hybrid search
- query expansion
- retrieval cache
- prompt versioning
- memory layer

단,
현재 단계에서는
복잡한 Retrieval 구조를 우선하지 않는다.