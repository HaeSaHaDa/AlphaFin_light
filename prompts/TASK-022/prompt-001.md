# TASK-022 Prompt-001

## 작업

TASK-022-build-unified-engine-runner

## 목표

모든 RAG 엔진 구성 요소를 연결하는 End-to-End Unified Engine Runner 구축

## 수행 내용

- TASK-021 완료 처리 및 tasks/done/ 이동
- prompts/TASK-022/, logs/TASK-022/ 생성
- src/rag/unified_engine/ 생성
  - pipeline_manager.py: Pipeline 단계·trace 관리
  - context_orchestrator.py: Unified Context 조립
  - result_builder.py: Unified Result·Trace 저장
  - engine_runner.py: End-to-End 실행
  - run_sample.py: 샘플 검증
- Retrieval → Analysis → Reflection → Memory → Importance → Temporal → Event Graph → Stock Chain 통합
- 삼성전자 반도체 전망 분석 샘플 E2E 검증

## 환경

- Python 3.x, OpenAI gpt-4o-mini
- MariaDB (document_embeddings)
- data/unified_engine/ 저장

## 샘플 Query

```text
삼성전자 반도체 전망 분석
```

## 제외 범위

- Multi-agent orchestration 금지
- Distributed processing 금지
- Autonomous Trading Agent 금지
- 과도한 abstraction 금지
