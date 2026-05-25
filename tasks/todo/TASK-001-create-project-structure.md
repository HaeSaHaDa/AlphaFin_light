# TASK-001-create-project-structure.md

# TASK-001 프로젝트 기본 구조 생성

## 상태

DONE

---

# 목표

AlphaFin LTE 프로젝트의
기본 디렉토리 구조와
초기 문서 구조를 생성한다.

현재 TASK의 목표는
AI 협업 가능한 최소 프로젝트 구조를 만드는 것이다.

실제 금융 기능 구현은 포함하지 않는다.

---

# 범위

현재 TASK에서 포함하는 작업:

- docs 디렉토리 생성
- tasks 디렉토리 생성
- logs 디렉토리 생성
- data 디렉토리 생성
- src 디렉토리 생성
- 기본 md 문서 생성
- 기본 구조 정리

---

# 현재 제외 범위

현재 TASK에서 제외:

- 실제 Collector 구현
- DB 테이블 생성
- RAG 구현
- Embedding 구현
- LLM 연동
- Prompt 구현
- 실험 코드 구현

현재 TASK는
프로젝트 구조 생성만 수행한다.

---

# 생성 대상 구조

## 루트 구조

```text
alphafin-lte/
├─ README.md
├─ AGENTS.md
├─ docs/
├─ tasks/
├─ logs/
├─ data/
└─ src/
```

---

# docs 구조

```text
docs/
├─ project/
├─ architecture/
├─ data/
├─ pipeline/
├─ rag/
├─ evaluation/
├─ conventions/
└─ setup/
```

---

# tasks 구조

```text
tasks/
├─ backlog/
├─ todo/
├─ doing/
├─ review/
└─ done/
```

---

# logs 구조

```text
logs/
├─ daily/
├─ issues/
├─ ai-decisions/
└─ experiments/
```

---

# data 구조

```text
data/
├─ raw/
├─ processed/
├─ chunks/
├─ embeddings/
└─ samples/
```

---

# src 구조

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

# 생성 대상 문서

## 현재 포함 문서

```text
README.md
AGENTS.md
```

## docs/project/

```text
project-overview.md
alphafin-lte-scope.md
roadmap.md
terminology.md
```

## docs/architecture/

```text
architecture-overview.md
module-structure.md
execution-flow.md
storage-architecture.md
rag-architecture.md
```

## docs/data/

```text
data-sources.md
```

## docs/conventions/

```text
validation-rules.md
```

---

# 구현 규칙

현재 TASK는 다음 규칙을 따른다.

- 작은 구조 우선
- 명시적 디렉토리 구조 유지
- 과도한 abstraction 금지
- 불필요한 코드 생성 금지
- 문서 우선 구조 유지

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## 디렉토리 검증

- docs 생성 여부
- tasks 생성 여부
- logs 생성 여부
- data 생성 여부
- src 생성 여부

---

## 문서 검증

- md 파일 생성 여부
- markdown 구조 정상 여부
- 코드블럭 정상 여부
- 헤더 depth 정상 여부

---

## 구조 검증

- 디렉토리 depth 정상 여부
- 중복 디렉토리 여부
- 잘못된 위치 여부

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- 기본 디렉토리 구조 생성 완료
- 기본 md 문서 생성 완료
- markdown 구조 검증 완료
- 디렉토리 구조 검증 완료

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-002-build-pykrx-collector
- TASK-003-build-opendart-collector
- TASK-004-build-news-collector

단,
Collector 구현 전
문서 구조 검증을 우선한다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 문서 우선 개발
- 작은 TASK 기반 개발
- 명시적 구조 유지
- AI 협업 가능한 구조 유지
- 반복 가능한 실험 구조 유지

