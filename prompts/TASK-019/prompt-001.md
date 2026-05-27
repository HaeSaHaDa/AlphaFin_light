# TASK-019 Prompt-001

## 작업

TASK-019-build-memory-importance-system

## 목표

Memory Importance System 구축 — 중요 Memory 식별, Ranking, Retrieval 우선순위, Retention 정책

## 수행 내용

- TASK-018 완료 처리 및 tasks/done/ 이동
- prompts/TASK-019/, logs/TASK-019/ 생성
- src/rag/memory_importance/ 생성
  - importance_calculator.py: importance_score, reuse_score, event_impact, Reflection 보정
  - importance_manager.py: update, rank, retrieval 우선순위, 저장
  - retention_policy.py: promote/decay 판단
  - run_sample.py: 샘플 검증
- Layered Memory, Reflection, Event Graph 연동
- NVIDIA/HBM/AI 메모리 샘플 Importance 검증

## 환경

- Python 3.x
- 기존 Layered Memory / Reflection / Event Graph 재사용
- data/memory_importance/ 저장

## 샘플 Query

```text
NVIDIA 실적 발표
HBM 공급 부족
AI 메모리 시장 성장
```

## 제외 범위

- Reinforcement Learning 금지
- Self-learning Importance 금지
- Attention 기반 Importance 금지
- Dynamic Neural Scoring 금지
- 과도한 abstraction 금지
