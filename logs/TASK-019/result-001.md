# TASK-019 Result-001

## 실행 일시

2026-05-27

## 실행 결과

### 구현 모듈

| 파일 | 역할 |
|------|------|
| importance_calculator.py | importance_score, factor 계산, reuse/event/reflection 보정 |
| importance_manager.py | importance 업데이트, ranking, retrieval 우선순위, JSON 저장 |
| retention_policy.py | promote/decay/high_retention 판단 |
| run_sample.py | 전체 흐름 검증 스크립트 |

### 검증 흐름

```text
Phase 1: Importance 계산
  - Layered Memory 7건 + 샘플 4건 로드
  - Reflection 1건, Event Graph 1건 연동
  - NVIDIA/HBM/AI 메모리 → score=1.0 (high_retention)
  - 단기 루머 → score=0.0 (decay)

Phase 2: Importance Ranking
  - NVIDIA 실적 발표 rank=1 (score=1.0)
  - 단기 루머 rank=11 (score=0.0)

Phase 3: Retrieval 우선순위
  - "HBM 공급 부족" → HBM 메모리 priority=0.60 (최상위)
  - "NVIDIA 실적 발표" → NVIDIA 메모리 priority=0.61

Phase 4: Retention 정책
  - promote: NVIDIA, HBM, AI 메모리, Reflection(mid→long) 등
  - decay: 단기 루머(score=0.0), 저점수 short_term 메모리

Phase 5: Layered Memory 연동
  - sample_importance_verification.json 저장 (3건)
  - importance_verification_summary.json 저장
```

### 검증 항목

| 항목 | 결과 |
|------|------|
| importance_score_generated | OK |
| importance_factors | OK |
| importance_ranking | OK |
| high_importance_nvidia | OK |
| low_importance_rumor | OK |
| retrieval_priority | OK |
| promote_judgment | OK |
| decay_judgment | OK |
| reflection_boost | OK |
| layered_memory_linked | OK |

### 최종 결과

**OK** — 전 항목 통과

### Importance Factor 예시 (NVIDIA 실적)

```json
{
  "base_score": 0.375,
  "market_impact": 0.16,
  "reuse_score": 0.12,
  "event_impact": 0.05,
  "reflection_boost": 0.05,
  "character_weight": 0.05,
  "importance_score": 1.0
}
```

### 비고

- 높은 importance 메모리는 raw_total이 1.0을 초과하여 cap=1.0 적용
- 낮은 importance(루머/일회성)는 low_importance_penalty로 score 감소 및 decay 대상
- Reflection 연동 시 reflection_mentions > 0 이면 reflection_boost 적용
- layered_store 저장 시 기존 classifier score와 별도로 memory_importance 모듈 score 유지
