# TASK-011-build-financial-analysis-flow.md

# TASK-011 금융 분석 RAG Flow 구축

## 상태

DONE

---

# 목표

RAG Context 기반 LLM 금융 분석 Flow 구축.

---

# 완료 결과

- prompts.py 구현 (System Prompt + 분석 Prompt 생성)
- analyzer.py 구현 (Retrieval → Context → Chat API → 결과)
- run_sample.py 구현 (Prompt 검증 + 전체 분석 Flow 검증, 모두 OK)
- gpt-4o-mini 기반 삼성전자 금융 분석 성공
- bullish/bearish/risks/summary/referenced_chunks 정상 생성

---

# 관련 문서

```text
prompts/TASK-011/prompt-001.md
logs/TASK-011/result-001.md
```
