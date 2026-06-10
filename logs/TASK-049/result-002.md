# TASK-049 후속 Regression 수정 결과

## 발견된 Regression

- `RuntimeQueryProvider`의 state updater 내부에서 `saveRuntimeSession()`이 동기 이벤트를 발생시켰다.
- 해당 이벤트를 받은 `GlobalTickerSelector`가 다른 컴포넌트 render 중 상태를 갱신했다.
- Runtime 결과가 없으면 News, Disclosure, Retrieval 섹션 DOM이 사라져 메뉴 이동이 동작하지 않았다.
- 같은 Dashboard 내부 메뉴 이동 시 URL hash가 갱신되지 않았다.
- 요구 메뉴에 없는 Settings가 Dashboard 요약으로 중복 연결되어 있었다.

## 수정 내용

- 세션 저장을 state updater 밖의 `useEffect`로 이동했다.
- Runtime 결과가 없어도 Dashboard 섹션 대상을 유지했다.
- 섹션 이동 시 URL hash를 함께 갱신했다.
- Settings 중복 메뉴를 제거하고 요구된 7개 메뉴만 유지했다.

## 검증 결과

```text
npm run lint      성공
npx tsc --noEmit  성공
Frontend HTTP     200
Settings menu     제거 확인
News target       확인
Disclosure target 확인
Retrieval target  확인
Graph route       확인
Memory route      확인
Evaluation route  확인
```

인앱 Browser는 Windows sandbox 초기화 오류로 실행되지 않아 렌더링 HTML과 개발 서버 응답으로 대체 검증했다.
