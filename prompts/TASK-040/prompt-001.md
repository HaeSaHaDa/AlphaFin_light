# TASK-040 Prompt 001

## 목표

Disclosure Document Store 구축 및 공시 기반 runtime retrieval/evidence를 초기 통합한다.

## 수행

- `src/disclosure/*` 모듈 추가
  - OpenDART 공시 수집
  - disclosure_documents/chunks/embeddings/events 테이블 생성 및 저장
  - 공시 chunking/embedding/retrieval/timeline/evidence 처리
- Disclosure API 추가
  - `POST /api/disclosure/collect`
  - `GET /api/disclosure/{ticker}`
  - `GET /api/disclosure/search`
  - `GET /api/disclosure/timeline/{ticker}`
  - `GET /api/disclosure/evidence/{traceId}`
- Dashboard Disclosure Panel 추가
  - 문서 목록/필터
  - 타임라인
  - trace 기반 evidence
- Market reasoning evidence에 disclosure 근거 문자열 연결

## 검증

- 공시 저장/조회 응답
- selectedTicker 기반 공시 isolation
- 대시보드 공시 패널 표시
- trace 기반 disclosure evidence 응답
