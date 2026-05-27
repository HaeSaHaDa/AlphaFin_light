# TASK-017 결과 001

## 일시

2026-05-27

## 작업 결과

### 1. TASK-016 완료 처리

- 상태: DONE 변경 완료
- tasks/done/TASK-016-build-market-event-graph.md 이동 완료

### 2. 디렉토리 구조 생성

- src/rag/layered_memory/__init__.py 생성 완료
- src/rag/layered_memory/memory_classifier.py 생성 완료
- src/rag/layered_memory/layered_store.py 생성 완료
- src/rag/layered_memory/layered_retriever.py 생성 완료
- src/rag/layered_memory/run_sample.py 생성 완료

### 3. memory_classifier.py 구현

- `classify_memory_layer(memory)` — 시간 + 키워드 기반 Layer 분류
  - Short-term: 7일 이내 또는 단기 키워드 2개 이상
  - Long-term: 90일 초과 또는 장기 키워드 2개 이상
  - Mid-term: 나머지
- `calculate_importance_score(memory)` — 0.0~1.0 중요도 계산
  - HIGH_IMPACT_KEYWORDS 매칭 (최대 0.4)
  - 분석 구조 완전성 (최대 0.3)
  - referenced_chunks 수 (최대 0.2)
  - 시간 보너스 (최대 0.1)
- `is_expired(memory, layer)` — Short-term 7일, Mid-term 90일, Long-term 무기한

### 4. layered_store.py 구현

- `save_layered_memory(memory)` — 자동 분류 후 Layer별 저장
- `load_layer_memories(layer)` — Layer별 로드 (만료 필터링 지원)
- `load_all_layers()` — 전체 Layer 로드

### 5. layered_retriever.py 구현

- `retrieve_short/mid/long_term_memories(query)` — Layer별 keyword+importance 조회
- `retrieve_all_layers(query)` — 전체 Layer 조회
- `build_layered_context(layered_memories)` — [Short-term]/[Mid-term]/[Long-term] 구조 Context 생성

### 6. 검증 결과

#### Phase 1: 분석 + Layered Memory 저장

| Query | Layer | importance_score |
|-------|-------|-----------------|
| 삼성전자 반도체 전망 분석 | short_term | 0.9000 |
| HBM 시장 성장 | short_term | 1.0000 |

- 이벤트 Memory 4건 추가 저장 (score 0.1~0.4)
- 총 6건 short_term 저장

#### Phase 2: Layer 로드

| Layer | 건수 |
|-------|------|
| short_term | 6 |
| mid_term | 0 |
| long_term | 0 |

(당일 생성으로 모두 short_term 분류 — 정상 동작)

#### Phase 3: Layer별 Retrieval

| Layer | 건수 | 최고 retrieval_score |
|-------|------|---------------------|
| short_term | 2 | 0.4111 |
| mid_term | 0 | - |
| long_term | 0 | - |

#### Phase 4: Layered Context + 강화 분석

| 항목 | 결과 |
|------|------|
| Layered Context | 296자 |
| Enhanced Context | 4,324자 |
| 강화 분석 | bullish=2, bearish=2, risks=2 |

### 7. 최종 검증

| 항목 | 상태 |
|------|------|
| layer_storage | OK |
| importance_score | OK |
| layer_retrieval | OK |
| layered_context | OK |
| enhanced_analysis | OK |
| json_saved | OK |
| 최종 | OK |

### 8. 참고: Layer 분류 동작 설명

당일 생성된 Memory는 age=0일이므로 모두 short_term으로 분류됨.
시간이 경과하면:
- 7일 초과 시 short_term에서 만료
- mid_term 키워드 매칭으로 mid_term 분류
- 90일 초과 시 long_term 분류
이는 의도된 정상 동작임.

### 9. 생성 파일

```text
src/rag/layered_memory/__init__.py
src/rag/layered_memory/memory_classifier.py
src/rag/layered_memory/layered_store.py
src/rag/layered_memory/layered_retriever.py
src/rag/layered_memory/run_sample.py
data/layered_memory/short_term/growth_investor_short_term.json
data/layered_memory/short_term/default_short_term.json
data/layered_memory/samsung_layered_verification.json
tasks/done/TASK-016-build-market-event-graph.md
prompts/TASK-017/prompt-001.md
logs/TASK-017/result-001.md
```
