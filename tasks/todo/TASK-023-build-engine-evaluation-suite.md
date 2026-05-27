# TASK-023-build-engine-evaluation-suite.md

# TASK-023 Engine Evaluation Suite 구축

## 상태

TODO

---

# 목표

Unified Financial AI Engine 전체를
정량적·정성적으로 검증할 수 있는
Engine Evaluation Suite를 구축한다.

현재 TASK의 목표는
단순 실행 성공 여부를 넘어,
엔진의 Retrieval 품질,
Reasoning 품질,
Reflection 품질,
Memory 품질,
Stock Chain 품질을
종합적으로 평가 가능한 구조를 만드는 것이다.

현재 단계에서는
복잡한 benchmark automation보다
명시적이고 추적 가능한 evaluation pipeline에 집중한다.

---

# 배경

현재 프로젝트는 다음 흐름까지 구축 완료되었다.

```text
수집
→ 저장
→ Chunking
→ Embedding
→ Semantic Retrieval
→ Context Assembly
→ Financial Analysis
→ Evaluation
→ Character Layer
→ Memory Layer
→ Market Event Graph
→ Layered Memory
→ Reflection
→ Memory Importance
→ Temporal Market Memory
→ Stock Chain
→ Unified Engine Runner
```

현재 시스템은:

```text
End-to-End 실행
```

까지 가능하다.

하지만 현재 구조는:

```text
엔진 품질을 체계적으로 측정
```

하지 않는다.

현재 TASK에서는
엔진 품질을 정량화하고,
각 단계의 품질을 검증 가능한 구조를 만든다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Engine Evaluation 디렉토리 구조 생성
- Retrieval 품질 평가 구현
- Context 품질 평가 구현
- Reflection 품질 평가 구현
- Memory 품질 평가 구현
- Stock Chain 품질 평가 구현
- hallucination risk 평가 구현
- consistency score 계산 구현
- Full Engine Score 생성 구현
- Evaluation Report JSON 생성 구현
- 샘플 Evaluation 실행 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- Human RLHF
- Reinforcement Learning
- Fine-tuning
- Auto Benchmark Optimization
- Online Evaluation Learning
- Real-world Trading Benchmark
- Sharpe Ratio 기반 투자 검증
- 실거래 성능 검증
- Autonomous AI Self-improvement
- LLM-as-a-judge 고도화
- Multi-agent debate evaluation

현재 TASK는
정적 Evaluation Suite만 구현한다.

---

# 생성 대상 구조

```text
src/rag/evaluation_suite/
├─ __init__.py
├─ retrieval_evaluator.py
├─ reasoning_evaluator.py
├─ memory_evaluator.py
├─ stock_chain_evaluator.py
├─ score_aggregator.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/evaluation_suite/
├─ reports/
├─ traces/
└─ scores/
```

예상 저장 파일 예시:

```text
data/evaluation_suite/reports/hbm_analysis_report.json
data/evaluation_suite/scores/full_engine_score.json
```

---

# Evaluation 역할

현재 Evaluation 역할:

- Retrieval 품질 평가
- Context relevance 평가
- Reflection 품질 평가
- hallucination risk 평가
- Memory consistency 평가
- Stock Chain reasoning 평가
- Full Engine Score 생성

---

# Evaluation 대상

현재 Evaluation 대상:

```text
- Retrieval
- Context Assembly
- Character Analysis
- Financial Analysis
- Reflection
- Memory Layer
- Temporal Memory
- Event Graph
- Stock Chain
- Unified Result
```

---

# Retrieval 평가 기준

현재 Retrieval 평가 기준:

```text
- relevance
- chunk diversity
- semantic similarity
- context coverage
- retrieval reuse quality
```

---

# Reasoning 평가 기준

현재 Reasoning 평가 기준:

```text
- bullish/bearish balance
- risk coverage
- evidence consistency
- hallucination risk
- reasoning trace consistency
```

---

# Reflection 평가 기준

현재 Reflection 평가 기준:

```text
- missing_risk detection
- overconfidence detection
- context gap detection
- reflection usefulness
```

---

# Memory 평가 기준

현재 Memory 평가 기준:

```text
- importance consistency
- temporal consistency
- promotion validity
- decay validity
- retrieval reuse consistency
```

---

# Stock Chain 평가 기준

현재 Stock Chain 평가 기준:

```text
- entity consistency
- propagation consistency
- relation quality
- chain continuity
```

---

# Full Engine Score 목표

예상 점수 구조:

```json
{
  "retrieval_score": 0.82,
  "reasoning_score": 0.79,
  "reflection_score": 0.76,
  "memory_score": 0.81,
  "stock_chain_score": 0.84,
  "overall_score": 0.80
}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Unified Engine 재사용
- 기존 Trace 재사용
- 기존 Reflection 재사용
- 기존 Temporal Memory 재사용
- 기존 Stock Chain 재사용
- evaluation trace 유지
- score 계산 추적 가능성 유지
- 작은 함수 유지
- 과도한 abstraction 금지
- 자율 투자 판단 금지

---

# Evaluation 흐름

현재 목표 흐름:

```text
Unified Engine 실행
→ Retrieval 평가
→ Reasoning 평가
→ Reflection 평가
→ Memory 평가
→ Stock Chain 평가
→ hallucination risk 계산
→ consistency score 계산
→ Full Engine Score 생성
→ Evaluation Report 저장
```

---

# Evaluation Report 목표

예상 Report 흐름:

```text
[Retrieval]
관련성 높음
Context coverage 양호

[Reasoning]
bullish 편향 존재
리스크 coverage 부족

[Reflection]
공급 과잉 리스크 탐지 성공

[Memory]
mid-term promotion 적절

[Stock Chain]
HBM 공급망 propagation 정상
```

---

# 예상 Evaluation 구조

예상 반환 형태:

```json
{
  "query": "...",
  "retrieval_score": 0.82,
  "reasoning_score": 0.79,
  "reflection_score": 0.76,
  "memory_score": 0.81,
  "stock_chain_score": 0.84,
  "overall_score": 0.80,
  "hallucination_risk": "low"
}
```

---

# 예상 기능

## retrieval_evaluator.py

역할:

- Retrieval 품질 평가
- relevance 평가

예상 함수:

```text
evaluate_retrieval(result)
calculate_context_coverage(result)
```

---

## reasoning_evaluator.py

역할:

- Reasoning 품질 평가
- hallucination risk 평가

예상 함수:

```text
evaluate_reasoning(result)
detect_hallucination_risk(result)
```

---

## memory_evaluator.py

역할:

- Memory consistency 평가
- temporal consistency 평가

예상 함수:

```text
evaluate_memory_consistency(result)
evaluate_temporal_consistency(result)
```

---

## stock_chain_evaluator.py

역할:

- Stock Chain 품질 평가
- propagation consistency 평가

예상 함수:

```text
evaluate_stock_chain(chain)
evaluate_propagation(chain)
```

---

## score_aggregator.py

역할:

- 전체 score 통합
- overall score 생성

예상 함수:

```text
aggregate_scores(scores)
build_engine_score_report(scores)
```

---

## run_sample.py

역할:

- 샘플 Engine Evaluation 실행
- Full Score 검증
- Evaluation Report 검증

샘플 Query 예시:

```text
삼성전자 반도체 전망 분석
HBM 공급 부족 영향
AI 서버 투자 확대
```

---

# Evaluation 활용 목표

현재 활용 목표:

```text
- 엔진 품질 검증
- reasoning 품질 개선
- Reflection 품질 개선
- Memory lifecycle 검증
- Stock Chain 품질 검증
```

현재 단계에서는
자동 투자 판단을 수행하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Retrieval 검증

- retrieval_score 생성 여부
- relevance 평가 여부
- context coverage 평가 여부

---

## Reasoning 검증

- reasoning_score 생성 여부
- hallucination risk 평가 여부
- reasoning consistency 평가 여부

---

## Reflection 검증

- reflection_score 생성 여부
- missing_risk 평가 여부
- overconfidence 평가 여부

---

## Memory 검증

- memory_score 생성 여부
- temporal consistency 평가 여부
- promotion validity 평가 여부

---

## Stock Chain 검증

- stock_chain_score 생성 여부
- propagation consistency 평가 여부
- entity consistency 평가 여부

---

## Full Engine 검증

- overall_score 생성 여부
- Full Report 저장 여부
- Evaluation trace 저장 여부

---

## 구조 검증

- `src/rag/evaluation_suite/` 생성 여부
- `data/evaluation_suite/` 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-023/
```

---

# 관련 Logs

```text
logs/TASK-023/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Engine Evaluation Suite 구축 완료
- Full Engine Score 생성 성공
- Evaluation Report 저장 성공
- hallucination risk 평가 성공
- consistency score 생성 성공
- overall_score 생성 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-024-build-dashboard-backend-api
- TASK-025-build-dashboard-ui
- TASK-026-build-retrieval-analysis-viewer

단,
현재 TASK에서는
자율 투자 Agent를 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- End-to-End 추적 가능성 유지
- Retrieval 기반 분석 유지
- Memory lifecycle 유지
- Reflection 기반 개선 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지