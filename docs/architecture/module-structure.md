# module-structure.md

# AlphaFin LTE 모듈 구조

## 문서 목적

이 문서는 AlphaFin LTE 프로젝트의
모듈 구조와 각 디렉토리의 책임을 정의한다.

목표는 다음과 같다.

- 모듈 책임 분리
- 구조적 혼동 방지
- AI 구현 위치 통일
- 유지보수 가능한 구조 유지

현재 문서는
상위 수준 디렉토리 구조를 기준으로 작성한다.

---

# 현재 예상 구조

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

# 구조 원칙

현재 프로젝트는 다음 원칙을 따른다.

- 단일 책임 유지
- 작은 모듈 유지
- 명시적 구조 유지
- 순환 의존 최소화
- 과도한 계층 분리 금지

---

# collectors/

외부 데이터 수집 모듈.

## 역할

외부 API 또는 웹에서
데이터를 수집한다.

## 예상 대상

- pykrx 시세 데이터
- OpenDART 공시 데이터
- 뉴스 데이터

## 주요 책임

- API 요청
- 응답 처리
- Raw Data 저장
- 수집 로그 생성

## 포함 가능 예시

```text
src/collectors/
├─ pykrx/
├─ opendart/
└─ news/
```

---

# preprocess/

데이터 전처리 모듈.

## 역할

수집 데이터를
검색 및 분석 가능한 형태로 변환한다.

## 주요 책임

- 텍스트 정리
- HTML 제거
- 데이터 정규화
- Chunk 생성
- Metadata 생성

## 입력

- Raw Data

## 출력

- Processed Data

---

# rag/

RAG 처리 모듈.

## 역할

검색 기반 분석 구조를 담당한다.

## 주요 책임

- Embedding 생성
- Vector 저장
- Retrieval
- Context Assembly

## 현재 목표

- 단순한 구조 유지
- 실험 가능한 구조 유지
- 경량 Vector 구조 유지

## 현재 후보 기술

- FAISS
- ChromaDB

## 포함 가능 예시

```text
src/rag/
├─ embedding/
├─ retrieval/
├─ vectorstore/
└─ context/
```

---

# analysis/

LLM 분석 모듈.

## 역할

금융 분석 흐름을 담당한다.

## 주요 책임

- Prompt 구성
- 분석 요청
- 응답 생성
- 분석 결과 저장

## 입력 가능 데이터

- 뉴스
- 공시
- Retrieval 결과
- Metadata

## 예상 흐름

```text
질문
→ Retrieval
→ Context 생성
→ Prompt 구성
→ LLM 응답 생성
```

---

# evaluation/

평가 및 실험 모듈.

## 역할

실험 결과를 비교 및 기록한다.

## 주요 책임

- Retrieval 품질 비교
- Prompt 결과 비교
- 응답 품질 비교
- 실험 로그 저장

## 현재 목표

반복 가능한 실험 구조 구축.

---

# common/

공통 기능 모듈.

## 역할

공통 기능을 관리한다.

## 주요 책임

- 설정 관리
- 환경 변수 처리
- 로그 처리
- 파일 처리
- 시간 처리
- 공통 유틸리티

## 포함 가능 예시

```text
src/common/
├─ config/
├─ logger/
├─ utils/
└─ constants/
```

---

# 의존성 방향

현재 프로젝트는
다음 방향의 의존성을 권장한다.

```text
collectors
    ↓
preprocess
    ↓
rag
    ↓
analysis
    ↓
evaluation
```

common은
모든 모듈에서 사용할 수 있다.

---

# 현재 금지 사항

현재 금지:

- 거대한 service 클래스
- 과도한 abstraction layer
- 불필요한 interface 분리
- 순환 참조 구조
- 모듈 간 직접 강결합

---

# 현재 구조 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 파일 유지
- 작은 함수 유지
- 명시적 흐름 유지
- 추적 가능한 구조 유지
- AI 협업 가능한 구조 유지

---

# 향후 확장 가능 영역

향후 확장 가능 영역:

- reranking/
- prompt-versioning/
- memory/
- experiment-tracking/

단,
현재 단계에서는
복잡한 구조를 우선하지 않는다.