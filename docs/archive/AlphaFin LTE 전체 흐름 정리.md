# AlphaFin LTE 전체 흐름 정리

# 프로젝트 한 줄 정의

AlphaFin LTE는
한국 금융 데이터를 수집하고,
RAG 기반으로 검색한 뒤,
LLM이 금융 정보를 분석하는
경량형 금융 AI 연구 프로젝트이다.

---

# 전체 목표

현재 프로젝트 목표:

```text
한국 금융 데이터 기반
RAG + LLM 분석 실험 환경 구축
```

현재 프로젝트는:

- 실험 가능한 구조
- 유지보수 가능한 구조
- AI 협업 가능한 구조

를 우선한다.

---

# 현재 프로젝트 범위

## 포함 범위

- pykrx 시세 수집
- OpenDART 공시 수집
- 뉴스 수집
- MariaDB 저장
- Chunk 생성
- Embedding 생성
- Vector Search
- Retrieval
- Context Assembly
- LLM 분석
- 실험 로그 저장

---

## 제외 범위

- 실거래 자동화
- HFT
- 대규모 분산 시스템
- 원본 AlphaFin 완전 재현
- 멀티 에이전트 구조
- 초대형 벡터 인프라

---

# 현재 기술 스택

| 영역 | 기술 |
|---|---|
| Language | Python |
| DB | MariaDB |
| 주가 데이터 | pykrx |
| 공시 데이터 | OpenDART API |
| 뉴스 데이터 | RSS / Crawling |
| 전처리 | pandas |
| Vector DB | FAISS 또는 ChromaDB |
| AI | OpenAI API |
| 설정 관리 | .env |
| 로그 | 파일 기반 logs/ |

---

# 전체 시스템 흐름

```text
외부 데이터 수집
→ Raw Data 저장
→ 전처리
→ Processed Data 저장
→ Chunk 생성
→ Embedding 생성
→ Vector 저장
→ Retrieval
→ Context 생성
→ Prompt 구성
→ LLM 분석
→ 결과 저장
→ 평가
```

---

# 단계별 설명

# 1. 데이터 수집 단계

## 역할

외부 금융 데이터를 가져온다.

## 데이터 종류

- 주가 데이터
- 공시 데이터
- 뉴스 데이터

## 사용 기술

- pykrx
- OpenDART API
- 뉴스 RSS / Crawling

## 예상 위치

```text
src/collectors/
```

---

# 2. Raw Data 저장 단계

## 역할

원본 데이터를 그대로 저장한다.

## 목적

- 원본 보존
- 재현 가능성 유지
- 디버깅 가능성 유지

## 저장 위치

```text
data/raw/
```

---

# 3. 전처리 단계

## 역할

검색 가능한 형태로 데이터를 정리한다.

## 주요 작업

- HTML 제거
- 텍스트 정리
- 데이터 정규화
- Metadata 생성

## 예상 위치

```text
src/preprocess/
```

---

# 4. Processed Data 저장 단계

## 역할

전처리 완료 데이터를 저장한다.

## 특징

- 검색 가능 상태
- 분석 가능 상태

## 저장 위치

```text
data/processed/
```

---

# 5. Chunk 생성 단계

## 역할

문서를 검색 가능한 단위로 분할한다.

## 예시

- 뉴스 기사 일부
- 공시 문단 일부
- 재무 설명 일부

## 저장 위치

```text
data/chunks/
```

---

# 6. Embedding 생성 단계

## 역할

텍스트를 벡터 형태로 변환한다.

## 목적

- 의미 기반 검색
- Similarity Search

## 예상 위치

```text
src/rag/embedding/
```

---

# 7. Vector 저장 단계

## 역할

Embedding 데이터를 저장한다.

## 현재 후보 기술

- FAISS
- ChromaDB

## 현재 원칙

- 단일 노드 기반
- 경량 구조 우선

---

# 8. Retrieval 단계

## 역할

질문과 관련된 문서를 검색한다.

## 검색 요소

- Similarity Search
- Metadata Filtering
- 날짜 기반 검색
- 종목 기반 검색

## 예상 위치

```text
src/rag/retrieval/
```

---

# 9. Context 생성 단계

## 역할

검색 결과를
LLM 입력 형태로 조합한다.

## 예시

```text
질문
+ 관련 뉴스
+ 관련 공시
+ 관련 Metadata
```

## 예상 위치

```text
src/rag/context/
```

---

# 10. Prompt 구성 단계

## 역할

LLM에 전달할 입력을 생성한다.

## 포함 가능 요소

- System Prompt
- 사용자 질문
- Retrieval 결과
- 금융 문맥 정보

## 예상 위치

```text
src/analysis/
```

---

# 11. AI(LLM) 분석 단계

## 역할

검색된 금융 정보를 기반으로 분석 수행.

## AI 역할

- 금융 정보 요약
- 뉴스 분석
- 공시 분석
- 시장 이벤트 해석
- Retrieval 결과 종합

## 핵심 특징

AI는:

```text
직접 모든 정보를 아는 존재가 아니라

검색된 정보를
분석하고 reasoning 하는 역할
```

을 수행한다.

---

# 12. 결과 저장 단계

## 역할

분석 결과 및 실험 결과 저장.

## 저장 가능 대상

- Prompt
- Retrieval 결과
- LLM 응답
- 실험 메타데이터

## 저장 위치 예시

```text
logs/experiments/
```

---

# 13. 평가 단계

## 역할

실험 결과 품질 비교.

## 평가 가능 대상

- Retrieval 품질
- Prompt 품질
- 응답 품질
- 검색 정확도

## 예상 위치

```text
src/evaluation/
```

---

# 현재 디렉토리 구조

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

# logs 구조

```text
logs/
├─ daily/
├─ issues/
├─ ai-decisions/
└─ experiments/
```

---

# 현재 프로젝트 원칙

현재 프로젝트는
다음 원칙을 유지한다.

- 문서 우선 개발
- 작은 TASK 기반 개발
- 작은 모듈 유지
- 명시적 구조 유지
- AI 협업 가능한 구조 유지
- 반복 가능한 실험 구조 유지

---

# 현재 프로젝트 상태

현재 상태:

```text
하네스 및 문서 구조 구축 단계
```

현재 완료:

- README.md
- AGENTS.md
- project 문서
- architecture 문서
- data 문서
- validation 문서

아직 미구현:

- 실제 Collector
- DB 테이블
- Embedding
- Retrieval
- LLM 분석
- 평가 코드

---

# 다음 단계

현재 다음 목표:

```text
1. TASK 구조 생성
2. TASK-001 완료
3. pykrx Collector 구현
4. OpenDART Collector 구현
5. 뉴스 Collector 구현
```

현재는
"구조와 흐름을 안정화하는 단계"에 해당한다.