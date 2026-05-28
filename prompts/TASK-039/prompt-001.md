# TASK-039 Prompt 001

## 목표

Global Persistent Runtime Shell Layout 초기 구현으로 Header/Sidebar/Footer 및 Runtime Context 유지 구조를 구축한다.

## 수행

- `RuntimeShellLayout`, `RuntimeHeader`, `RuntimeSidebar`, `RuntimeFooter`, `RuntimeWorkspace` 생성
- `RuntimeShellProvider` + layout state(sessionStorage) persistence 구현
- `RuntimeQueryProvider`를 app 전역 provider로 승격
- global header 요소 추가(종목/검색/trace 상태/section nav/actions)
- sidebar menu 및 page highlight 구현
- `/api/runtime/context` 추가
- TASK-038 done 이동 및 상태 업데이트

## 검증

- 페이지 이동 시 header/sidebar/footer 유지
- selectedTicker/traceId/session 기반 표시 유지
- sidebar collapse state 유지
- workspace 영역만 스크롤
