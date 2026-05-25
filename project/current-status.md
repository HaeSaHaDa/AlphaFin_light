# current-status.md

# AlphaFin LTE 현재 프로젝트 상태

## 문서 목적

이 문서는 AlphaFin LTE 프로젝트의
현재 상태를 기록한다.

목표는 다음과 같다.

- 현재 구현 범위 명확화
- 미구현 영역 명확화
- AI 오인식 방지
- 미래 기능 조기 구현 방지
- 작업 우선순위 통일

현재 문서는
프로젝트 진행 상태 기준으로 관리한다.

---

# 현재 프로젝트 단계

현재 프로젝트 상태:

```text
하네스 및 문서 구조 구축 단계
```

현재는:

- 구조 설계
- 문서 체계 구축
- AI 협업 구조 구축

을 우선한다.

실제 금융 기능 구현은
아직 시작하지 않았다.

---

# 현재 완료 영역

## 기본 문서

완료:

- README.md
- AGENTS.md

---

## project 문서

완료:

- project-overview.md
- alphafin-lte-scope.md
- roadmap.md
- terminology.md

---

## architecture 문서

완료:

- architecture-overview.md
- module-structure.md
- execution-flow.md
- storage-architecture.md
- rag-architecture.md

---

## conventions 문서

완료:

- validation-rules.md
- task-prompt-history-rules.md
- task-template.md
- cursor-workflow.md

---

## data 문서

완료:

- data-sources.md

---

# 현재 미구현 영역

현재 아직 구현하지 않은 영역:

- pykrx Collector
- OpenDART Collector
- 뉴스 Collector
- DB 테이블 구조
- Embedding 구조
- Retrieval 구조
- Vector Store
- LLM 분석 코드
- 평가 코드

현재는
문서와 구조 정의 단계이다.

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

# 현재 DB 상태

현재 DB:

```text
MariaDB
```

현재 목적:

- 로컬 개발 환경 구축
- 수집 데이터 저장
- 실험 구조 저장

현재는
복잡한 DB 구조를 우선하지 않는다.

---

# 현재 AI 역할

현재 AI 역할:

```text
검색된 금융 정보를
분석하고 reasoning 하는 역할
```

현재 프로젝트는
RAG 기반 구조를 사용한다.

즉:

```text
Retriever
→ 관련 정보 검색

LLM
→ 검색 결과 분석
```

구조를 유지한다.

---

# 현재 프로젝트 범위

현재 포함 범위:

- 금융 데이터 수집
- Raw / Processed 저장 구조
- Chunk 구조
- Embedding 구조
- Retrieval 구조
- LLM 분석 흐름
- 실험 로그 구조

현재 제외 범위:

- 실거래 자동화
- HFT
- 대규모 분산 시스템
- 멀티 에이전트 구조
- 원본 AlphaFin 완전 재현

---

# 현재 우선순위

현재 우선순위:

```text
1. 문서 구조 안정화
2. TASK 구조 구축
3. Collector 구현
4. 저장 구조 구축
5. Retrieval 구축
6. LLM 분석 구축
```

---

# 다음 예정 작업

현재 다음 예정 작업:

- TASK-001 완료
- pykrx Collector 구축
- OpenDART Collector 구축
- 뉴스 Collector 구축

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 문서 우선 개발
- 작은 TASK 기반 개발
- 작은 모듈 유지
- 명시적 흐름 유지
- AI 협업 가능한 구조 유지
- Prompt 단순화 유지

---

# 현재 금지 사항

현재 금지:

- 문서 없는 구현
- 검증 없는 완료 처리
- 범위 외 기능 구현
- 미래 기능 조기 구현
- 과도한 abstraction
- 구조 임의 변경