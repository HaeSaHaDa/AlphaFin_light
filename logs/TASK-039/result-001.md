# TASK-039 result-001

## 수행 요약

- TASK-038 파일을 `tasks/done/`으로 이동하고 상태를 `DONE`으로 업데이트
- TASK-039 상태를 `DOING`으로 전환
- Runtime Shell 초기 구현
  - `dashboard-ui/src/layout/runtime-shell/*` 생성
  - `dashboard-ui/src/components/navigation/*` 생성
  - `dashboard-ui/src/components/runtime-header/Global*` 컴포넌트 생성
  - app 루트 레이아웃에 `RuntimeShellLayout` + 전역 provider 적용
- Runtime context API 추가
  - `GET /api/runtime/context?trace_id=...`
- 스타일 보강
  - shell header/body/sidebar/workspace/footer 스크롤/고정 구조 CSS 추가

## 핵심 변경 파일

- `dashboard-ui/src/app/layout.tsx`
- `dashboard-ui/src/app/providers.tsx`
- `dashboard-ui/src/app/page.tsx`
- `dashboard-ui/src/app/globals.css`
- `dashboard-ui/src/layout/runtime-shell/*`
- `dashboard-ui/src/components/navigation/*`
- `dashboard-ui/src/components/runtime-header/Global*.tsx`
- `dashboard-ui/src/services/api.ts`
- `src/dashboard_api/routes/runtime.py`

## 남은 확인

- 실제 페이지 전환 시 shell 절대 재마운트 여부 확인
- 모바일 drawer/sidebar 동작 고도화
- 기존 페이지별 중복 header/nav 정리(2차 리팩터)
