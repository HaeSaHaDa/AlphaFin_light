# AlphaFin LTE 코드 의도 불일치 및 설계 모순 점검

## 문서 목적

이 문서는 AlphaFin LTE의 문서와 TASK에서 선언한 의도와 실제 코드 흐름을 비교하여,
의도대로 작동하지 않거나 잘못된 결과를 만들 가능성이 높은 부분을 정리한다.

이번 점검은 코드 수정이 아니라 Audit이다.

판정 기준:

```text
P0: 결과의 신뢰성을 직접 훼손하거나 잘못된 성공 상태를 만드는 문제
P1: 주요 기능이 의도와 다르게 동작하거나 회귀 가능성이 높은 문제
P2: 구조적 부채로 인해 유지보수와 검증을 어렵게 만드는 문제
```

---

# 1. P0: 분석 실패가 성공으로 기록될 수 있음

## 의도

```text
Retrieval 성공
-> LLM 분석 성공
-> Evaluation
-> Memory 저장
-> Runtime completed
```

## 실제 흐름

`src/rag/unified_engine/engine_runner.py`

```text
47-67:
Chat API 실패 시 예외를 기록하고 빈 dict 반환

181-195:
빈 dict로 summary가 없는 analysis_result 생성
character_analysis 상태는 warn

197-279:
Evaluation, Reflection, Memory, Graph, Stock Chain을 계속 실행
```

`src/runtime_query/runtime_query_pipeline.py`

```text
141-143:
retrieval_chunk_count가 1개 이상이면 engine_status = completed
```

`src/runtime_flow/runtime_query_runner.py`

```text
165-177:
retrieval chunk 수만으로 completed 판정
```

`src/rag/unified_engine/result_builder.py`

```text
117-123:
Pipeline Log status를 항상 completed로 저장
```

## 문제

OpenAI 호출이 실패하거나 분석 결과가 비어 있어도 Retrieval Chunk만 있으면 Runtime이
`completed`로 표시된다. 이후 빈 분석이 Memory와 Graph에 저장될 수 있다.

이 구조는 다음 두 상태를 구분하지 못한다.

```text
검색 성공
분석 성공
```

## 권장 방향

```text
retrieval_status
analysis_status
memory_status
graph_status
overall_status
```

단계 상태를 분리하고, 분석 실패 시 Memory와 Graph 저장을 중단해야 한다.

---

# 2. P0: 공시 cache가 본문 수집 완료를 의미하지 않음

## 의도

```text
공시 최신 여부 확인
-> 새 공시 본문 수집
-> Chunk
-> Embedding
-> cache HIT
```

## 실제 흐름

`src/runtime_query/disclosure_runtime_integration.py`

```text
41:
Runtime 자동 수집 시 body_limit=1
```

`src/disclosure/disclosure_cache.py`

```text
36-45:
fetched > 0 또는 chunks > 0이면 현재 body cache로 인정
```

`fetched`는 공시 목록 건수이며 본문 수집 성공 건수가 아니다. 기존 Chunk가 남아 있어도
cache가 정상으로 판정될 수 있다.

## 문제

다음 상태도 12시간 동안 HIT가 될 수 있다.

```text
공시 목록 80건
신규 본문 수집 0~1건
기존 Chunk 일부 존재
cache 상태 HIT
```

사용자에게 보이는 `Disclosure Updated`가 실제 본문 corpus의 완전성을 보장하지 않는다.

## 권장 방향

cache 판정에 다음 값을 포함한다.

```text
latest_receipt_no
latest_report_date
body_expected
body_collected
body_failed
chunked_document_count
embedded_chunk_count
```

새 공시의 `receipt_no`가 DB에 없거나 `raw_text`가 비어 있으면 cache를 완료 상태로
간주하지 않아야 한다.

---

# 3. P0: Dashboard 상세 메뉴가 존재하지 않는 DOM으로 이동함

## 의도

Dashboard 하위 메뉴:

```text
요약
뉴스
이벤트
근거
공시
그래프
메모리
평가
```

버튼을 누르면 같은 Dashboard의 해당 영역으로 스크롤해야 한다.

## 실제 흐름

`dashboard-ui/src/ui/action-policy.ts`

```text
21-29:
section-graph
section-memory
section-evaluation
```

를 Dashboard 섹션으로 선언한다.

그러나 `dashboard-ui/src/components/dashboard-client.tsx`는 현재 다음 영역만 렌더링한다.

```text
section-summary
section-news
section-events
section-runtime-evidence
section-disclosure
```

`section-graph`, `section-memory`, `section-evaluation`은 현재 Dashboard DOM에 없다.

## 문제

`RuntimeSectionNav.scrollToSection()`은 대상이 없으면 그대로 반환한다. 따라서 메뉴
버튼은 표시되지만 아무 동작도 하지 않는다.

## 권장 방향

현재 정보 구조를 기준으로 다음처럼 분리하는 것이 가장 명확하다.

```text
Dashboard 내부 스크롤:
- 요약
- 뉴스
- 이벤트
- 근거
- 공시

독립 Sidebar Route:
- Retrieval
- Graph
- Memory
- Evaluation
```

Dashboard에 독립 페이지 내용을 다시 넣지 않는다면 상세 메뉴에서도 제거해야 한다.

---

# 4. P1: 검색과 종목 선택 상태의 소유자가 둘 이상임

## 실제 구조

전역 Header:

```text
GlobalRuntimeSearch
-> 자체 query, keywords, selected 상태
-> RuntimeQueryProvider 실행
```

Dashboard:

```text
QueryExecutionPanel
-> useSelectedTicker()
-> 자체 searchText, keywords, selectedCompany 상태
-> RuntimeQueryProvider 실행
```

`useSelectedTicker()`는 전역 Store가 아니라 컴포넌트마다 독립적인 `useState` Hook이다.

## 문제

두 검색창이 같은 Runtime을 실행하지만 선택 상태와 키워드 상태는 공유하지 않는다.
Runtime 결과가 갱신되면 Dashboard 검색창은 session과 external ticker를 이용해 다시
hydrate하고, Header 검색창도 별도로 hydrate한다.

이 구조는 다음 현상을 만들 수 있다.

```text
새 기업을 입력하는 중 기존 기업명이 다시 채워짐
한 검색창에서 선택한 종목이 다른 검색창과 즉시 일치하지 않음
키워드가 두 입력창 사이에서 달라짐
드롭다운과 선택 해제 타이밍 충돌
```

## 권장 방향

종목 선택과 분석 키워드의 단일 상태 소유자를 정한다.

```text
RuntimeQueryProvider
-> draft company query
-> selected company
-> keywords
-> 실행 상태
```

Header 또는 Dashboard 중 하나만 편집 가능한 검색 UI로 두고, 다른 위치에는 현재 종목
정보만 표시하는 것이 안전하다.

---

# 5. P1: 한 개의 보조 API 실패가 전체 Dashboard 실패로 전파됨

`dashboard-ui/src/services/api.ts`

```text
412-420:
Retrieval, Reflection, Memory, Stock Chain, Trace, Evaluation을 Promise.all로 로드
```

`dashboard-ui/src/runtime-state/runtime-panel-loader.ts`

```text
20-23:
Dashboard와 Signal도 Promise.all로 로드
```

## 문제

Signal이나 Reflection처럼 보조적인 API 하나가 404 또는 500을 반환해도 전체 Panel
Load가 실패한다. 정상 Retrieval과 공시 데이터까지 화면에서 사라질 수 있다.

이는 안전한 fallback과 부분 결과 표시 의도에 반한다.

## 권장 방향

```text
필수:
- Retrieval
- Trace

선택:
- Reflection
- Memory
- Stock Chain
- Evaluation
- Signal
```

필수와 선택 패널을 구분하고, 선택 데이터는 `Promise.allSettled()` 또는 패널별 Error
Boundary로 처리한다.

---

# 6. P1: 공시 Embedding을 생성하지만 Retrieval에서 사용하지 않음

`src/disclosure/disclosure_embedder.py`

```text
공시 Chunk의 text-embedding-3-small 벡터를 생성하고 DB 저장
```

`src/disclosure/disclosure_retriever.py`

```text
Query와 Chunk를 공백·구두점 Token으로 분리
Token overlap 0.75 + importance 0.25
```

## 문제

공시 Embedding 생성 비용은 발생하지만 실제 검색 품질에는 기여하지 않는다.
`similarity_score`라는 이름도 실제로는 vector similarity가 아니라 token overlap이다.

다음 표현은 의미가 비슷해도 검색되지 않을 수 있다.

```text
영업이익 개선
수익성 회복

설비 투자 확대
CAPEX 증가
```

## 권장 방향

```text
vector similarity
+ lexical overlap
+ report priority
+ freshness
```

Hybrid Retrieval로 연결하거나, 연결 전까지 불필요한 자동 Embedding 생성을 중단해야
한다.

---

# 7. P1: 공시의 제목과 날짜가 LLM Context에서 누락될 수 있음

`src/disclosure/disclosure_retriever.py`는 다음 값을 최상위 필드로 반환한다.

```text
report_name
report_date
section_name
```

하지만 `src/rag/context/formatter.py`의 공시 Formatter는 다음 값을
`metadata_json`에서만 찾는다.

```text
published_at
report_name
```

## 문제

Runtime 공시 Chunk에 `metadata_json`이 없으면 Prompt에는 다음처럼 들어간다.

```text
date: unknown
report 이름 없음
content만 표시
```

DB와 API에는 공시 날짜와 제목이 있지만 LLM이 받는 Context에서는 사라진다. 이는
공시 Grounding과 최신성 판단을 약하게 만든다.

## 권장 방향

Formatter가 최상위 값을 먼저 읽고 metadata를 fallback으로 사용한다.

```text
date = report_date or published_at or metadata.published_at
report = report_name or metadata.report_name
```

---

# 8. P1: Context 제한 방식이 중요한 Chunk 전체를 탈락시킬 수 있음

`src/rag/context/assembler.py`

```text
57-61:
다음 Chunk를 추가하면 max_chars를 넘을 경우 break
```

## 문제

상위 1개 Chunk가 매우 크면 해당 Chunk뿐 아니라 뒤에 있는 작은 Chunk도 전부
포함되지 않는다.

```text
첫 Chunk: 9,000자
최대 Context: 8,000자
결과: 0개 Chunk
```

또한 `assembler`는 최대 8,000자를 만들지만
`src/rag/unified_engine/context_orchestrator.py`는 Retrieval Context를 다시 3,000자로
자른다.

```text
수집된 Context 8,000자
실제 Unified Context 반영 3,000자
```

이 이중 제한은 뉴스와 이벤트가 중간에서 잘려 보이는 현상과 분석 근거 손실로 이어질
수 있다.

## 권장 방향

```text
Chunk가 크면 남은 문자 수만큼 안전하게 자르기
너무 큰 Chunk를 건너뛰고 다음 Chunk 검토
section 경계 기반 압축
최종 Prompt token budget 한 곳에서 관리
```

---

# 9. P1: Memory의 반복 등장과 승격 로직이 과거 Memory를 보지 않음

`src/rag/unified_engine/engine_runner.py`

```text
238-240:
all_memories = [importance_mem]
현재 생성한 Memory 한 건만 전달
```

`src/rag/temporal_memory/temporal_tracker.py`

```text
44-50:
자기 자신은 비교에서 제외
```

## 문제

반복 등장을 판단할 비교 대상이 항상 비어 있게 된다. 따라서 과거 분석과의 재등장
횟수에 기반한 MID/LONG 승격은 의도대로 작동하기 어렵다.

## 추가 모순

같은 파일의 `EVOLUTION_CHAINS`에는 다음 반도체 Demo 패턴이 고정되어 있다.

```text
NVIDIA -> 실적 -> HBM -> 수요
HBM -> 공급 -> AI -> 메모리
```

이는 hardcoded stock chain 제거 의도와 충돌하며, 다른 기업 분석에서도 반도체 관련
장기 신호가 반복해서 나타날 수 있는 원인이 된다.

## 권장 방향

```text
현재 ticker의 과거 Memory 로드
-> 현재 Memory와 비교
-> 재등장 계산
-> 승격 판단
```

고정 산업 Chain 대신 Evidence 또는 Event Graph에서 동적으로 진화 경로를 생성해야
한다.

---

# 10. P1: Event ID와 날짜가 실제 사건의 시간성을 보존하지 못함

`src/event_consolidation/canonical_event_builder.py`

```text
event_id = hash(ticker + canonical_title)
```

`src/event_consolidation/event_consolidator.py`

```text
event_date = Runtime 실행 당일
```

`src/event_consolidation/event_repository.py`

```text
동일 event_id는 기존 Event를 UPDATE
```

## 문제

같은 제목의 사건이 다른 날짜에 반복되면 동일 Event로 합쳐질 수 있다.
또한 실제 뉴스·공시 날짜가 아니라 분석 실행 날짜가 Event 날짜가 된다.

예:

```text
2025년 공급계약 체결
2026년 별도 공급계약 체결
canonical title이 같으면 하나의 event_id로 충돌 가능
```

## 권장 방향

Event ID에 안정적인 시간 단위를 포함한다.

```text
ticker
+ normalized event type
+ canonical title
+ source event date 또는 date bucket
```

`event_date`는 Evidence의 대표 날짜를 사용해야 한다.

---

# 11. P1: 공시 수집이 Backend Runtime과 Frontend에서 중복 실행됨

Backend:

```text
run_disclosure_aware_query
-> integrate_disclosure_runtime
-> 공시 cache 확인 및 필요 시 수집
```

Frontend `DisclosurePanel`:

```text
기존 공시 조회
-> collectDisclosure()
-> 다시 조회
```

## 문제

Runtime 분석 직후 Dashboard가 같은 종목에 대해 다시 공시 수집을 요청한다.

```text
중복 OpenDART 호출
동시 Chunk/Embedding 작업
화면 조회와 수집의 race condition
Runtime에 사용된 공시와 화면에 표시된 공시의 시점 차이
```

## 권장 방향

수집 책임은 Backend Runtime 한 곳에 둔다. Frontend는 Runtime의 collect 상태를
표시하고, 명시적인 수동 새로고침에서만 강제 수집을 요청해야 한다.

---

# 12. P1: Memory 조회 API가 저장 파일을 수정함

`src/dashboard_api/services/memory_service.py`

```text
156-159:
Memory 조회 중 중복 검사
필요 시 repair_layer_duplicates() 실행
다시 조회
```

## 문제

GET 성격의 조회가 디스크 상태를 변경한다.

```text
화면을 열었을 뿐인데 Memory 파일 변경
동시 조회 시 race 가능
오류 원인과 수정 시점 추적 어려움
```

또한 Event Memory 조회 오류는 `except Exception: pass`로 숨겨진다.

## 권장 방향

```text
조회:
- 읽기와 화면용 dedupe만 수행

수리:
- 명시적인 maintenance 명령
- 변경 전후 로그
- dry-run 지원
```

---

# 13. P2: Trace ID가 초 단위라 충돌 가능

`src/rag/unified_engine/pipeline_manager.py`

```text
trace_id = YYYYMMDD_HHMMSS
```

동일 초에 두 Runtime이 실행되면 Result, Trace, Pipeline, Stock Chain 파일명이 겹칠 수
있다.

## 권장 방향

```text
YYYYMMDD_HHMMSS_microseconds
또는
UUID/ULID
```

사용자에게 보이는 짧은 ID가 필요하면 내부 ID와 표시용 ID를 분리한다.

---

# 14. P2: sys.path 조작이 모듈 경계를 불안정하게 만듦

다음 영역에서 실행 중 `sys.path`를 변경하고 짧은 모듈 이름으로 import한다.

```text
src/rag/unified_engine/
src/runtime_flow/
src/dashboard_api/services/memory_service.py
src/rag/temporal_memory/
```

## 문제

```text
실행 위치에 따른 다른 모듈 import 가능
IDE와 type checker가 실제 의존성을 추적하기 어려움
테스트 격리 어려움
동일 파일명의 모듈 충돌 가능
```

## 권장 방향

```python
from src.rag.retrieval.retriever import retrieve_similar_chunks
```

형태의 package import로 점진적으로 통일한다.

---

# 15. P2: Dashboard 뉴스는 원문이 아니라 제한된 미리보기만 표시함

`dashboard-ui/src/components/report-layout/RelatedNewsPanel.tsx`

```text
최대 6건만 표시
본문은 line-clamp-3 적용
```

이는 Dashboard 요약 UI로는 타당하지만, 별도의 전체 뉴스 상세 경로가 없다면 사용자는
Chunk 일부만 데이터 전체로 오해할 수 있다.

## 권장 방향

```text
Dashboard:
- 제목, 날짜, 짧은 preview

상세:
- 원문 링크
- 분석에 사용한 전체 Chunk
- 같은 기사의 인접 Chunk
- 해당 Chunk가 선택된 점수 근거
```

UI에서 `원문`, `검색 Chunk`, `LLM Context에 포함된 부분`을 구분해 표시해야 한다.

---

# 우선 수정 권장 순서

## 1단계: 결과 신뢰성

```text
1. Runtime 단계별 상태 계약
2. LLM 실패 시 Memory/Graph 저장 중단
3. completed 하드코딩 제거
4. 공시 body cache 완전성 판정
```

## 2단계: 사용자 회귀

```text
5. 존재하지 않는 Dashboard 상세 메뉴 제거
6. 검색 UI와 선택 상태 단일화
7. 패널 부분 실패 허용
8. 공시 중복 수집 제거
```

## 3단계: RAG 품질

```text
9. 공시 Vector Retrieval 연결
10. 공시 제목과 날짜 Context 복구
11. Context token budget 단일화
12. 실제 과거 Memory 기반 Temporal 계산
13. hardcoded 반도체 evolution chain 제거
```

## 4단계: 데이터 안정성

```text
14. Event ID와 source date 수정
15. Memory repair를 조회에서 분리
16. Trace ID 충돌 방지
17. package import 통일
```

---

# 최종 판단

현재 시스템의 가장 큰 문제는 기능이 전혀 없는 것이 아니다. 각 모듈은 상당 부분
구축되어 있지만 단계별 성공 조건과 상태 소유권이 분명하지 않아 다음 현상이 발생한다.

```text
검색 성공을 분석 성공으로 오인
목록 수집을 본문 수집 완료로 오인
Embedding 생성을 Vector Retrieval 연결로 오인
Dashboard 메뉴 정의를 실제 화면 구현으로 오인
현재 Memory 한 건 처리를 시간적 학습으로 오인
Chunk 존재를 충분한 Grounding으로 오인
```

따라서 다음 개발은 기능 추가보다 먼저 상태 계약, 데이터 완전성, 단일 상태 소유권,
검증 가능한 단계 경계를 정리하는 방향이 안전하다.
