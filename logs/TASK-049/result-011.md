# TASK-049 전체 화면 chunk 노출 점검 결과

## 점검 범위

- Dashboard
- Runtime Evidence
- News
- Event
- Disclosure
- Stock Chain
- Market Graph
- Memory
- Retrieval
- Source Trace

## 발견한 부적절한 chunk 노출

### Runtime Evidence

- `[공시] chunk #251`
- `[뉴스] chunk #236`

### Stock Chain

- `disclosure #251`
- `news_article #236`

### Market Graph

- 노드 이름이 `disclosure #251` 형태로 표시됐다.
- 관계 근거가 `retrieval:disclosure#251` 형태로 표시됐다.

## 수정

- trace의 Runtime merged evidence에서 제목, 출처, 발행일, URL을 공통 복원한다.
- Runtime Evidence는 chunk ID 대신 뉴스·공시 제목을 표시한다.
- Stock Chain fallback 노드는 chunk ID 대신 기사·공시 제목을 사용한다.
- Market Graph 노드와 관계 근거도 기사·공시 제목을 사용한다.
- 프런트 fallback도 제목과 문서 첫 줄을 우선하도록 변경했다.

## 유지한 chunk 표시

다음 화면은 retrieval 동작과 source trace를 진단하는 전용 화면이므로 chunk 단위 표시를 유지했다.

- Retrieval 상세
- Chunk Ranking
- Similarity Score
- Source Trace

뉴스 카드와 공시 근거의 본문 미리보기는 chunk 식별자를 노출하는 것이 아니라 문서 내용을 미리 보여주는 용도이므로 유지했다.

## 실제 API 검증

trace `20260609_154829` 기준:

- `/api/runtime/evidence/{trace_id}`: chunk 식별자 없음
- `/api/stock-chain/{trace_id}`: chunk 식별자 없음
- `/api/market-graph/{trace_id}`: chunk 식별자 없음
- 공시 제목과 뉴스 기사 제목으로 표시됨

## 정적 검증

- Python compileall 통과
- Frontend lint 통과
- TypeScript 검사 통과
- Backend health `200`
- Frontend route `200`

## TASK 파일

이번 작업에서는 `tasks/` 아래 파일을 수정하거나 이동하지 않았다.
