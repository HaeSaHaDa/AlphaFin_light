# terminology.md

# AlphaFin LTE 용어 정의

## 문서 목적

이 문서는 AlphaFin LTE 프로젝트에서 사용하는
주요 용어를 정의한다.

목표는 다음과 같다.

- 용어 혼동 방지
- 문서 간 표현 통일
- AI 협업 시 의미 충돌 방지
- 구조적 일관성 유지

---

# 프로젝트 용어

## AlphaFin LTE

현재 프로젝트의 이름.

의미:

```text
한국 금융 환경 기반의 경량형 금융 AI 연구 프로젝트
원본 AlphaFin 논문의 전체 구조를
완전히 재현하는 프로젝트는 아니다.
``` 

# 데이터 관련 용어

## Raw Data

수집 직후의 원본 데이터.

예:

- 원본 뉴스
- 원본 공시
- 원본 시세 데이터

특징:

- 전처리 전 상태
- 수정하지 않음
- 원본 유지 목적

저장 위치 예시:

```text
data/raw/
```

## Processed Data

전처리 완료 데이터.

예:

- 정제된 뉴스
- Chunk 생성 완료 문서
- Metadata 추가 데이터

특징:

- 검색 가능 상태
- 분석 가능 상태

저장 위치 예시:
```text
	data/processed/
```
## Sample Data

테스트 및 검증용 데이터.

특징:

- 작은 규모
- 빠른 검증 목적
- 반복 테스트 목적

저장 위치 예시:
```text
	data/samples/
```
# 수집 관련 용어

## Collector

외부 데이터를 수집하는 모듈.

예:

- 주가 수집기
- 공시 수집기
- 뉴스 수집기

예상 위치:
```text
	src/collectors/
```
## Crawling

웹 페이지 기반 데이터 수집.

주의:

- robots.txt 확인 필요
- 과도한 요청 금지
- 법적 제한 확인 필요

# RAG 관련 용어

## RAG

Retrieval-Augmented Generation.

검색 결과를 기반으로
LLM 응답을 생성하는 구조.

현재 프로젝트의 핵심 구조 중 하나.

## Chunk

문서를 작은 단위로 분할한 데이터.

예:

- 뉴스 기사 일부
- 공시 문단 일부
- 재무 설명 일부

Chunk는 Retrieval 및 Embedding의 기본 단위로 사용된다.

## Embedding

텍스트를 벡터 형태로 변환한 데이터.

주요 목적:

- 의미 기반 검색
- Vector Search

## Vector DB

- Embedding 데이터를 저장하는 구조.
- 현재 프로젝트에서는 단일 노드 기반 경량 Vector DB 구조를 우선한다.

현재 후보:

- FAISS
- ChromaDB

## Metadata

문서 검색 및 필터링을 위해
문서에 추가되는 부가 정보.

예:

- 종목코드
- 날짜
- 뉴스 출처
- 공시 종류
- 문서 타입

Metadata는 Retrieval 단계에서
검색 정확도 향상에 사용된다.

## Retrieval

사용자 질문과 관련된 문서를 검색하는 단계.

포함 가능 요소:

- Vector Search
- Similarity Search
- Metadata Filtering
- 날짜 기반 필터링
- 종목 기반 필터링

## Context Assembly

검색 결과를
LLM 입력용 Context로 조합하는 단계.

예:
```text
	질문
	+ 검색 결과
	+ 공시 정보
	+ 뉴스 정보
```

# LLM 관련 용어

## Prompt

LLM에 전달하는 입력 구조.

종류 예시:

- System Prompt
- Analysis Prompt
- Evaluation Prompt

## Analysis Flow

LLM 기반 금융 분석 흐름 전체.

예상 흐름:

```text
	Retrieval
	→ Context Assembly
	→ Prompt 구성
	→ LLM 응답 생성
```

# 프로젝트 구조 관련 용어

## Harness Engineering

AI 협업을 위한
문서 기반 운영 구조 설계 방식.

포함 요소:

- AGENTS.md
- docs/
- tasks/
- prompts/
- logs/
- 검증 규칙

## TASK

작은 단위 작업 문서.

규칙:

- 하나의 목적만 가진다
- 범위를 명확히 정의한다
- 검증 기준을 포함한다

예시:

```text
TASK-001-create-project-harness.md
```

## Validation

구현 결과 검증 과정.

최소 포함 항목:

- 실행 가능 여부
- 샘플 데이터 동작 여부
- 로그 생성 여부
- 예외 처리 여부

# 로그 관련 용어

## Experiment Log

실험 결과 기록.

포함 예시:

- Retrieval 결과
- Prompt 비교
- 응답 품질 비교

## AI Decision Log

AI가 수행한 구조적 결정 기록.

예:

- 구조 변경 이유
- 라이브러리 선택 이유
- 설계 변경 이유

# 현재 제외 용어

현재 프로젝트에서 적극적으로 사용하지 않는 용어:

- MSA
- Distributed Retrieval Cluster
- Agent Orchestration
- HFT
- Institutional Trading System

현재 프로젝트는
경량형 연구 구조를 목표로 한다.