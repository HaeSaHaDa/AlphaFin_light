# storage-architecture.md

# AlphaFin LTE 저장 구조

## 문서 목적

이 문서는 AlphaFin LTE 프로젝트의
데이터 저장 구조와 저장 원칙을 정의한다.

목표는 다음과 같다.

- 데이터 저장 구조 통일
- Raw / Processed 데이터 분리
- 검색 데이터 구조 정의
- 실험 재현 가능성 확보
- AI 구현 방향 통일

현재 문서는
경량형 연구 구조를 기준으로 작성한다.

---

# 저장 구조 개요

현재 프로젝트는
다음 저장 흐름을 기준으로 한다.

```text
수집 데이터
→ Raw Data 저장
→ 전처리
→ Processed Data 저장
→ Chunk 저장
→ Embedding 저장
→ Retrieval 결과 저장
→ 실험 결과 저장
```

---

# 최상위 저장 구조

현재 예상 구조:

```text
data/
├─ raw/
├─ processed/
├─ chunks/
├─ embeddings/
└─ samples/
```

---

# 저장 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Raw Data 수정 금지
- Processed Data 분리 저장
- 실험 재현 가능성 유지
- Metadata 기반 구조 유지
- 검색 가능한 구조 유지

---

# raw/

원본 데이터 저장 영역.

## 목적

외부에서 수집한 데이터를
원본 상태 그대로 보관한다.

## 저장 대상

- 뉴스 원문
- 공시 원문
- 시세 데이터
- API 응답 원본

## 특징

- 수정 금지
- 원본 유지
- 재현 가능성 보장

## 예시 구조

```text
data/raw/
├─ news/
├─ dart/
└─ stock/
```

---

# processed/

전처리 완료 데이터 저장 영역.

## 목적

검색 및 분석 가능한 상태의 데이터를 저장한다.

## 포함 가능 요소

- 정제된 텍스트
- 정규화 데이터
- Metadata 포함 데이터
- 분석용 데이터

## 특징

- 검색 가능 상태
- 분석 가능 상태
- 구조화 가능 상태

## 예시 구조

```text
data/processed/
├─ news/
├─ dart/
└─ stock/
```

---

# chunks/

Chunk 데이터 저장 영역.

## 목적

문서를 검색 가능한 단위로 저장한다.

## 저장 대상

- 뉴스 Chunk
- 공시 Chunk
- 재무 설명 Chunk

## 특징

- Retrieval 기본 단위
- Metadata 포함 가능
- Embedding 연결 가능

## 예시 구조

```text
data/chunks/
├─ news/
├─ dart/
└─ financial/
```

---

# embeddings/

Embedding 저장 영역.

## 목적

텍스트 벡터 데이터를 저장한다.

## 현재 후보 기술

- FAISS
- ChromaDB

## 특징

- 의미 기반 검색 지원
- Retrieval 지원
- Chunk 연결 가능

## 현재 원칙

- 단일 노드 기반
- 경량 구조 우선
- 실험 구조 우선

---

# samples/

샘플 데이터 저장 영역.

## 목적

빠른 테스트 및 검증 지원.

## 특징

- 작은 규모 유지
- 반복 테스트 가능
- 빠른 실행 가능

## 사용 목적

- Collector 테스트
- Retrieval 테스트
- Prompt 테스트
- 실험 재현

---

# 로그 저장 구조

현재 예상 구조:

```text
prompts/
├─ TASK-001/
├─ TASK-002/
└─ TASK-003/

logs/
├─ TASK-001/
├─ TASK-002/
├─ daily/
├─ issues/
├─ ai-decisions/
└─ experiments/
```

---

# logs/daily/

일일 작업 로그 저장.

## 기록 가능 대상

- 작업 내용
- 오류 발생
- 수정 내역
- 구조 변경

---

# logs/issues/

문제 및 오류 기록.

## 기록 가능 대상

- 버그 원인
- 데이터 오류
- API 오류
- Retrieval 실패

---

# logs/ai-decisions/

AI 구조 결정 기록.

## 기록 가능 대상

- 구조 변경 이유
- 라이브러리 선택 이유
- Prompt 변경 이유
- Retrieval 변경 이유

---

# logs/experiments/

실험 결과 저장.

## 저장 가능 대상

- Prompt 결과
- Retrieval 결과
- 응답 품질 비교
- 실험 메타데이터

---

# prompts/

실행 Prompt 저장 영역.

## 목적

- AI 실행 기록 보존
- 세션 복구 지원
- 작업 재현 가능성 확보

## 예시 구조

```text
prompts/
├─ TASK-001/
├─ TASK-002/
└─ TASK-003/
```

---

# Metadata 저장 원칙

현재 프로젝트는
Metadata 기반 구조를 유지한다.

## Metadata 예시

- 종목코드
- 날짜
- 뉴스 출처
- 공시 종류
- 문서 타입

## 목적

- Retrieval 정확도 향상
- 검색 필터링 지원
- 실험 추적 지원

---

# 파일 저장 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 파일 유지
- 명확한 디렉토리 구조 유지
- Raw / Processed 분리 유지
- 실험 결과 분리 유지
- 로그 분리 유지

---

# 현재 제외 범위

현재 제외:

- 대규모 데이터 레이크
- 분산 파일 시스템
- 클라우드 스토리지 최적화
- 초대형 데이터 파이프라인

현재 프로젝트는
경량형 연구 구조를 목표로 한다.

---

# 현재 DB 선택

현재 프로젝트는 MariaDB를 사용한다.

## 사용 목적

- 로컬 개발 환경 구축
- 수집 데이터 저장
- 전처리 데이터 저장
- 실험 결과 저장
- 초기 검증용 관계형 저장소 구성

## 현재 원칙

- 단순한 테이블 구조를 우선한다.
- 복잡한 ORM 구조를 도입하지 않는다.
- SQL이 추적 가능하도록 유지한다.
- 과도한 DB 최적화를 우선하지 않는다.

---

# 향후 확장 가능 영역

향후 프로젝트 규모가 커질 경우
다음 확장을 검토할 수 있다.

- PostgreSQL
- Supabase
- 원격 DB 환경
- 클라우드 저장 구조

단,
현재 단계에서는
MariaDB 기반 로컬 구조를 우선한다.