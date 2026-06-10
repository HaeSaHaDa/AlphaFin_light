# TASK-049 메뉴·검색 추가 회귀 점검

## 점검 범위

- 사이드바 7개 메뉴
- Dashboard 내부 9개 메뉴
- Retrieval, Graph, Memory, Evaluation 상세 화면
- 회사명·ticker 검색
- 종목 선택 동기화
- 분석 실행과 traceId 생성
- hash 이동, 뒤로가기, 상세 화면 복귀
- Frontend·Backend 오류 로그

## 발견 및 수정한 버그

1. 빠르게 검색어를 변경하면 이전 API 응답이 최신 검색 결과를 덮을 수 있었다.
   - 검색 요청 식별자를 추가해 최신 요청만 반영했다.

2. Header 또는 Dashboard 한쪽에서 종목이 변경돼도 다른 검색 UI가 이전 종목을 유지할 수 있었다.
   - 외부 ticker 변경 시 선택 종목을 다시 동기화했다.

3. Header에서 분석을 실행하면 현재 상세 화면에 그대로 남아 새 결과 위치가 불명확했다.
   - 분석 완료 후 새 traceId를 유지한 Dashboard로 이동하도록 수정했다.

4. 내부 메뉴의 마지막 평가 섹션이 페이지 높이에 따라 활성화되지 않을 수 있었다.
   - 페이지 최하단에서는 마지막 렌더링 섹션을 활성화하도록 수정했다.

5. hash가 제거되는 브라우저 뒤로가기에서 이전 메뉴 활성 효과가 남았다.
   - Dashboard의 hash가 없으면 Summary 상태로 복원하도록 수정했다.

6. 검색 결과가 하나일 때 Enter 키로 선택할 수 없었다.
   - 단일 결과는 Enter 키로 선택할 수 있도록 보완했다.

## 실행 검증

```text
회사명 검색: 삼성전자, 삼성전기 성공
ticker 검색: 005930, 009150 성공
없는 종목 검색: 빈 결과 정상

Runtime 실행:
ticker   009150
company  삼성전기
keyword  MLCC
status   completed
traceId  20260609_154829

Dashboard          200
Analysis           200
Event Graph        200
Memory Timeline    200
Signal Evaluation  200
Runtime APIs       200
Events API         200
```

## 검증 도구

```text
npm run lint      성공
npx tsc --noEmit  성공
git diff --check  성공
Frontend HTTP     200
Backend HTTP      200
Frontend stderr   신규 오류 없음
```

## 남아있는 위험

- Backend 시작 시 pykrx가 KRX 응답을 파싱하지 못하면 traceback을 기록한 뒤 seed 데이터로 복구한다.
- 메뉴·검색 기능에는 영향을 주지 않지만 시작 로그가 과도하게 오염된다.
- 인앱 Browser는 Windows sandbox 초기화 오류로 사용할 수 없어 렌더링 HTML, API, route 응답으로 대체 검증했다.
