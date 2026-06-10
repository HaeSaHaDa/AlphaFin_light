# TASK-049 Navigation 계층 분리 결과

## 문제

- 사이드바에 독립 route와 Dashboard 내부 section이 같은 등급으로 섞여 있었다.
- News와 Disclosure는 Dashboard 하위 영역인데 Graph, Memory, Evaluation, Retrieval과 같은 메뉴 등급으로 표시됐다.
- Graph 상세 화면에는 동작하지 않는 `Dashboard sections` 제목이 남아 있었다.
- Dashboard 내부 Graph, Memory, Evaluation, Retrieval을 볼 때 대응 사이드바 메뉴가 활성화되어 현재 화면 계층이 모호했다.

## 수정

### 사이드바: 독립 Pages

```text
Dashboard
Retrieval
Graph
Memory
Evaluation
```

- 각 항목은 실제 독립 route로 이동한다.
- News와 Disclosure를 사이드바에서 제거했다.
- Dashboard 내부 어느 section을 보고 있어도 사이드바는 Dashboard만 활성화한다.

### Dashboard 내부 메뉴

```text
요약
뉴스
이벤트
근거
공시
그래프
Retrieval
메모리
평가
```

- Dashboard에서만 표시한다.
- 상세 route에서는 내부 메뉴와 제목을 모두 숨긴다.
- News와 Disclosure는 Dashboard 내부 section으로 유지한다.

## route

```text
Dashboard  -> /
Retrieval  -> /analysis
Graph      -> /event-graph
Memory     -> /memory-timeline
Evaluation -> /signal-evaluation
```

## 검증

```text
각 route HTTP 200
사이드바 메뉴 5개
화면별 활성 사이드바 1개
Dashboard 내부 메뉴 9개
상세 route 내부 메뉴 0개
News 사이드바 링크 없음
Disclosure 사이드바 링크 없음
News section 유지
Disclosure section 유지
npm run lint 성공
npx tsc --noEmit 성공
Frontend stderr 신규 오류 없음
```
