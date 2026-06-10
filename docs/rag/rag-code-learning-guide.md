# AlphaFin LTE RAG 코드 학습 가이드

## 문서 목적

이 문서는 AlphaFin LTE의 현재 코드를 이용해 RAG(Retrieval-Augmented Generation)를
학습하기 위한 안내서다.

이 프로젝트를 완성된 모범 답안으로 설명하지 않는다. 대신 다음 세 가지 관점으로
코드를 분석한다.

1. 현재 코드가 실제로 어떻게 동작하는가
2. RAG 학습에 도움이 되는 부분은 무엇인가
3. 실전 시스템으로 발전시키려면 무엇을 개선해야 하는가

현재 코드의 성격은 다음과 같이 보는 것이 적절하다.

```text
RAG 전체 흐름 학습용 프로토타입: 적합
실제 API와 DB를 연결하는 실습: 적합
프로덕션 RAG 모범 구현: 부적합
문제점을 찾아 개선하는 학습 프로젝트: 매우 적합
```

---

# 1. 먼저 알아야 할 RAG 개념

RAG는 LLM이 자체 학습 지식만으로 답하지 않고, 외부 문서를 검색한 뒤 그 검색 결과를
Context로 제공하여 답을 생성하게 하는 구조다.

기본 흐름은 다음과 같다.

```text
문서 수집
-> 문서 정리
-> Chunk 분할
-> Embedding 생성
-> Vector 저장
-> 사용자 Query Embedding 생성
-> 유사 문서 검색
-> Context 조립
-> LLM 답변 생성
-> 근거 및 품질 평가
```

AlphaFin LTE는 이 기본 흐름에 다음 기능을 추가했다.

```text
종목 ticker 필터
뉴스 최신성 점수
OpenDART 공시
Persona 기반 분석
Memory
Reflection
Event Graph
Stock Chain
Trace
Dashboard
```

Memory, Event Graph, Stock Chain은 기본 RAG의 필수 요소는 아니다. 기본 RAG를 이해한
다음 확장 기능으로 보는 것이 좋다.

---

# 2. 프로젝트의 실제 RAG 흐름

## 전체 흐름

```text
사용자 종목 선택 및 분석 키워드 입력
-> Runtime Query 생성
-> 회사와 ticker 확정
-> 뉴스와 공시 수집 상태 확인
-> 필요한 데이터 수집
-> Chunk 및 Embedding 생성
-> 뉴스 Vector Retrieval
-> 공시 Lexical Retrieval
-> 뉴스와 공시 Evidence 병합
-> Prompt Context 조립
-> OpenAI Chat 호출
-> 분석 결과 평가
-> Memory, Event Graph, Stock Chain 저장
-> trace_id 기반 결과 조회
```

중요한 점은 뉴스와 공시의 검색 방식이 현재 서로 다르다는 것이다.

| 데이터 | 현재 검색 방식 | Embedding 사용 |
|---|---|---:|
| 뉴스 | cosine similarity + freshness | 사용 |
| 기존 일반 문서 | cosine similarity | 사용 |
| 공시 본문 | query token overlap + importance + freshness | 검색에는 미사용 |

공시 embedding은 생성하고 DB에 저장하지만, 현재 공시 Retrieval 코드는 그 벡터를
읽어 유사도를 계산하지 않는다.

---

# 3. 학습 권장 코드 읽기 순서

처음부터 Unified Engine 전체를 읽으면 Memory와 Graph 코드 때문에 핵심 RAG 흐름을
놓치기 쉽다. 다음 순서로 읽는 것을 권장한다.

## 1단계: 입력과 Runtime Query

```text
dashboard-ui/src/hooks/use-selected-ticker.ts
dashboard-ui/src/components/company-selector/QueryExecutionPanel.tsx
src/dashboard_api/routes/query.py
src/company_master/query_builder.py
src/runtime_flow/runtime_query_runner.py
```

확인할 내용:

- 사용자가 종목을 어떻게 선택하는가
- 분석 키워드가 어떤 배열로 전달되는가
- 회사명, ticker, 키워드가 어떤 query 문자열로 합쳐지는가
- `selectedTicker`가 Backend까지 유지되는가

현재 query 예:

```text
SK하이닉스 000660 삼성전자 엔비디아 TSMC 마이크론
```

현재 추가 키워드는 경쟁사 문서를 별도로 수집하는 조건이 아니다. 선택한 ticker의
기존 문서를 검색할 때 Query Embedding에 포함되는 조건이다.

## 2단계: 데이터 수집

```text
src/ingestion_pipeline/ingestion_runner.py
src/ingestion_pipeline/news_ingestor.py
src/disclosure/dart_collector.py
src/disclosure/disclosure_body_collector.py
```

확인할 내용:

- cache가 있으면 수집을 생략하는 방식
- 뉴스 수집 query가 회사명 중심이라는 점
- OpenDART `corp_code`가 필요한 이유
- 공시 목록과 공시 본문이 다른 API로 수집된다는 점
- 실패 시 status와 로그가 어떻게 남는가

## 3단계: Chunk 생성

뉴스와 기존 공시 제목 경로:

```text
src/ingestion_pipeline/chunk_pipeline.py
src/preprocess/chunking/
```

공시 본문 경로:

```text
src/disclosure/disclosure_chunker.py
src/disclosure/disclosure_repository.py
```

현재 공시에는 두 저장 경로가 공존한다.

```text
dart_disclosures
-> 기존 OpenDART 목록 및 report_name 중심
-> document_chunks에 제목 중심 chunk 생성

disclosure_documents
-> report_name + raw_text 본문 저장
-> disclosure_chunks에 본문 section chunk 생성
```

학습할 때 두 경로를 같은 것으로 오해하지 않아야 한다.

## 4단계: Embedding 생성

뉴스 및 일반 문서:

```text
src/ingestion_pipeline/embedding_pipeline.py
src/rag/embedding/embedder.py
src/rag/embedding/storage.py
```

공시 본문:

```text
src/disclosure/disclosure_embedder.py
src/disclosure/disclosure_repository.py
```

현재 기본 Embedding 모델:

```text
text-embedding-3-small
```

학습 포인트:

- Chunk 단위로 Embedding을 생성한다.
- 이미 Embedding이 있는 Chunk는 다시 호출하지 않는다.
- 비용 guard와 hash cache가 존재한다.
- API 실패 시 더미 벡터를 저장하지 않는다.

## 5단계: 뉴스 Vector Retrieval

```text
src/runtime_flow/retrieval_executor.py
src/rag/retrieval/retriever.py
src/rag/retrieval/similarity.py
src/rag/retrieval/freshness.py
```

실제 동작:

```text
Query
-> OpenAI Query Embedding
-> ticker와 document_type으로 MariaDB 후보 필터
-> Python에서 cosine similarity 계산
-> 날짜 metadata 필터
-> 뉴스 freshness score 결합
-> top_k 반환
```

뉴스 최종 점수:

```text
final_score =
similarity_score * 0.8
+ freshness_score * 0.2
```

뉴스 기본 freshness half-life:

```text
14일
```

현재는 모든 후보 벡터를 MariaDB에서 읽어 Python 메모리에서 유사도를 계산한다.
학습용으로는 단순하고 이해하기 쉽지만 데이터가 많아지면 느려진다.

## 6단계: 공시 Retrieval

```text
src/disclosure/disclosure_retriever.py
src/runtime_query/disclosure_retrieval_ranker.py
```

현재 `disclosure_retriever.py`는 Query Embedding을 만들지 않는다.

기본 점수:

```text
token overlap * 0.75
+ importance * 0.25
```

이후 report priority와 freshness가 추가되어 다시 정렬된다.

학습 시 반드시 구분할 점:

```text
공시 embedding 생성 성공
!=
공시 vector retrieval 사용
```

현재 공시 검색은 Lexical Retrieval에 가깝다.

## 7단계: Evidence 병합

```text
src/runtime_query/unified_retrieval_builder.py
src/runtime_query/runtime_evidence_merger.py
```

뉴스와 공시는 공통 필드로 정규화된다.

```text
chunk_id
document_type
ticker
score
text
chunk_text
source
priority
```

병합 점수:

```text
merge_score =
retrieval score * 0.7
+ source weight * 0.3
```

공시는 높은 source priority를 받는다. 규제기관 공시를 뉴스보다 강한 근거로 다루려는
의도는 좋지만, 뉴스 score와 공시 score의 의미가 서로 다르므로 그대로 비교하는 것은
정교한 calibration이라고 보기 어렵다.

## 8단계: Context Assembly

```text
src/rag/context/assembler.py
src/rag/context/formatter.py
src/rag/unified_engine/context_orchestrator.py
```

기본 Context 제한:

```text
최대 Chunk: 10개
최대 문자: 8,000자
```

Unified Context에는 다음 정보가 들어갈 수 있다.

```text
Retrieval Context
Event Graph
Temporal Memory
Stock Chain
Reflection
Layered Memory
```

현재 Retrieval Context는 최대 3,000자로 다시 잘리고, 각 보강 Context는 최대
1,500자로 제한된다.

## 9단계: Prompt와 LLM 분석

```text
src/rag/character/personas.py
src/rag/character/prompt_builder.py
src/rag/unified_engine/engine_runner.py
```

현재 기본 Chat 모델:

```text
gpt-4o-mini
```

Prompt는 다음 JSON 형식을 요구한다.

```json
{
  "bullish_factors": [],
  "bearish_factors": [],
  "risks": [],
  "summary": ""
}
```

좋은 학습 포인트:

- System Prompt와 User Prompt의 책임을 구분한다.
- Context 밖의 정보를 생성하지 말라는 규칙이 있다.
- 투자 추천과 확정 예측을 금지한다.
- Persona에 따라 분석 관점을 변경한다.

주의할 점:

- Prompt 규칙만으로 hallucination을 막을 수는 없다.
- JSON schema 기반 structured output이 아니라 문자열 JSON 파싱을 사용한다.
- OpenAI 실패 시 빈 dict를 반환하며 Runtime 상태 계약이 충분히 엄격하지 않다.

## 10단계: 평가와 Trace

```text
src/rag/evaluation/evaluator.py
src/rag/evaluation/metrics.py
src/rag/unified_engine/result_builder.py
data/unified_engine/
```

평가 항목:

```text
retrieval score 통계
문서 유형 분포
Context 문자열 overlap
응답 구조 완성도
단정 표현 사용 여부
hallucination 위험 추정
```

Trace 저장:

```text
data/unified_engine/final_results/{trace_id}_result.json
data/unified_engine/traces/{trace_id}_trace.json
data/unified_engine/engine_runs/{trace_id}_pipeline.json
```

Trace는 입력, 검색 결과 수, 단계 로그와 최종 결과를 연결해서 디버깅할 수 있게 한다.

---

# 4. 코드에서 잘된 부분

## 전체 RAG 단계를 직접 확인할 수 있다

수집, Chunk, Embedding, Retrieval, Context, Prompt, Evaluation이 각각 다른 모듈에
존재한다. RAG가 단순히 Vector DB 검색 하나로 끝나는 것이 아니라는 점을 학습하기 좋다.

## ticker 중심 필터가 명시적이다

금융 RAG에서는 다른 기업의 문서가 섞이는 것이 큰 오류다. 이 프로젝트는 뉴스 Retrieval
전에 ticker를 DB 필터로 적용한다.

```text
Query similarity 검색
전에
ticker 후보 제한
```

이는 검색 후 ticker를 걸러내는 것보다 안전한 방향이다.

## Raw 데이터와 처리 데이터를 구분하려는 구조가 있다

뉴스 원문, DB 문서, Chunk, Embedding, Runtime Result가 단계별로 나뉜다. 데이터가
어느 단계에서 잘못됐는지 추적하는 연습에 유용하다.

## 최신성 점수를 별도로 다룬다

금융 뉴스는 관련성만큼 날짜가 중요하다. 단순 cosine similarity에 freshness를 결합한
구조는 금융 RAG 학습에 좋은 사례다.

## 비용 방지 구조가 있다

```text
Embedding 중복 확인
Chunk hash cache
Batch 상한
비용 추정
Presentation mode
```

외부 AI API를 사용하는 시스템에서 비용이 아키텍처의 일부라는 점을 보여준다.

## Evidence를 결과와 함께 저장한다

Memory에 요약만 저장하지 않고 referenced chunk의 ticker, score, source, 본문 등을
보존한다. 나중에 분석 결과의 근거를 추적하기 좋다.

## Trace 중심으로 Dashboard를 연결한다

`trace_id`를 기준으로 Retrieval, Memory, Graph, Evaluation을 조회한다. 여러 분석
결과가 섞이는 문제를 줄이려는 설계다.

## 안전한 분석 Prompt가 있다

매수·매도 추천과 확정 예측을 제한하고 Context 기반 답변을 요구한다. 금융 AI에서
필요한 최소 안전 규칙을 확인할 수 있다.

---

# 5. 부족한 부분과 학습 시 주의점

## 자동 테스트가 없다

현재 Python과 Frontend에 정식 단위 테스트 또는 통합 테스트가 없다. 따라서 다음
문제를 코드 변경 전에 자동으로 잡기 어렵다.

```text
잘못된 corp_code
다른 ticker 데이터 혼입
0건 cache를 HIT로 처리
OpenAI 실패인데 completed 반환
Memory layer 중복
Frontend 수집과 조회 race
```

이 프로젝트로 학습한다면 테스트 추가를 가장 먼저 해보는 것이 좋다.

## 공시 Vector Retrieval이 연결되지 않았다

공시 embedding 테이블은 존재하지만 검색에서는 읽지 않는다. 이 부분은 RAG를 공부할
때 가장 좋은 개선 과제다.

목표 흐름:

```text
공시 Query Embedding
-> disclosure_embeddings 조회
-> cosine similarity
-> freshness와 report priority 결합
-> top_k
```

## 뉴스와 공시 score가 같은 척 병합된다

뉴스 score는 cosine similarity와 freshness 기반이고, 공시 score는 token overlap과
importance 기반이다. 두 점수의 확률적 의미가 다르지만 하나의 `merge_score`로 직접
비교된다.

개선 방향:

```text
source별 score normalization
또는
각 source의 top_k quota 보장
또는
통합 reranker 사용
```

## 모든 Embedding 후보를 애플리케이션 메모리로 읽는다

현재는 MariaDB에서 ticker 후보 Embedding을 모두 읽은 다음 Python에서 cosine
similarity를 계산한다.

소규모 학습 데이터에는 단순하고 좋지만, 문서가 많아지면 다음 문제가 생긴다.

```text
DB 전송량 증가
Python 메모리 증가
검색 지연 증가
동시 사용자 처리 어려움
```

대규모 단계에서는 Vector DB나 DB 내 vector index를 고려해야 한다.

## Timeout이 실행 중인 작업을 실제로 중단하지 않는다

Thread의 `Future.cancel()`은 이미 실행 중인 네트워크 요청이나 embedding 작업을
강제로 종료하지 못한다.

현재 Runtime은 timeout 응답을 받을 수 있지만 내부 작업은 계속 실행될 수 있다.

개선 방향:

```text
수집 작업을 별도 worker로 분리
job_id와 상태 저장
ticker별 lock 적용
중복 수집 방지
API 요청 자체 timeout 적용
```

## Unified Engine의 책임이 너무 많다

`run_unified_pipeline()`은 다음 작업을 모두 수행한다.

```text
Retrieval
Context Assembly
LLM Analysis
Evaluation
Reflection
Memory
Temporal Lifecycle
Event Graph
Stock Chain
Result 저장
```

학습할 때 흐름을 한눈에 보기에는 좋지만, 테스트와 실패 격리가 어렵다.

## import 구조가 불안정하다

여러 모듈이 `sys.path`를 변경한 뒤 짧은 모듈 이름으로 import한다.

```python
sys.path.insert(0, module_path)
from retriever import retrieve_similar_chunks
```

이 방식은 실행 위치에 따라 다른 모듈이 import될 수 있고 IDE와 테스트 도구의 분석을
어렵게 한다.

권장 방식:

```python
from src.rag.retrieval.retriever import retrieve_similar_chunks
```

## Runtime 성공 상태가 분석 성공을 보장하지 않는다

현재 최종 `completed` 판정은 Retrieval Chunk 수에 크게 의존한다. OpenAI 분석이
실패하여 summary가 비어 있어도 Chunk가 있으면 completed가 될 수 있다.

권장 상태:

```text
retrieval_completed
analysis_completed
memory_completed
overall_status
```

각 단계 상태를 분리하는 것이 좋다.

## Hallucination 평가는 휴리스틱이다

현재 평가는 단정 표현, Retrieval 평균 점수, 응답 구조, 긴 단어의 문자열 overlap을
사용한다.

이는 경고 지표로는 유용하지만 다음을 검증하지 못한다.

```text
각 주장에 실제 근거가 있는가
수치가 원문과 일치하는가
인용 문서가 해당 주장을 지원하는가
서로 충돌하는 문서를 처리했는가
```

## Memory와 RAG를 구분해야 한다

현재 Analysis Memory, Event Memory, Layered Memory, Temporal Memory가 있다. 하지만
Memory가 많다고 Retrieval 품질이 자동으로 좋아지는 것은 아니다.

학습 시 다음을 분리해서 생각해야 한다.

```text
문서 RAG: 외부 원문 검색
분석 Memory: 과거 분석 결과 재사용
Event Memory: 사건 단위 정보
Conversation Memory: 사용자 대화 문맥
```

## Dependency 재현성이 낮다

Python dependency 버전이 고정되지 않았고 실제 사용하는 `openai` 패키지가
`requirements.txt`에 명시되지 않았다. 다른 환경에서 같은 코드가 동일하게 실행된다는
보장이 약하다.

---

# 6. 코드 품질 학습 평가

| 학습 영역 | 적합도 | 설명 |
|---|---:|---|
| RAG 전체 흐름 이해 | 8/10 | 수집부터 LLM과 Trace까지 확인 가능 |
| Embedding과 cosine similarity | 8/10 | 직접 구현 흐름을 읽기 쉬움 |
| Metadata filtering | 8/10 | ticker와 날짜 필터가 명시적 |
| Freshness-aware Retrieval | 8/10 | 금융 도메인 특성을 반영 |
| Hybrid Retrieval | 6/10 | 뉴스와 공시가 다르지만 score calibration이 약함 |
| Prompt 설계 | 7/10 | Persona와 안전 규칙이 분리됨 |
| RAG Evaluation | 4/10 | 기본 지표만 있고 claim 검증은 부족 |
| 테스트 설계 학습 | 2/10 | 기존 테스트가 없어 직접 추가해야 함 |
| 프로덕션 운영 | 3/10 | 동시성, 인증, job 관리가 부족 |
| 개선 실습 프로젝트 | 9/10 | 실제 문제를 단계별로 개선하기 좋음 |

---

# 7. 추천 학습 실습

## 실습 1: Retrieval 결과 관찰

목표:

```text
Query가 바뀌면 검색 순위가 어떻게 바뀌는지 확인
```

확인 항목:

```text
chunk_id
similarity_score
freshness_score
final score
published_at
ticker
```

비교 Query 예:

```text
SK하이닉스 HBM
SK하이닉스 실적
SK하이닉스 공급망 위험
```

## 실습 2: ticker 필터 테스트

테스트 조건:

```text
선택 ticker: 000660
Query: 삼성전자 엔비디아 TSMC
```

검증:

```text
반환 Chunk의 ticker가 모두 000660인가
다른 ticker 문서가 섞이지 않는가
키워드가 근거 문서에 실제 존재하는가
```

이 실습은 Query와 문서 corpus의 차이를 이해하는 데 중요하다.

## 실습 3: 공시 Vector Retrieval 연결

가장 추천하는 실습이다.

구현 목표:

1. Query Embedding을 한 번 생성한다.
2. `disclosure_embeddings`와 `disclosure_chunks`를 조회한다.
3. cosine similarity를 계산한다.
4. lexical score와 vector score를 결합한다.
5. freshness와 report priority를 추가한다.
6. 기존 lexical 결과와 비교 평가한다.

예시 점수:

```text
final =
vector_similarity * 0.55
+ lexical_overlap * 0.15
+ report_priority * 0.15
+ freshness * 0.15
```

가중치는 정답이 아니며 평가 데이터로 조정해야 한다.

## 실습 4: Grounding 평가 추가

각 분석 문장을 claim으로 나눈다.

```text
분석 문장
-> 핵심 명사와 수치 추출
-> 근거 Chunk에서 동일 정보 검색
-> supported / partial / unsupported 분류
```

최소 평가 결과:

```json
{
  "claim": "최근 HBM 수요가 증가했다.",
  "support": "partial",
  "evidence_chunk_ids": [123, 456],
  "reason": "수요 증가 언급은 있으나 기간과 수치가 불명확함"
}
```

## 실습 5: 실패 상태 분리

다음 실패를 각각 재현한다.

```text
Embedding API 실패
Chat API 실패
DB 연결 실패
뉴스 0건
공시 0건
Context 0건
```

기대 상태를 명시한다.

```text
failed
partial
completed
cached
stale
timeout
```

## 실습 6: 자동 테스트 추가

첫 테스트 후보:

```text
query_builder가 ticker와 keywords를 보존하는가
retrieval 결과가 선택 ticker로 제한되는가
freshness score가 오래된 문서를 낮추는가
0건 disclosure cache가 HIT가 되지 않는가
OpenAI 실패 시 completed가 되지 않는가
Memory가 ticker와 keywords를 보존하는가
동일 memory_id가 여러 layer에 중복되지 않는가
Frontend가 수집 완료 후 공시를 재조회하는가
```

---

# 8. 추천 학습 순서

## 1주차: 기본 RAG

```text
Chunk
Embedding
cosine similarity
ticker filter
top_k
Context Assembly
```

코드:

```text
src/ingestion_pipeline/chunk_pipeline.py
src/ingestion_pipeline/embedding_pipeline.py
src/rag/retrieval/retriever.py
src/rag/context/assembler.py
```

## 2주차: 금융 RAG

```text
News TTL
Freshness score
OpenDART
공시 section chunk
뉴스와 공시 병합
```

코드:

```text
src/rag/retrieval/freshness.py
src/disclosure/
src/runtime_query/
```

## 3주차: 생성과 평가

```text
Persona Prompt
Structured JSON
Grounding
Hallucination 평가
Trace
```

코드:

```text
src/rag/character/
src/rag/evaluation/
src/rag/unified_engine/
```

## 4주차: 확장 기능

```text
Analysis Memory
Event Memory
Layered Memory
Temporal Memory
Event Graph
Stock Chain
```

기본 RAG 품질을 먼저 검증한 뒤 학습하는 것을 권장한다.

---

# 9. 실행하며 확인하는 방법

## Backend

```bash
python -m uvicorn src.dashboard_api.app:app --host 127.0.0.1 --port 8000
```

## Frontend

```bash
cd dashboard-ui
npm run dev
```

## Runtime Query

```bash
python -m src.runtime_flow.runtime_query_runner "SK하이닉스 HBM 실적"
```

## 주요 API

```text
POST /api/query/run
GET /api/retrieval/{trace_id}
GET /api/runtime/context/{trace_id}
GET /api/disclosure/{ticker}
GET /api/disclosure/search
GET /api/memory/{trace_id}
GET /api/evaluation/{trace_id}
```

## DB에서 확인할 핵심 테이블

```text
news_articles
dart_disclosures
document_chunks
document_embeddings
disclosure_documents
disclosure_chunks
disclosure_embeddings
```

---

# 10. 최종 판단

이 프로젝트는 RAG를 처음부터 직접 연결해 보는 학습 자료로는 가치가 있다.

특히 다음 질문에 답하면서 공부하기 좋다.

```text
왜 문서를 Chunk로 나누는가
Embedding은 어디에 저장되는가
Query와 문서의 similarity는 어떻게 계산되는가
Metadata filter는 왜 필요한가
금융 데이터에서 freshness가 왜 중요한가
검색 결과를 Prompt에 어떻게 넣는가
LLM 결과가 근거를 사용했는지 어떻게 확인하는가
Memory는 문서 RAG와 무엇이 다른가
실패를 completed로 처리하면 어떤 문제가 생기는가
```

다만 현재 코드를 그대로 모범 사례로 외우면 안 된다. 가장 좋은 사용법은 다음과 같다.

```text
현재 코드를 실행한다
-> trace와 DB를 관찰한다
-> 한계를 재현한다
-> 작은 테스트를 만든다
-> 한 단계씩 개선한다
-> 개선 전후 Retrieval 결과를 비교한다
```

즉, 이 코드는 완성된 교과서라기보다 실제로 작동하는 초안을 개선하며 배우는
실습 교재에 가깝다.
