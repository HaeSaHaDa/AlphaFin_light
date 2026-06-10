# TASK-051 후속 수정 결과: 종목별 OpenDART 공시 복구

## 작업 일자

```text
2026-06-10
```

## 확인된 문제

- SK하이닉스 공시 cache가 `completed` 상태였지만 실제 수집 결과는 0건이었다.
- 공시 0건인 cache도 12시간 동안 정상 `HIT`로 처리되어 재수집되지 않았다.
- SK하이닉스에 SK 지주사의 OpenDART 기업코드가 잘못 연결되어 있었다.
- KOSPI200 seed 50개 중 24개 종목의 OpenDART 기업코드가 공식 목록과 달랐다.
- 프런트엔드는 공시 수집 요청을 기다리지 않고 목록을 조회했으며, 수집 완료 후 목록과 타임라인을 다시 조회하지 않았다.
- `company_master` 시작 동기화 중 `src.common.db.store`의 package import가 실패할 수 있었다.

## 수정 내용

### OpenDART 기업코드

OpenDART 공식 `corpCode.xml`을 기준으로 seed를 대조하고 잘못된 기업코드 24개를 수정했다.

주요 수정 예:

```text
SK하이닉스 000660: 00181751 -> 00164779
삼성SDI 006400: 00164779 -> 00126362
삼성전기 009150: 00126362 -> 00126371
LG생활건강 051900: 00188421 -> 00356370
삼성화재 000810: 00126256 -> 00139214
SK 034730: 00181751 -> 00181712
```

수정 후 전체 seed 50개를 공식 OpenDART 목록과 다시 비교했다.

```text
seed_count: 50
mismatch_count: 0
```

### Cache 판정

다음 조건을 만족하지 않는 공시 cache는 정상 cache로 인정하지 않도록 수정했다.

```text
fetched > 0
또는
chunks > 0
```

따라서 `completed`, `fetched=0`, `chunks=0` 상태는 `HIT`가 아니라 `STALE`로 처리되고 다음 실행에서 다시 수집된다.

### 프런트엔드 갱신

공시 화면은 다음 순서로 동작하도록 수정했다.

```text
기존 공시 목록과 타임라인 조회
-> OpenDART cache 확인 및 필요 시 수집
-> 수집 완료 후 목록과 타임라인 재조회
```

최초 조회에서 404 또는 0건이 반환되더라도 수집 완료 후 화면이 다시 갱신된다.

### DB 동기화

`src.common.db.store`가 package import와 직접 실행 import를 모두 지원하도록 연결 모듈 import를 수정했다.

수정된 seed를 `company_master`에 다시 적재했으며 SK하이닉스 등 표본 종목의 기업코드가 DB에 반영된 것을 확인했다.

## 실제 수집 결과

### SK하이닉스

```text
ticker: 000660
corp_code: 00164779
공시 목록 수집: 100건
본문 수집: 1건
본문 길이: 1,095자
공시 chunk: 105건
embedding: 105건
API 표시 문서: 80건
최신 공시일: 2026-06-09
공시 Retrieval: 5건
```

### LG전자

```text
ticker: 066570
공시 목록 수집: 73건
본문 수집: 1건
본문 길이: 46,038자
공시 chunk: 144건
embedding: 144건
API 표시 문서: 73건
최신 공시일: 2026-06-01
공시 Retrieval: 5건
```

### 추가 표본

```text
LG생활건강 051900: 64건
삼성화재 000810: 83건 수집, API 80건 표시
삼성SDI 006400: 66건
```

DB의 `ticker + corp_code` 분포를 확인한 결과, 현재 저장된 표본 공시는 모두 수정된 공식 기업코드와 일치했다.

## API 검증

```text
GET /api/disclosure/000660: 200, document_count=80
GET /api/disclosure/066570: 200, document_count=73
GET /api/disclosure/search?ticker=000660: chunk 5건
GET /api/disclosure/search?ticker=066570: chunk 5건
GET /health: 200
```

## 실행 검증

- Python `py_compile`: 성공
- TypeScript `npx tsc --noEmit`: 성공
- Backend 재시작: 성공
- Frontend `http://localhost:3000`: HTTP 200
- MariaDB 연결 및 `company_master` 적재: 성공
- OpenDART 공식 기업코드 전체 대조: 성공
- SK하이닉스 공시 목록, 본문, chunk, embedding 생성: 성공
- LG전자 0건 cache 자동 재수집: 성공

## 수정된 파일

```text
data/kospi200/kospi200_seed.json
src/company_resolver/company_registry.py
src/common/db/store.py
src/disclosure/disclosure_cache.py
dashboard-ui/src/components/disclosure/DisclosurePanel.tsx
```

실행 검증 과정에서 다음 cache 파일도 갱신되었다.

```text
data/disclosure_cache/000660.json
data/disclosure_cache/066570.json
```

## 남아있는 위험 요소

- 최초 공시 본문 수집과 embedding 생성은 종목에 따라 1분 이상 걸릴 수 있다.
- Runtime 자동 공시 수집은 timeout 이후 백그라운드 작업이 잠시 계속될 수 있다.
- 현재 자동 Runtime 수집의 `body_limit`은 응답 시간을 제한하기 위해 1건이다.
- 기존에 한 번도 선택하지 않은 종목은 첫 선택 시 공시 store를 생성해야 한다.
- pykrx의 KRX 요청이 실패하면 seed fallback을 사용하며, startup 로그에 pykrx 오류 stack이 기록될 수 있다.
