# TASK-029 Prompt-001

## 작업

TASK-029-build-signal-evaluation-system

## 목표

Unified Engine 분석 결과에서 bullish/neutral/bearish Signal을 생성하고,
실제(샘플) 시장 결과와 비교해 Direction Accuracy, Hit Ratio, Confidence Evaluation을 수행.

## 수행 내용

### 백엔드 (`src/signal_evaluation/`)
- signal_generator.py — 긍정/중립/부정 Signal + confidence
- direction_accuracy.py — 방향 예측 정확도 · Hit Ratio
- confidence_evaluator.py — 분석 신뢰도 평가
- signal_history_manager.py — JSON 저장/조회
- signal_evaluator.py — 평가 오케스트레이션
- signal_summary.py — API 요약 페이로드

### API
- GET /api/signal/latest
- GET /api/signal/{trace_id}

### 프론트 (`dashboard-ui/src/components/signal-evaluation/`)
- SignalPanel, SignalHistory, SignalTimeline
- AccuracyPanel, ConfidencePanel, EvaluationSummary
- `/signal-evaluation` 페이지

## 용어

- bullish → 긍정, neutral → 중립, bearish → 부정
- confidence → 분석 신뢰도
- direction accuracy → 방향 예측 정확도
- hit ratio → 예측 적중률

## 제외

- 자동 매매 · Broker API · 실시간 주문 금지
