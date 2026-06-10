# TASK-048 Runtime Demo 및 Hardcoded Entry Point 제거 결과

## 수행 기준

- 수행일: 2026-06-09
- 범위: 필요 최소 수정
- 신규 기능, Schema 변경, Backtesting, Auto Trading, UI Redesign 없음

---

## 제거된 Demo 코드

1. `src/signal_evaluation/signal_history_manager.py`
   - `DEMO_OUTCOMES` 제거
   - `DEMO_TIMELINE` 제거
   - bullish `+3.5%`, neutral `+0.5%`, bearish `-2.8%` 고정 outcome 제거
   - demo outcome/timeline 조회 함수 제거

2. `src/signal_evaluation/signal_evaluator.py`
   - demo 시장 결과 기반 direction accuracy, hit ratio 계산 제거
   - timeline과 history에 고정 demo 데이터를 넣는 경로 제거
   - 실제 시장 결과가 없을 때 `actual_direction=unavailable`로 명시
   - 과거 demo signal cache는 재사용하지 않고 demo-free record로 다시 생성

3. `src/signal_evaluation/signal_summary.py`
   - 샘플 적중률 문구 제거
   - 실제 수익률 및 적중률을 제공하지 않는다는 문구로 변경

4. Dashboard Signal 표시
   - 시장 결과가 `unavailable`이면 `0%`, `+0%`, 방향 불일치를 실제 평가처럼 표시하지 않음
   - 현재 AI 관점과 실제 시장 평가 미연동 상태를 구분

---

## 제거된 Hardcoded 코드

1. `src/rag/stock_chain/chain_builder.py`
   - NVIDIA, HBM, 삼성전자, SK하이닉스 중심의 고정 공급망 관계 제거
   - 고정 industry 및 negative propagation relation 제거
   - Stock Chain은 Runtime entity를 담은 뒤 Event Graph relation만 병합

2. `src/rag/unified_engine/engine_runner.py`
   - `start_source="NVIDIA"` 제거
   - `propagate_market_impact(chain, "HBM")` 제거
   - propagation은 Runtime Event Graph에서 생성된 첫 relation을 기준으로 계산

3. 과거 Stock Chain 결과
   - 기존 저장 파일에서 고정 규칙 유래 link 523개가 확인됨
   - 실행 산출물 파일은 삭제하지 않음
   - Dashboard API 조회 시 `from_event_graph=true` link만 허용하여 과거 hardcoded relation 노출 차단
   - Event Graph link가 없으면 기존 retrieval 기반 안전 fallback 사용

4. Default ticker
   - Unified Engine과 pipeline state의 `005930` 기본값 제거
   - enhancement context의 `005930` fallback 제거
   - memory importance와 evaluation sample 함수의 기본 ticker 제거
   - ticker 누락 시 `ValueError`로 명확하게 실패

5. Default query
   - Runtime CLI의 `현대자동차 전기차 전망` 자동 입력 제거
   - query를 필수 positional argument로 변경

표준 실행:

```bash
python -m src.runtime_flow.runtime_query_runner "<회사명이 포함된 질문>"
```

---

## 통합된 Pipeline fallback

Frontend의 다음 중복을 제거했다.

```text
DEFAULT_PIPELINE
defaultPipeline()
normalizeTraceById()
```

현재는 `dashboard-ui/src/services/api.ts`의 다음 두 요소만 사용한다.

```text
PIPELINE_FALLBACK
normalizeTrace()
```

Dashboard와 Analysis Viewer가 동일한 pipeline 목록과 legacy trace normalize를 공유한다.

---

## 남겨둔 안전한 fallback

- OpenAI 실패 시 기존 graceful error/빈 분석 결과 처리
- retrieval 결과가 없을 때 partial/empty 상태
- Disclosure timeout 시 빈 공시 결과
- `/latest` 요청 차단
- traceId 및 selectedTicker 누락 시 명확한 오류
- Event Graph relation이 없는 Stock Chain의 retrieval 기반 최소 graph
- Frontend loading 및 empty state

---

## Runtime 위험 요소

1. 실제 시장 가격 outcome과 Backtesting은 아직 연결되지 않았다.
   - Signal은 AI 관점만 제공한다.
   - 정확도와 적중률은 의도적으로 unavailable 상태다.

2. 과거 signal 및 stock-chain JSON 파일은 디스크에 남아 있다.
   - Signal API는 과거 demo cache를 재생성한다.
   - Stock Chain API는 과거 고정 relation을 필터링한다.
   - API를 거치지 않고 파일을 직접 읽는 도구는 과거 데이터를 볼 수 있다.

3. Entity extractor의 NVIDIA, HBM, 삼성전자 등 keyword dictionary는 남아 있다.
   - Runtime 문서에서 실제 entity를 찾기 위한 사전이다.
   - 고정 relation 또는 propagation 시작점으로는 사용하지 않는다.

4. `python -m src.runtime_flow.runtime_query_runner`의 package 선행 import warning은 남아 있다.
   - query 필수화 동작에는 영향이 없지만 별도 TASK에서 정리할 수 있다.

5. 이번 TASK에서는 외부 OpenAI 호출을 포함한 전체 Runtime 실행을 하지 않았다.
   - TASK-049의 OpenAI 재검증 범위로 남긴다.

---

## 검증 결과

통과:

```text
Python compileall
Signal unavailable payload smoke test
과거 demo signal cache 재생성 smoke test
Event Graph 기반 Stock Chain smoke test
과거 hardcoded chain API filter smoke test
ticker 필수 입력 smoke test
Runtime CLI --help 및 query 필수 확인
npm.cmd run build
git diff --check
금지 문자열 재검색
```

Frontend production build 결과:

```text
Compiled successfully
Linting and checking validity of types 통과
Static page 8개 생성 통과
```

---

## 최종 판단

완료 조건을 모두 충족했다.

- Demo Signal 제거 완료
- Demo Timeline 제거 완료
- Demo Outcome 제거 완료
- Hardcoded Stock Chain 제거 완료
- Default ticker 제거 완료
- Default query 제거 완료
- Pipeline fallback 통합 완료
- 결과 로그 작성 완료

추천 다음 TASK:

```text
TASK-049-runtime-openai-recheck
```
