# TASK-043 prompt-001

## 목표

Dashboard dead action 제거 및 visual hierarchy 개선.

## 범위

- `dashboard-ui/src/ui/*` design tokens
- `dashboard-ui/src/components/ui-cleanup/*`
- dashboard-client / shell / sidebar / section nav 정리

## 제거

- GlobalRuntimeSearch (미연동)
- RuntimeQuickActions (중복)
- RuntimeActionBar (중복)
- dashboard 중복 nav 버튼 4개
- Sidebar Settings/Retrieval/Disclosure dead links
