# TASK-029-build-signal-evaluation-system.md

# TASK-029 Signal Evaluation System 구축

## 상태

TODO

---

# 목표

Financial AI Engine이 생성한
시장 분석 결과를 기반으로:

```text
긍정
중립
부정
```

Signal을 생성하고,
실제 시장 결과와 비교 평가하는
Signal Evaluation System을 구축한다.

현재 TASK의 목표는
단순 분석 결과 표시를 넘어,
AI 분석이 실제 시장 방향성과 얼마나 일치했는지
정량적으로 평가하는 것이다.

현재 단계에서는
복잡한 자동 투자 시스템보다
설명 가능한 Signal Evaluation에 집중한다.

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
→ Engine Evaluation Suite
→ Dashboard Backend API
→ Dashboard UI
→ Retrieval & Analysis Viewer
→ Event Graph Visualization
→ Memory Timeline Visualization
```

현재 시스템은:

```text
설명 가능한 금융 AI 분석
```

까지 가능하다.

하지만 현재 구조는:

```text
실제 시장 방향성과의 비교 평가
```

를 수행하지 않는다.

현재 TASK에서는
AI 분석 Signal을 생성하고,
실제 시장 결과와 비교 평가한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Signal Generator 구현
- bullish/neutral/bearish Signal 생성 구현
- confidence score 생성 구현
- Signal Evaluation Engine 구현
- Direction Accuracy 계산 구현
- Hit Ratio 계산 구현
- Confidence Evaluation 구현
- Signal History 저장 구현
- Signal Comparison Panel 구현
- 실제 가격 변화 비교 구현
- Signal Timeline Visualization 구현
- Evaluation Summary Panel 구현
- 샘플 Signal Evaluation 검증
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 실제 자동 매매
- 주문 API 연동
- HTS/MTS 연동
- Broker API 연동
- 실시간 매매 Signal
- 강화학습 기반 투자
- Portfolio Optimization
- 고빈도 매매
- Quant 전략 자동 생성
- Reinforcement Trading Agent
- 실시간 시장 주문 실행

현재 TASK는
설명 가능한 Signal Evaluation만 구현한다.

---

# 생성 대상 구조

```text
src/signal_evaluation/
├─ signal_generator.py
├─ signal_evaluator.py
├─ signal_history_manager.py
├─ direction_accuracy.py
├─ confidence_evaluator.py
└─ signal_summary.py
```

```text
dashboard-ui/src/components/
├─ signal-evaluation/
│  ├─ SignalPanel.tsx
│  ├─ SignalHistory.tsx
│  ├─ SignalTimeline.tsx
│  ├─ AccuracyPanel.tsx
│  ├─ ConfidencePanel.tsx
│  └─ EvaluationSummary.tsx
```

---

# Signal 역할

현재 Signal 역할:

- 시장 방향성 표현
- bullish/bearish 판단 표현
- AI confidence 표현
- 시장 결과 비교 기준 제공
- 발표용 평가 지표 제공

---

# Signal 구조

현재 Signal 구조:

```json
{
  "signal": "bullish",
  "display_label": "긍정",
  "confidence": 0.82,
  "reason": [
    "HBM 수요 증가",
    "AI 서버 투자 확대",
    "메모리 가격 상승 기대"
  ]
}
```

---

# Signal 종류

현재 Signal 종류:

| Signal | 의미 |
|---|---|
| bullish | 긍정 |
| neutral | 중립 |
| bearish | 부정 |

---

# Confidence 역할

현재 Confidence 역할:

- AI 분석 확신도 표현
- reasoning consistency 표현
- retrieval confidence 반영
- reflection 결과 반영

---

# Evaluation 역할

현재 Evaluation 역할:

- 방향성 정확도 계산
- 실제 가격 변화 비교
- Signal 적중률 계산
- Confidence 신뢰도 평가

---

# Evaluation 예시

예상 흐름:

```text
2024-01-01
삼성전자 bullish signal 생성

↓

2024-01-08
주가 +4.2%

↓

direction_correct = true
```

---

# Direction Accuracy 목표

예상 계산:

```text
bullish signal
+
실제 가격 상승
=
정답
```

---

# Hit Ratio 목표

예상 계산:

```text
총 Signal: 100
정확한 방향 예측: 68

Hit Ratio: 68%
```

---

# Confidence Evaluation 목표

예상 계산:

```text
confidence: 0.91
실제 방향 일치

→ high confidence success
```

---

# Signal Timeline 목표

예상 표시:

```text
2024-01
bullish

↓

2024-02
neutral

↓

2024-03
bearish
```

---

# UI 레이아웃 목표

예상 레이아웃:

```text
┌────────────────────────────────┐
│ Signal Summary                 │
├────────────────────────────────┤
│ Signal Timeline                │
├────────────────┬───────────────┤
│ Accuracy Panel │ Confidence    │
├────────────────┴───────────────┤
│ Signal History                 │
└────────────────────────────────┘
```

---

# Dashboard 역할

현재 Dashboard 역할:

- 현재 AI Signal 표시
- Signal 변화 흐름 표시
- 시장 결과 비교 표시
- 평가 지표 표시
- 발표용 explainability 강화

---

# API 연동 대상

현재 API 연동 대상:

```text
GET /api/evaluation/{trace_id}
GET /api/signal/latest
GET /api/signal/{trace_id}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Evaluation Suite 재사용
- 기존 Unified Engine 재사용
- 기존 Dashboard UI 재사용
- trace_id 기반 조회 유지
- 설명 가능한 Signal 유지
- 발표용 readability 우선
- 한국어 친화적 UI 유지
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## signal_generator.py

역할:

- Signal 생성
- bullish/bearish 판단

예상 기능:

```text
generate_signal()
calculate_confidence()
```

---

## signal_evaluator.py

역할:

- 실제 결과 비교
- 정확도 계산

예상 기능:

```text
evaluate_direction()
calculate_hit_ratio()
```

---

## direction_accuracy.py

역할:

- 방향성 평가

예상 기능:

```text
check_direction_match()
```

---

## confidence_evaluator.py

역할:

- confidence 평가

예상 기능:

```text
evaluate_confidence_quality()
```

---

## SignalPanel.tsx

역할:

- 현재 Signal 표시

예상 표시:

```text
현재 관점:
긍정
confidence: 82%
```

---

## AccuracyPanel.tsx

역할:

- direction accuracy 표시

예상 표시:

```text
Direction Accuracy:
68%
```

---

## SignalTimeline.tsx

역할:

- signal 변화 흐름 표시

예상 표시:

```text
bullish
→ neutral
→ bearish
```

---

# 한국어 UI 목표

현재 용어:

| 내부 용어 | 사용자 표현 |
|---|---|
| bullish | 긍정 |
| neutral | 중립 |
| bearish | 부정 |
| confidence | 분석 신뢰도 |
| direction accuracy | 방향 예측 정확도 |
| hit ratio | 예측 적중률 |

---

# Visualization 활용 목표

현재 활용 목표:

```text
- AI 시장 판단 설명
- 실제 시장 결과 비교
- 방향성 평가
- 발표용 성능 검증
- Explainable AI 강화
```

현재 단계에서는
실제 자동 투자 시스템을 구현하지 않는다.

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Signal 생성 검증

- bullish 생성 여부
- neutral 생성 여부
- bearish 생성 여부

---

## Confidence 검증

- confidence 계산 여부
- confidence 표시 여부

---

## Accuracy 검증

- direction accuracy 계산 여부
- hit ratio 계산 여부

---

## Timeline 검증

- signal timeline 표시 여부
- signal history 표시 여부

---

## Dashboard 검증

- Signal Panel 표시 여부
- Accuracy Panel 표시 여부
- Summary Panel 표시 여부

---

## API 검증

- signal API 연동 여부
- evaluation API 연동 여부

---

## 구조 검증

- signal_evaluation 구조 생성 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-029/
```

---

# 관련 Logs

```text
logs/TASK-029/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Signal Evaluation System 구축 완료
- Signal 생성 성공
- Direction Accuracy 계산 성공
- Hit Ratio 계산 성공
- Confidence Evaluation 성공
- Signal Timeline 구축 성공
- 발표 가능한 성능 평가 확보
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-030-build-portfolio-backtesting-suite
- TASK-031-build-sector-expansion-system
- TASK-032-build-real-market-monitoring-dashboard

단,
현재 TASK에서는
실제 자동 투자 시스템을 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- End-to-End traceability 유지
- Explainable Signal 유지
- Memory lifecycle 유지
- 발표 가능한 evaluation 유지
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지