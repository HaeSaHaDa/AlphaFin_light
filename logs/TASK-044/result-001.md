# TASK-044 result-001

## 수행 요약

- Header에서 전역 페이지 이동 UI 제거
- Sidebar를 global navigation 단일 소스로 통합
- 모바일 Sidebar Drawer 추가
- section-level navigation은 detail-local로 제한
- dead navigation 컴포넌트 제거
- TASK-043를 `tasks/done/`으로 완료 처리
- Breadcrumb 계층을 `Dashboard > 현재화면 > 상세섹션`으로 강화
- section 기반 active route 규칙(뉴스/공시/근거 등) 정밀화
- sidebar collapse 시에도 글로벌 메뉴가 사라지지 않도록 compact 렌더 적용

## 생성 파일

- `dashboard-ui/src/navigation/navigation-policy.ts`
- `dashboard-ui/src/navigation/navigation-responsibility.ts`
- `dashboard-ui/src/navigation/global-navigation-map.ts`
- `dashboard-ui/src/navigation/local-navigation-map.ts`
- `dashboard-ui/src/navigation/navigation-priority.ts`
- `dashboard-ui/src/navigation/route-visibility.ts`
- `dashboard-ui/src/components/navigation-cleanup/GlobalNavigation.tsx`
- `dashboard-ui/src/components/navigation-cleanup/SidebarNavigation.tsx`
- `dashboard-ui/src/components/navigation-cleanup/DetailLocalNavigation.tsx`
- `dashboard-ui/src/components/navigation-cleanup/RuntimeBreadcrumb.tsx`
- `dashboard-ui/src/components/navigation-cleanup/NavigationDivider.tsx`
- `dashboard-ui/src/components/navigation-cleanup/NavigationGroup.tsx`

## 제거 파일

- `dashboard-ui/src/components/navigation/SidebarMenu.tsx`
- `dashboard-ui/src/components/navigation/RuntimePageTabs.tsx`
- `dashboard-ui/src/components/navigation/RuntimeBreadcrumb.tsx`
- `dashboard-ui/src/components/runtime-header/GlobalSectionNav.tsx`

## 검증 메모

- `npx tsc --noEmit` (dashboard-ui) 통과
- `python src/runtime_flow/runtime_query_runner.py` 는 상대 import 오류로 실패
- `python -m src.runtime_flow.runtime_query_runner` 실행 성공
- `http://localhost:3000` 응답 `200`
- `http://localhost:8000/health` 응답 `{"status":"ok","port":"8000"}`
