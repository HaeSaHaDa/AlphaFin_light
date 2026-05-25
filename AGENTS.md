# AGENTS.md

# AlphaFin LTE 프로젝트 AI 협업 규칙

## 프로젝트 개요

이 프로젝트는 AlphaFin 논문에서 영감을 받은 한국 주식 시장 기반의 경량형(LTE) 금융 분석 시스템을 구축하는 것을 목표로 한다.

원본 AlphaFin 전체 구현이 아니라 다음 목표에 집중한다.

- 한국 주식 시장 데이터 활용
- 무료 데이터 소스 기반 구축
- 실험 가능한 수준의 경량 구조
- LLM + RAG 기반 분석 흐름 구축
- AI 협업(Codex / Cursor)에 최적화된 개발 환경 구성

---

# 핵심 원칙

## Keep Everything Small

모든 작업은 작고 명확하게 유지한다.

금지:

- 거대한 파일
- 거대한 함수
- 거대한 TASK
- 과도한 추상화
- 불필요한 리팩토링
- 한 번에 많은 기능 구현

권장:

- 작은 모듈
- 작은 함수
- 작은 커밋
- 작은 TASK
- 단일 책임 구조

---

# 구현 우선순위

다음 순서를 우선적으로 따른다.

1. 문서 정의
2. 데이터 구조 정의
3. 데이터 수집
4. 전처리
5. 저장 구조
6. 검색(RAG)
7. 분석 프롬프트
8. 평가 및 검증

---

# 현재 프로젝트 범위

현재 구현 범위:

- 한국 주식 데이터 수집
- OpenDART 공시 수집
- pykrx 기반 시세 수집
- 뉴스 데이터 수집
- 문서 저장 및 검색
- RAG 프로토타입
- LLM 기반 분석 흐름
- 간단한 백테스트 수준 검증

현재 제외 범위:

- 실거래 자동화
- 초고빈도 트레이딩
- 대규모 분산 시스템
- MSA
- 복잡한 오케스트레이션
- 과도한 벡터 인프라
- 원본 AlphaFin 완전 재현

---

# 기술 원칙

## 기본 원칙

- 단순성을 우선한다.
- 읽기 쉬운 코드를 우선한다.
- 명시적 구조를 우선한다.
- 디버깅 가능한 구조를 우선한다.

## Python 원칙

- 함수는 단일 책임 유지
- 하드코딩 금지
- 환경 변수는 `.env` 사용
- requests timeout 필수
- 예외 무시 금지
- 실패 로그 반드시 기록

## 데이터 원칙

Raw 데이터와 Processed 데이터를 분리한다.

예시:

```text
data/
├─ raw/
├─ processed/
└─ samples/
```

---

# 문서 언어 규칙

다음 규칙을 따른다.

- 문서(md)는 한글 작성
- 코드 및 변수명은 영어 사용
- 기술 용어는 필요 시 영어 유지 가능

예시:

좋은 예:
- `주가 수집기`
- `뉴스 전처리`
- `RAG 검색 흐름`

좋지 않은 예:
- `Advanced Financial Autonomous Pipeline`

---

# 문서 읽기 우선순위

모든 작업 전
반드시 다음 순서로 문서를 확인한다.

1. README.md
2. AGENTS.md
3. 현재 TASK 문서
4. docs/project/*
5. docs/architecture/*
6. docs/conventions/*
7. 기존 prompts
8. 기존 logs
9. 기존 코드

문서를 읽지 않고
바로 구현하지 않는다.

---

# AI 작업 규칙

## 구현 전 필수 확인 순서

구현 전에 반드시 아래 순서대로 읽는다.

1. AGENTS.md
2. 현재 TASK 문서
3. 관련 docs 문서
4. 기존 prompts
5. 기존 logs
6. 기존 코드

읽지 않고 바로 구현하지 않는다.

---

# TASK 규칙

모든 작업은 TASK 단위로 수행한다.

작업 폴더 구조:

tasks/
├─ backlog/
├─ todo/
├─ doing/
├─ review/
└─ done/

파일명 규칙:

TASK-001-create-project-harness.md

규칙:

- TASK 범위를 벗어난 수정 금지
- 관련 없는 리팩토링 금지
- 하나의 TASK는 하나의 목적만 가진다

---

# 현재 Prompt 관리 상태

현재 프로젝트는 실행 Prompt를
TASK 기준으로 분리 관리한다.

```text
prompts/TASK-XXX/
logs/TASK-XXX/
```

현재 구조:

```text
TASK
→ 작업 정의

prompts
→ 실행 Prompt 기록

logs
→ 실행 결과 및 이슈 기록
```

---

# 로그 규칙

중요 작업은 반드시 로그를 남긴다.

로그 위치:

prompts/
├─ TASK-001/
├─ TASK-002/

logs/
├─ TASK-001/
├─ TASK-002/
├─ daily/
├─ issues/
├─ ai-decisions/
└─ experiments/

기록 대상:

- 오류 원인
- AI 실수 패턴
- 구조 변경 이유
- 데이터 이슈
- 실험 결과

---

# 검증 규칙

구현 후 반드시 검증한다.

최소 검증 항목:

- 실행 가능 여부
- 샘플 데이터 동작 여부
- 로그 생성 여부
- 출력 파일 생성 여부
- 예외 처리 여부

검증 없이 완료 처리하지 않는다.

---

# Git 규칙

## 기본 원칙

- 작은 단위 커밋
- TASK 단위 브랜치
- 관련 없는 변경 혼합 금지

브랜치 예시:

feature/price-collector
feature/news-crawler
docs/update-architecture

커밋 예시:

feat: add pykrx price collector
fix: handle empty news response
docs: update pipeline flow

---

# 디렉토리 원칙

권장 구조:

src/
├─ collectors/
├─ preprocess/
├─ rag/
├─ analysis/
├─ evaluation/
└─ common/

각 모듈은 단일 책임 유지.

---

# 금지 사항

다음 행동을 금지한다.

- 문서 없이 대규모 구현
- 테스트 없는 완료 처리
- AI 임의 구조 변경
- 불필요한 라이브러리 추가
- 과도한 추상화
- 거대한 클래스 생성
- 설정 하드코딩
- 예외 무시
- 로그 없는 실패 처리

---

# 최종 목표

이 프로젝트의 목표는 다음과 같다.

- 한국 환경에서 실험 가능한 AlphaFin LTE 구축
- AI 협업 최적화 개발 구조 구축
- 유지보수 가능한 하네스 엔지니어링 구조 확립
- 반복 가능한 금융 AI 실험 환경 구축