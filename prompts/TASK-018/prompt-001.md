# TASK-018 Prompt-001

## 작업

TASK-018-build-reflection-layer

## 목표

이전 금융 분석 결과를 재검토하는 Reflection Layer 구축

## 수행 내용

- TASK-017 완료 처리 및 tasks/done/ 이동
- prompts/TASK-018/, logs/TASK-018/ 생성
- src/rag/reflection/ 생성
  - prompt_builder.py: Reflection Prompt 생성
  - reflection_analyzer.py: Reflection 분석 (LLM + 규칙 기반)
  - reflection_store.py: Reflection 저장/조회/Context 생성
  - run_sample.py: 샘플 검증 스크립트
- 과거 분석 조회 → Evaluation 결과 조회 → Reflection Prompt 생성 → Reflection Analysis → Reflection Memory 저장 → 재분석 Context 강화
- 삼성전자/HBM 관련 샘플 Reflection 검증

## 환경

- Python 3.x
- OpenAI gpt-4o-mini
- MariaDB (document_embeddings)
- .env 기반 키 관리

## 샘플 Query

```text
삼성전자 반도체 전망 분석
```

## Reflection 관점

```text
- 과도한 낙관 여부
- 과도한 비관 여부
- 리스크 누락 여부
- 근거 부족 여부
- Context 부족 여부
- 시장 변화 반영 여부
```

## 제외 범위

- Reinforcement Learning 금지
- Autonomous Self-improvement 금지
- Fine-tuning 금지
- Recursive Reflection Loop 금지
- 과도한 abstraction 금지
