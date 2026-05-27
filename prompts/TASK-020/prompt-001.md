# TASK-020 Prompt-001

## 작업

TASK-020-build-temporal-market-memory

## 목표

Memory의 시간 흐름(Temporal Evolution)을 추적하고 Short/Mid/Long-term Layer 이동을 수행하는 Temporal Market Memory 구축

## 수행 내용

- TASK-019 완료 처리 및 tasks/done/ 이동
- prompts/TASK-020/, logs/TASK-020/ 생성
- src/rag/temporal_memory/ 생성
  - temporal_tracker.py: 반복 등장, evolution stage, event chain 추적
  - decay_manager.py: decay 계산, temporal importance 보정
  - lifecycle_manager.py: promote/decay 수행, lifecycle log, Temporal Context
  - run_sample.py: 샘플 검증
- Layered Memory, Memory Importance, Reflection, Event Graph 연동
- NVIDIA/HBM/AI 장기 성장 샘플 Temporal 흐름 검증

## 환경

- Python 3.x
- 기존 layered_memory, memory_importance, reflection, event_graph 재사용
- data/temporal_memory/ 저장

## 샘플 Query

```text
NVIDIA 실적 발표
HBM 공급 부족
AI 산업 장기 성장
```

## 제외 범위

- Reinforcement Learning 금지
- Temporal GNN 금지
- Fully Autonomous Temporal Reasoning 금지
- Causal AI 금지
- 과도한 abstraction 금지
