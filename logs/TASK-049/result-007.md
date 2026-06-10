# TASK-049 Dashboard와 독립 페이지 책임 분리

## 발견된 문제

- Dashboard 내부 메뉴가 `window`를 스크롤했지만 실제 스크롤 영역은 `.runtime-shell-workspace`였다.
- 이 때문에 내부 메뉴 버튼을 눌러도 대상 섹션으로 이동하지 않았다.
- Dashboard에 Graph, Retrieval, Memory, Evaluation 전체 패널이 들어 있어 독립 사이드바 페이지와 중복됐다.
- Dashboard 하위 section과 독립 page의 등급 구분이 불명확했다.

## 최종 Navigation 구조

### 사이드바: 독립 페이지

```text
Dashboard  -> /
Retrieval  -> /analysis
Graph      -> /event-graph
Memory     -> /memory-timeline
Evaluation -> /signal-evaluation
```

### Dashboard 하위 메뉴

```text
요약   -> section-summary
뉴스   -> section-news
이벤트 -> section-events
근거   -> section-runtime-evidence
공시   -> section-disclosure
```

## 수정 내용

- Dashboard에서 Graph 전체 패널을 제거했다.
- Dashboard에서 Retrieval, Memory, Evaluation 전체 패널을 제거했다.
- 내부 메뉴를 Dashboard 하위 5개 section으로 축소했다.
- `scrollIntoView()`를 사용해 실제 workspace 내부에서 대상 section으로 이동하도록 수정했다.
- 활성 section 감지도 `window`가 아닌 `.runtime-shell-workspace`의 scroll 이벤트를 사용하도록 수정했다.

## 검증

```text
Dashboard 하위 메뉴 5개
Dashboard 중복 상세 section 0개
Retrieval route 200
Graph route 200
Memory route 200
Evaluation route 200
회사명 검색 정상
ticker 검색 정상
Frontend HTTP 200
Backend HTTP 200
npm run lint 성공
npx tsc --noEmit 성공
Frontend stderr 신규 오류 없음
```

인앱 Browser는 Windows sandbox 초기화 오류로 사용할 수 없어 실제 렌더링 HTML, route 응답, 스크롤 코드 경로로 대체 검증했다.
