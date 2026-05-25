# execution-flow.md

# AlphaFin LTE 실행 흐름

## 문서 목적

이 문서는 AlphaFin LTE 프로젝트의
전체 실행 흐름과 데이터 이동 과정을 정의한다.

목표는 다음과 같다.

- 데이터 흐름 명확화
- 모듈 간 연결 구조 정의
- 실행 순서 통일
- AI 구현 방향 통일
- 구조적 혼동 방지

현재 문서는
상위 수준 실행 흐름을 기준으로 작성한다.

---

# 전체 실행 흐름

현재 AlphaFin LTE는
다음 흐름을 기준으로 동작한다.

```text
데이터 수집
→ Raw Data 저장
→ 전처리
→ Processed Data 저장
→ Chunk 생성
→ Embedding 생성
→ Vector 저장
→ Retrieval
→ Context Assembly
→ Prompt 구성
→ LLM 분석
→ 결과 저장
→ 평가
```

---

# 실행 단계 개요

현재 프로젝트는
다음 단계로 실행된다.

| 단계 | 설명 |
|---|---|
| 1 | 데이터 수집 |
| 2 | Raw Data 저장 |
| 3 | 전처리 |
| 4 | Processed Data 저장 |
| 5 | Chunk 생성 |
| 6 | Embedding 생성 |
| 7 | Vector 저장 |
| 8 | Retrieval |
| 9 | Context Assembly |
| 10 | Prompt 구성 |
| 11 | LLM 분석 |
| 12 | 결과 저장 |
| 13 | 평가 |

---

# 1. 데이터 수집 단계

## 목적

외부 데이터 수집.

## 주요 대상

- 한국 주식 시세
- OpenDART 공시
- 뉴스 데이터

## 예상 모듈

```text
src/collectors/
```

## 예상 처리

- API 요청
- HTML 요청
- 응답 처리
- 수집 로그 기록

---

# 2. Raw Data 저장 단계

## 목적

원본 데이터 보존.

## 저장 대상

- 원본 뉴스
- 원본 공시
- 원본 시세 데이터

## 저장 위치 예시

```text
data/raw/
```

## 원칙

- 원본 수정 금지
- 수집 시점 유지
- 재현 가능성 유지

---

# 3. 전처리 단계

## 목적

검색 및 분석 가능한 형태로 변환.

## 예상 처리

- HTML 제거
- 텍스트 정리
- 데이터 정규화
- 불필요 데이터 제거

## 예상 모듈

```text
src/preprocess/
```

---

# 4. Processed Data 저장 단계

## 목적

전처리 완료 데이터 저장.

## 저장 위치 예시

```text
data/processed/
```

## 특징

- 검색 가능 상태
- 분석 가능 상태
- Metadata 포함 가능

---

# 5. Chunk 생성 단계

## 목적

문서를 검색 가능한 단위로 분할.

## 예상 대상

- 뉴스 기사
- 공시 문서
- 재무 설명 텍스트

## 결과

Chunk 단위 데이터 생성.

---

# 6. Embedding 생성 단계

## 목적

텍스트를 벡터 형태로 변환.

## 예상 역할

- 의미 기반 검색 지원
- Vector Search 지원

## 예상 모듈

```text
src/rag/embedding/
```

---

# 7. Vector 저장 단계

## 목적

Embedding 저장.

## 현재 후보 기술

- FAISS
- ChromaDB

## 현재 원칙

- 단일 노드 기반
- 경량 구조 우선
- 실험 가능한 구조 우선

---

# 8. Retrieval 단계

## 목적

질문과 관련된 문서 검색.

## 포함 가능 요소

- Similarity Search
- Metadata Filtering
- 날짜 기반 검색
- 종목 기반 검색

## 예상 모듈

```text
src/rag/retrieval/
```

---

# 9. Context Assembly 단계

## 목적

검색 결과를
LLM 입력용 Context로 조합.

## 예상 구성 요소

```text
질문
+ Retrieval 결과
+ 뉴스 정보
+ 공시 정보
+ Metadata
```

## 예상 모듈

```text
src/rag/context/
```

---

# 10. Prompt 구성 단계

## 목적

LLM 입력 Prompt 생성.

## 포함 가능 요소

- System Prompt
- 사용자 질문
- Retrieval 결과
- 금융 문맥 정보

## 예상 모듈

```text
src/analysis/
```

---

# 11. LLM 분석 단계

## 목적

금융 분석 응답 생성.

## 예상 역할

- 뉴스 기반 분석
- 공시 기반 분석
- Retrieval 기반 응답 생성

## 출력 예시

- 분석 결과
- 요약 결과
- 판단 근거

---

# 12. 결과 저장 단계

## 목적

분석 결과 및 실험 결과 저장.

## 저장 가능 대상

- Prompt
- Retrieval 결과
- LLM 응답
- 실험 메타데이터

## 예상 위치

```text
logs/experiments/
```

---

# 13. 평가 단계

## 목적

분석 품질 검증.

## 평가 가능 대상

- Retrieval 품질
- Prompt 품질
- 응답 품질
- 검색 정확도

## 예상 모듈

```text
src/evaluation/
```

---

# 현재 실행 원칙

현재 프로젝트는
다음 원칙을 유지한다.

- 단순한 흐름 유지
- 명시적 데이터 이동 유지
- 추적 가능한 구조 유지
- 실험 가능한 구조 유지
- AI 협업 가능한 구조 유지

---

# 현재 제외 범위

현재 제외:

- 실시간 거래 시스템
- 멀티 에이전트 구조
- 대규모 분산 Retrieval
- 초대형 Vector 인프라
- 실거래 자동화

현재 프로젝트는
경량형 연구 구조를 목표로 한다.

---

# 향후 확장 가능 영역

향후 확장 가능 영역:

- reranking
- hybrid search
- memory layer
- prompt versioning
- 실험 자동화
- retrieval 최적화

단,
현재 단계에서는
복잡한 구조를 우선하지 않는다.