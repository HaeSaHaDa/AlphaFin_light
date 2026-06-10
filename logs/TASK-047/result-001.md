# TASK-047 Hardcoded / Sample / Fallback 재점검 결과

## 수행 기준

- 수행일: 2026-06-09
- 범위: Audit Only
- 검색 대상: `src/`, `dashboard-ui/src/`
- 검색어: sample, mock, demo, fallback, latest, default, dummy, placeholder
- 종목 검색어: 삼성전자, 현대자동차, 005930, 005380, NVDA, NVIDIA, HBM, MLCC
- 코드, Schema, UI는 변경하지 않았다.

---

## 발견된 hardcoded 코드

### 즉시 Runtime에 영향을 주는 항목

1. `src/rag/unified_engine/engine_runner.py`
   - `run_unified_pipeline()`의 기본 ticker가 `005930`이다.
   - Stock Chain 전파 시작점을 항상 `NVIDIA`, 영향 시작점을 항상 `HBM`으로 사용한다.
   - selectedTicker가 현대자동차 등 다른 종목이어도 NVIDIA/HBM 전파 결과가 생성될 수 있다.

2. `src/rag/unified_engine/pipeline_manager.py`
   - pipeline state 생성 기본 ticker가 `005930`이다.

3. `src/rag/unified_engine/context_orchestrator.py`
   - state에 ticker가 없으면 `005930`을 사용한다.

4. `src/runtime_flow/runtime_query_runner.py`
   - CLI query 생략 시 `현대자동차 전기차 전망`을 실행한다.
   - 실수로 인자 없이 실행하면 특정 종목 trace, memory, graph가 실제 저장될 수 있다.

### 고정 지식 사전

1. `src/rag/stock_chain/chain_builder.py`
   - NVIDIA, GPU, AI 서버, HBM, 삼성전자, SK하이닉스, DRAM 중심의 정적 관계 규칙이 있다.
   - 실제 Runtime Stock Chain 생성에 사용되므로 다른 산업 종목 분석을 반도체 관계로 편향시킬 수 있다.

2. `src/rag/stock_chain/entity_extractor.py`
   - 삼성전자, SK하이닉스, NVIDIA, TSMC, Intel, Micron, AMD와 반도체 제품 키워드가 코드에 고정되어 있다.

3. `src/rag/event_graph/event_extractor.py`
   - 일부 회사 ticker 및 HBM 계열 키워드가 고정 사전으로 사용된다.

4. `src/company_resolver/company_registry.py`
   - 주요 6개 회사의 ticker/corp_code/alias가 정적 registry로 존재한다.
   - 회사 검색 master의 보조 경로로는 사용할 수 있으나 전체 종목 지원처럼 보이면 범위 오인이 발생한다.

5. `src/rag/memory_importance/importance_manager.py`
   - `load_event_graphs_all()` 기본 ticker가 `005930`이다.
   - 현재 확인된 직접 호출은 sample 스크립트이므로 핵심 Runtime 오염도는 낮다.

---

## 발견된 fallback

1. `src/dashboard_api/services/runtime_context_service.py`
   - 과거 trace에 `runtime_context`가 없으면 현재 시점의 뉴스 및 공시 retrieval을 다시 수행한다.
   - ticker/query는 해당 trace에서 가져오므로 종목 고정은 아니지만, 과거 trace 조회 결과가 시간에 따라 달라질 수 있다.
   - 조회 API가 OpenAI/DB/OpenDART 관련 작업을 다시 유발할 가능성도 있다.

2. `dashboard-ui/src/services/api.ts`
   - trace payload에 `pipeline_flow`가 없으면 `DEFAULT_PIPELINE`을 주입한다.

3. `dashboard-ui/src/components/trace/engine-trace-viewer.tsx`
   - 데이터의 pipeline이 없을 때 별도의 `defaultPipeline()`을 표시한다.

4. `dashboard-ui/src/hooks/use-analysis-viewer.ts`
   - legacy trace를 정규화하며 또 다른 고정 pipeline 목록을 넣는다.

Frontend의 세 pipeline fallback은 목록이 서로 달라, 실제 실행되지 않은 단계를 실행된 구조처럼 표시할 수 있다.

---

## 발견된 sample

- `src/` 아래 `run_sample.py` 또는 `run_db_sample.py`가 21개 존재한다.
- 수집, 전처리, RAG, Memory, Event Graph, Stock Chain, Evaluation, Dashboard API 예제가 포함된다.
- 다수 파일이 삼성전자, `005930`, NVIDIA, HBM 또는 고정 mock context를 사용한다.
- 일반 Runtime 모듈에서 sample runner를 import하는 경로는 발견되지 않았다.
- `src/dashboard_api/run_sample.py`는 비활성화된 `/latest`가 성공한다고 가정하므로 현재 정책과 불일치한다.

Dashboard component에서 sample card나 mock financial panel이 Runtime payload 대신 사용되는 경로는 발견되지 않았다.

---

## 제거가 필요한 코드

우선 제거 또는 격리 후보:

1. `src/signal_evaluation/signal_history_manager.py`의 `DEMO_OUTCOMES`, `DEMO_TIMELINE` 및 방향별 고정 수익률
2. `src/rag/unified_engine/engine_runner.py`의 고정 `NVIDIA`/`HBM` 전파 시작점
3. Unified Engine 계층의 `005930` 기본 ticker
4. Runtime CLI의 현대자동차 기본 query
5. 서로 다른 Frontend pipeline fallback 3종
6. 차단된 `/latest`용 service 함수와 import
7. 현재 정책과 반대인 `src/dashboard_api/run_sample.py`
8. 21개 sample runner의 유지 필요성 검토 및 테스트/예제 영역 격리

이번 TASK는 Audit Only이므로 위 코드는 수정하지 않았다.

---

## 즉시 위험한 코드

### 1. Signal Evaluation demo 결과

`src/signal_evaluation/signal_evaluator.py`는 실제 `/api/signal/{trace_id}` 경로에서
`get_market_outcome()`과 `get_demo_timeline()`을 호출한다.

그 결과 실제 시장 가격을 조회하지 않고:

- bullish: `+3.5%`
- neutral: `+0.5%`
- bearish: `-2.8%`
- 2024년 고정 demo timeline

을 사용하여 direction accuracy와 hit ratio를 계산하고 저장한다.
이는 실제 평가 지표처럼 노출되는 가장 높은 위험 항목이다.

### 2. selectedTicker와 무관한 Stock Chain 전파

Unified Engine은 실제 Runtime에서 항상 `NVIDIA`와 `HBM`을 전파 기준으로 사용한다.
선택 종목이 반도체와 무관해도 Stock Chain 결과가 오염될 수 있다.

### 3. 인자 없는 Runtime 실행

표준 명령을 query 없이 실행하면 현대자동차 기본 query가 실행된다.
명령 실수가 실제 trace와 memory를 만드는 운영 위험이 있다.

---

## 안전한 fallback

1. `src/runtime_query/disclosure_timeout_guard.py`
   - 공시 retrieval timeout 또는 예외 시 빈 목록이나 timeout 상태를 반환한다.
   - 가짜 공시를 만들지 않고 ticker를 유지하므로 graceful degradation으로 판단한다.

2. `/api/*/latest` route guard
   - retrieval, reflection, memory, stock-chain, trace, evaluation, signal의 `/latest` 요청은 400으로 차단된다.
   - 임의의 최신 trace를 다른 selectedTicker에 연결하지 않으므로 안전하다.

3. Frontend의 빈 `selectedTicker`/`traceId` 초기값
   - 특정 종목이나 trace를 자동 주입하지 않으므로 안전하다.

4. UI loading fallback 및 input placeholder
   - 표시 상태와 안내 문구일 뿐 Runtime payload를 위조하지 않는다.

5. KOSPI200 seed fallback
   - pykrx 로드 실패 시 로컬 종목 master seed를 사용한다.
   - 실제 종목 데이터 seed이며 sample payload는 아니지만, seed 최신성은 별도 운영 점검 대상이다.

---

## 영역별 판단

- Runtime: selectedTicker 전달 구조는 있으나 Unified Engine 기본값과 CLI 기본 query가 남아 있다.
- Graph: Event Graph는 Runtime text 기반이다. Stock Chain은 반도체 고정 규칙과 전파 시작점의 영향을 받는다.
- Memory: Analysis/Layered Memory는 Runtime 결과 기반이다. placeholder memory 주입은 발견되지 않았다.
- Event: canonical event는 Runtime evidence 기반이다. sample event의 Runtime 직접 주입은 발견되지 않았다.
- Disclosure: Runtime ticker 기반이며 timeout fallback은 빈 결과다. default disclosure 주입은 발견되지 않았다.
- Dashboard: 금융 값의 sample card/mock panel은 발견되지 않았다. pipeline 단계 표시 fallback은 실제 trace와 불일치할 수 있다.

---

## 최종 판단

TASK-047의 점검 조건은 충족했다.

다음 기능 개발 전 최소 선행 작업은 다음과 같다.

```text
1. Signal Evaluation demo 시장 결과를 실제 결과 연동 전까지 비활성 또는 명시적 unavailable 상태로 전환
2. Stock Chain의 NVIDIA/HBM 고정 전파 제거 및 selectedTicker/runtime entity 기반 전환
3. Runtime/Unified Engine의 특정 ticker 및 query 기본값 제거
4. Frontend pipeline fallback 단일화 또는 backend trace 없음을 명시
5. stale /latest sample 및 legacy service 정리
```

추천 다음 TASK:

```text
TASK-048-remove-runtime-demo-signal-and-hardcoded-stock-chain-entrypoints
```

이 정리 전에도 일반 Runtime 실행은 가능하지만, Signal Evaluation과 Stock Chain 결과를 실제 검증 결과로 신뢰해서는 안 된다.
