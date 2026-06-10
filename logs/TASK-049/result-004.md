# TASK-049 Navigation 전체 연결 후속 수정

## 발견된 문제

- 사이드바가 route와 Dashboard section을 서로 다른 기준으로 활성화했다.
- URL hash가 Runtime layout의 `currentSection`과 초기 동기화되지 않았다.
- 상세 화면에서 Dashboard로 복귀하면 이전 section 상태가 남았다.
- Graph section anchor가 패널 상태에 따라 렌더링되지 않았다.
- 사이드바 Retrieval과 내부 Retrieval이 같은 section 이동을 담당해 상세 Analysis route 연결이 불명확했다.
- Memory 상세 화면에는 Dashboard 복귀 링크가 없었다.

## 수정 내용

- pathname과 `currentSection`을 하나의 active key로 변환해 사이드바 활성 항목을 하나로 제한했다.
- Dashboard 진입 시 hash가 없으면 Summary, hash가 있으면 해당 section으로 동기화했다.
- 내부 메뉴는 실제 DOM 순서와 동일한 9개 section을 사용한다.
- Graph anchor를 항상 렌더링되는 외부 래퍼로 이동했다.
- 로딩 중에도 내부 section anchor를 유지했다.
- 사이드바 Retrieval은 `/analysis` 상세 route로 연결했다.
- 내부 Retrieval에는 Analysis 상세 보기 링크를 추가했다.
- Memory 상세 화면에 trace를 유지하는 Dashboard 복귀 링크를 추가했다.

## 메뉴 연결

```text
내부 메뉴:
요약 -> section-summary
뉴스 -> section-news
이벤트 -> section-events
근거 -> section-runtime-evidence
공시 -> section-disclosure
그래프 -> section-graph
Retrieval -> section-retrieval
메모리 -> section-memory
평가 -> section-evaluation

상세 route:
Retrieval -> /analysis
Graph -> /event-graph
Memory -> /memory-timeline
Evaluation -> /signal-evaluation
```

## 검증 결과

```text
npm run lint      성공
npx tsc --noEmit  성공
내부 anchor 9개   확인
사이드바 link 7개 확인
상세 route 4개    HTTP 200
Dashboard 복귀    traceId 유지 확인
Frontend stderr   신규 오류 없음
```

인앱 Browser는 Windows sandbox 초기화 오류로 실행되지 않아 개발 서버의 렌더링 HTML과 route 응답으로 대체 검증했다.
