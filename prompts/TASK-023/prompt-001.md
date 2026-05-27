# TASK-023 Prompt-001

## 작업

TASK-023-build-engine-evaluation-suite

## 목표

Unified Financial AI Engine 전체를 정량·정성 검증하는 Engine Evaluation Suite 구축

## 수행 내용

- TASK-022 완료 처리 및 tasks/done/ 이동
- prompts/TASK-023/, logs/TASK-023/ 생성
- src/rag/evaluation_suite/ 생성
  - retrieval_evaluator.py, reasoning_evaluator.py, memory_evaluator.py
  - stock_chain_evaluator.py, score_aggregator.py, run_sample.py
- Unified Engine Result/Trace 재사용 기반 종합 평가
- Full Engine Score, Evaluation Report, Evaluation trace 저장
- 샘플 Query별 Retrieval 평가

## 환경

- Python 3.x
- data/unified_engine/ (TASK-022 결과) 재사용
- data/evaluation_suite/ 저장

## 샘플 Query

```text
삼성전자 반도체 전망 분석
HBM 공급 부족 영향
AI 서버 투자 확대
```

## 제외 범위

- RLHF / Reinforcement Learning 금지
- 실거래 성능 검증 금지
- LLM-as-a-judge 고도화 금지
- 과도한 abstraction 금지
