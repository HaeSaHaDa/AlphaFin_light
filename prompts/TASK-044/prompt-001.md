# TASK-044 prompt-001

## 요청 요약

- Navigation responsibility 분리
- Header 내 전역 화면 이동 제거
- Sidebar를 단일 global navigation source로 통일
- Detail 내부는 local tab/section navigation만 허용
- dead/duplicated navigation 제거

## 수행 범위

- `dashboard-ui/src/navigation/*` 정책/맵 파일 생성
- `dashboard-ui/src/components/navigation-cleanup/*` 컴포넌트 생성
- `RuntimeHeader`, `RuntimeSidebar` 연결 정리
- TASK-043 완료 처리 + TASK-044 상태 DOING 반영
