# architecture-overview.md

# AlphaFin LTE 아키텍처 개요

## 문서 목적

이 문서는 AlphaFin LTE 프로젝트의
전체 시스템 구조를 설명한다.

목표는 다음과 같다.

- 전체 흐름 정의
- 모듈 역할 정의
- 데이터 흐름 정의
- AI 구현 방향 통일
- 구조적 혼동 방지

현재 문서는
상위 수준 아키텍처만 정의한다.

세부 구현은
각 하위 문서에서 별도로 정의한다.

---

# 전체 시스템 구조

현재 AlphaFin LTE는
다음 흐름을 기준으로 구성된다.

```text
데이터 수집
→ 데이터 저장
→ 전처리
→ Chunking
→ Embedding
→ Vector 저장
→ Retrieval
→ Context Assembly
→ LLM 분석
→ 평가
```

---

# 상위 모듈 구조


현재 예상 모듈 구조:

```text
src/
├─ collectors/
├─ preprocess/
├─ rag/
├─ analysis/
├─ evaluation/
└─ common/
```

--- 

# 모듈 설명

## collectors/

외부 데이터 수집 모듈.

예상 대상:

- pykrx 시세 수집
- OpenDART 공시 수집
- 뉴스 수집

주요 역할:

- 데이터 요청
- 응답 저장
- Raw Data 생성
- 수집 로그 기록

## preprocess/

데이터 전처리 모듈.

예상 역할:

- 텍스트 정리
- 데이터 정규화
- Chunk 생성
- Metadata 생성

입력:

- Raw Data

출력:

- Processed Data

## rag/

RAG 관련 처리 모듈.

예상 역할:

- Embedding 생성
- Vector 저장
- Retrieval
- Context Assembly

현재 목표:

- 단순하고 실험 가능한 구조 유지

현재 후보 기술:

- FAISS
- ChromaDB

## analysis/

LLM 기반 분석 모듈.

예상 역할:

- Prompt 구성
- 금융 분석 요청
- 응답 생성
- 분석 결과 저장

입력 가능 요소:

- 뉴스 데이터
- 공시 데이터
- Retrieval 결과

## evaluation/

평가 및 실험 모듈.

예상 역할:

- Retrieval 품질 비교
- Prompt 결과 비교
- 실험 기록 저장
- 샘플 기반 평가

현재 목표:

- 반복 가능한 실험 구조 구축

## common/

공통 기능 모듈.

예상 역할:

- 설정 관리
- 로그 처리
- 공통 유틸리티
- 파일 처리
- 시간 처리

---

# 데이터 흐름

현재 예상 데이터 흐름:

## 1. 데이터 수집 단계

Collector가 외부 데이터를 수집한다.

예:

- 주가 데이터
- 뉴스 데이터
- 공시 데이터

수집 결과는 Raw Data로 저장한다.

## 2. 전처리 단계

Raw Data를 분석 가능한 형태로 변환한다.

포함 가능 작업:

- 텍스트 정리
- HTML 제거
- Chunk 생성
- Metadata 생성

결과는 Processed Data로 저장한다.

## 3. RAG 단계

Processed Data 기반 검색 구조 생성.

포함 단계:

- Embedding 생성
- Vector 저장
- Retrieval
- Context 생성

## 4. 분석 단계

LLM 기반 금융 분석 수행.

예상 흐름:

```text
	질문
	→ Retrieval
	→ Context 생성
	→ Prompt 구성
	→ LLM 응답 생성
```

## 5. 평가 단계

실험 결과를 비교 및 기록한다.

예상 대상:

- Retrieval 품질
- Prompt 결과
- 응답 품질
- 검색 정확도

--- 

# 현재 구조 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 단순성 우선
- 작은 모듈 유지
- 명시적 흐름 유지
- 추적 가능한 구조 유지
- AI 협업 가능한 구조 유지

---

# 현재 제외 범위

현재 제외 대상:

- 대규모 분산 시스템
- 멀티 노드 Retrieval
- 실시간 거래 시스템
- Agent Orchestration
- 초대형 Vector 인프라

현재 프로젝트는
경량형 연구 구조를 목표로 한다.

# 향후 확장 가능 영역

향후 확장 가능 영역:

- Reranking
- Hybrid Search
- Memory Layer
- Prompt Versioning
- 실험 자동화
- Retrieval 최적화

단,
현재 단계에서는
복잡한 구조 도입을 우선하지 않는다.