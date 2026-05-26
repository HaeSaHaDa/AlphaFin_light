# TASK-012 결과 001

## 일시

2026-05-26

## 작업 결과

### 1. TASK-011 완료 처리

- 상태: DONE 변경 완료
- tasks/done/TASK-011-build-financial-analysis-flow.md 이동 완료

### 2. Embedding 품질 점검 (inspect)

- document_embeddings 총 행: 3
- 정상: 0
- 비정상: 3 (모두 더미 벡터)
  - chunk_id 1, 2, 3: 0.001 단위 순차 증가 패턴
- Embedding 미존재 chunk: 20 (chunk_id 4~23)
- 재생성 필요 총: 23 chunk

### 3. 문제 원인

TASK-008 실행 시 OpenAI API 쿼터 초과(insufficient_quota)로
실제 Embedding 생성이 불가했다.
파이프라인 검증을 위해 더미 벡터(0.001*i 시퀀스, dim=1536)를
chunk_id 1~3에 저장했다.
이후 TASK-007에서 추가 생성된 chunk_id 4~23은 Embedding이 없었다.

### 4. Embedding 재생성 (rebuild)

- 기존 더미 3건 삭제
- 23개 Chunk 전체 OpenAI Embedding 재생성
- 모든 API 호출: HTTP 200 OK
- 모든 chunk: dim=1536 정상
- 재생성 INSERT: 23/23건 성공

### 5. 재점검 결과

- document_embeddings 총 행: 23
- 정상: 23
- 비정상: 0
- Embedding 미존재: 0

### 6. Retrieval 재검증

**이전 (더미 벡터)**:
- 모든 Query에서 score ≈ -0.03
- 의미 기반 구별 불가

**이후 (실제 Embedding)**:

| Query | 최고 score | Top-1 chunk_id | Top-1 type |
|-------|-----------|---------------|------------|
| 삼성전자 반도체 실적 전망 | 0.4577 | 1 | news_article |
| HBM 수요 증가 | 0.3599 | 4 | news_article |
| AI 메모리 시장 성장 | 0.3460 | 9 | news_article |

**개선:**
- score: -0.03 → 0.35~0.46 (약 15배 이상 개선)
- 각 Query별 다른 Top-1 chunk 반환 (의미 기반 구별 정상)
- news_article + disclosure 혼합 결과 반환 (다양한 소스)

### 7. 완료 기준 점검

| 항목 | 상태 |
|------|------|
| document_embeddings 상태 검증 성공 | OK |
| embedding_vector 파싱 성공 | OK |
| invalid embedding 탐지 성공 | OK (더미 3건 + 미존재 20건) |
| OpenAI Embedding 재생성 성공 | OK (23/23) |
| document_embeddings 갱신 성공 | OK |
| Retrieval 재검증 성공 | OK |
| similarity score 개선 확인 | OK (-0.03 → 0.35~0.46) |
| 문제 원인 기록 | OK |
| TASK-011 done 이동 완료 | OK |
| prompts/TASK-012/prompt-001.md 저장 | OK |
| logs/TASK-012/result-001.md 기록 | OK |

### 8. 생성/수정 파일

```text
src/rag/embedding/inspect_embeddings.py (신규)
src/rag/embedding/rebuild_embeddings.py (신규)
tasks/done/TASK-011-build-financial-analysis-flow.md
prompts/TASK-012/prompt-001.md
logs/TASK-012/result-001.md
```
