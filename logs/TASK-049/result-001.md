# TASK-049 Navigation 및 Search Runtime Regression 수정 결과

## 수행 기준

- 수행일: 2026-06-09
- 범위: Regression Fix Only
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:3000`

---

## 발견된 Regression

1. Sidebar `Retrieval` 메뉴가 실제 `section-retrieval`이 아니라
   `section-evaluation`으로 연결되어 있었다.

2. TASK-044 Navigation 정리 후 Header에서 종목 검색, 종목 선택,
   분석 실행 진입점이 사라지고 현재 종목 표시만 남아 있었다.

3. Header에서 새 분석을 실행해도 기존 URL의 `trace_id`가 우선되어,
   새 trace가 route 화면과 Sidebar 링크에 반영되지 않을 수 있었다.

4. 새로고침 또는 trace URL 직접 진입 시 session의 trace 메타만 복원하고
   Dashboard panel 데이터는 자동으로 다시 로드하지 않았다.

5. 검증 중 실행 중인 `next dev`와 `next build`가 동일한 `.next`를 사용하여
   `Cannot find module './611.js'` 500 오류가 발생했다.
   코드 오류가 아니라 개발 서버 cache 충돌이었으며 cache 정리와 dev 서버
   재시작으로 복구했다.

---

## 수정된 코드

### `dashboard-ui/src/navigation/global-navigation-map.ts`

- Retrieval href를 `/#section-retrieval`로 수정
- active section key를 `retrieval`로 수정

### `dashboard-ui/src/components/runtime-header/GlobalRuntimeSearch.tsx`

- Header의 compact 종목 검색 입력 복구
- company search API 기반 명시적 종목 선택 복구
- 분석 키워드 입력과 분석 실행 버튼 복구
- 선택된 ticker만 `/api/query/run`에 전달
- 기존 selectedTicker hydration 유지
- 새 Runtime trace 생성 후 현재 route의 URL을 새 traceId로 교체

### `dashboard-ui/src/layout/runtime-shell/RuntimeHeader.tsx`

- Header에 `GlobalRuntimeSearch` 연결

### `dashboard-ui/src/runtime-state/runtime-query-context.tsx`

- URL `trace_id` 또는 저장 session trace로 진입할 때 panel 자동 로드
- session과 trace가 일치하면 selectedTicker, companyName, runtimeQuery 복원
- 다른 trace URL이면 API 결과에서 ticker 메타를 다시 확정

---

## 복구된 기능

### Sidebar

다음 메뉴의 실제 href와 HTTP 200을 확인했다.

```text
Dashboard  → /?trace_id=20260609_124221
News       → /?trace_id=20260609_124221#section-news
Disclosure → /?trace_id=20260609_124221#section-disclosure
Graph      → /event-graph?trace_id=20260609_124221
Memory     → /memory-timeline?trace_id=20260609_124221
Evaluation → /signal-evaluation?trace_id=20260609_124221
Retrieval  → /?trace_id=20260609_124221#section-retrieval
```

모든 메뉴가 traceId를 유지했으며 404와 빈 route는 발생하지 않았다.

### Header

렌더 결과에서 다음 컨트롤을 확인했다.

```text
종목 검색
분석 키워드
분석 실행
```

company search 확인:

```text
GET /api/company/search?q=009150 → 200
```

### Runtime

고정 ticker 없이 명시적으로 선택한 종목으로 실행했다.

```text
ticker  : 009150
company : 삼성전기
keyword : MLCC
```

결과:

```text
POST /api/query/run → completed
trace_id            → 20260609_124221
runtime_query       → 삼성전기 009150 MLCC
retrieval chunks    → 5
AI summary 생성     → 성공
```

### API

생성 trace 기준:

```text
/api/runtime/dashboard/{trace_id} → 200
/api/runtime/context/{trace_id}   → 200
/api/events/{trace_id}            → 200
/api/disclosure/evidence/{trace_id} → 200
/api/retrieval/{trace_id}         → 200
/api/reflection/{trace_id}        → 200
/api/memory/{trace_id}            → 200
/api/stock-chain/{trace_id}       → 200
/api/trace/{trace_id}             → 200
/api/evaluation/{trace_id}        → 200
/api/signal/{trace_id}            → 200
/api/runtime-status/{trace_id}    → 200
```

### 화면 렌더

- Dashboard trace route 5회 연속 HTTP 200
- Graph, Memory, Evaluation route HTTP 200
- News, Disclosure, Retrieval section route HTTP 200
- Frontend와 Backend 최종 HTTP 200
- Next.js production build와 TypeScript 검사 통과
- 무한 로딩을 유발하는 API 실패 없음

---

## 남아있는 문제

1. 인앱 Browser 자동화가 Windows sandbox 초기화 오류로 두 번 중단되어
   실제 포인터 클릭 검증은 수행하지 못했다.
   렌더된 href, Header control, HTTP route, API E2E로 대체 검증했다.

2. `GET /api/disclosure/009150`은 신규 `disclosure_documents` 저장소가 비어 있어
   404를 반환했다.
   Runtime retrieval에는 기존 DART disclosure chunk 4건이 포함됐고
   `/api/disclosure/evidence/{trace_id}`는 200이었다.
   OpenDART 신규 수집 실패는 Navigation/Search 회귀가 아닌 외부 수집 이슈다.

3. 실행 중인 `next dev`와 같은 디렉터리에서 `next build`를 동시에 수행하면
   `.next` chunk 충돌이 발생할 수 있다.
   최종 검증에서는 cache 정리 후 dev 서버만 실행하여 정상 상태를 확인했다.

---

## 검증 결과

```text
npm.cmd run build 통과
Python compileall 통과
git diff --check 통과
Frontend HTTP 200
Backend HTTP 200
Dashboard 반복 렌더 5/5 성공
selectedTicker 기반 Runtime completed
traceId 생성 및 결과 파일 저장 확인
전체 Dashboard panel API 성공
```

TASK-049 완료 조건을 충족했다.
