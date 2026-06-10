# TASK-051 최신성 기반 Runtime Retrieval 결과

## 적용된 TTL

뉴스와 공시 cache에 각각 12시간 TTL을 적용했다.

```text
News cache TTL: 12시간
Disclosure cache TTL: 12시간
```

- TTL 안이면 `HIT`로 기존 데이터를 사용한다.
- TTL이 지나면 Runtime 실행 전에 재수집한다.
- 뉴스 재수집이 실패하거나 0건이면 기존 cache 시각을 갱신하지 않고 `STALE`을 유지한다.
- 공시는 TTL 만료 시 OpenDART 목록, 본문, chunk, embedding을 다시 동기화한다.

실제 삼성전자 검증:

```text
기존 뉴스 cache: 2026-05-27 19:35:28, STALE
재수집 완료: 2026-06-10 10:06:16, REFRESHED
공시 cache: 2026-06-10 09:07:25, HIT
```

## Freshness Score 계산 방식

뉴스:

```text
최종 점수 = similarity 0.8 + freshness 0.2
freshness half-life = 14일
검색 날짜 범위 = 최근 90일
```

공시:

```text
최종 점수 =
relevance 0.4
+ report priority 0.25
+ importance 0.15
+ freshness 0.2

freshness half-life = 90일
검색 날짜 범위 = 최근 365일
```

각 결과에 다음 값을 보존한다.

```text
similarity_score
freshness_score
score 또는 rank_score
```

## Dashboard 표시 내용

Retrieval API와 Dashboard News 영역에 다음 정보를 연결했다.

```text
News Updated 기준 시각
Disclosure Updated 기준 시각
마지막 수집 시각
Cache HIT / REFRESHED / STALE
TTL 시간
```

검증 trace:

```text
trace_id: 20260610_100616
news data_as_of: 2026-06-10 10:03:42
news last_collected_at: 2026-06-10 10:06:16
news cache: REFRESHED
disclosure data_as_of: 2026-06-08
disclosure cache: HIT
```

`GET /api/retrieval/20260610_100616`에서 freshness payload와 11개 chunk 반환을 확인했다.

## Runtime 영향

- stale 뉴스 cache는 Runtime 시작 전에 자동 갱신된다.
- 새 뉴스 2건, chunk 4건, embedding 4건을 생성했다.
- Runtime Retrieval은 뉴스 6건과 공시 5건을 병합했다.
- 빈 뉴스 결과를 다시 검색하던 중복 호출을 제거했다.
- `src.runtime_flow.__init__`를 lazy import로 변경하여 module 실행 warning을 제거했다.
- `run_with_timeout`은 executor 종료를 기다리지 않고 즉시 fallback을 반환한다.

표준 실행 검증:

```bash
python -m src.runtime_flow.runtime_query_runner "삼성전자 최신 뉴스와 공시 분석"
```

결과:

```text
status: completed
trace_id: 20260610_100616
retrieval chunks: 11
```

## OpenAI 상태

```text
.env OPENAI_API_KEY: 설정 확인
Embedding model: text-embedding-3-small
Chat model: gpt-4o-mini
Embedding API: HTTP 200
Chat API: HTTP 200
Reflection Chat API: HTTP 200
```

API key 값 자체는 로그에 기록하지 않았다.

## 공시 본문 상태

삼성전자 기준:

```text
최신 report_date: 2026-06-08
raw_text 보유 문서: 101건
본문 연결 chunk: 107건
본문 연결 embedding: 107건
```

## 검증 결과

- Python compileall: 성공
- Frontend ESLint: 성공
- TypeScript `tsc --noEmit`: 성공
- Backend health: 정상
- Frontend localhost 응답: HTTP 200
- MariaDB 연결: 성공
- 실제 뉴스 자동 재수집: 성공
- OpenAI 최소 호출: 성공
- Runtime End-to-End: 성공
- Retrieval API freshness payload: 성공
- timeout 반환 시간: 0.053초
- Runtime module 실행 warning 제거: 성공

앱 내 브라우저는 Windows 샌드박스 초기화 오류로 연결되지 않아 시각적 브라우저
검증은 수행하지 못했다. 컴포넌트 정적 검증, Frontend 응답, API payload는 확인했다.

## 발견된 위험 요소

- 뉴스 수집 검색 결과에는 기업과 직접 관련성이 약한 기사가 포함될 수 있어 수집 단계의
  제목·본문 관련성 필터가 추가로 필요하다.
- 공시 신규 여부는 실시간 push가 아니라 12시간 TTL 만료 시 확인한다.
- 실행 중인 thread 작업은 Python에서 강제 종료할 수 없지만 호출자는 timeout 시 즉시
  fallback을 받는다.
- OpenAI 분석 실패가 최종 Runtime `completed` 상태에 직접 반영되지 않는 기존 계약은
  별도 TASK에서 정리해야 한다.
- 앱 내 브라우저의 시각 검증 환경 오류는 프로젝트 코드 오류와 분리해 확인해야 한다.
