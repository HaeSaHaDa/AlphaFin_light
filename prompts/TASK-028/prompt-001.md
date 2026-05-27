# TASK-028 Prompt-001

## 작업

TASK-028-build-memory-timeline-visualization

## 목표

Financial AI Engine의 Memory Lifecycle을 시간 축 기반으로 시각화하는
Memory Timeline Visualization 구축.

단기 기억 → 중기 기억 → 장기 기억 흐름과
importance score, promotion, decay를 발표용으로 시각화.

## 수행 내용

- MemoryTimeline.tsx: 전체 타임라인 렌더링
- MemoryTrack.tsx: layer별 트랙 (단기/중기/장기)
- MemoryNode.tsx: 기억 노드 · importance badge
- MemoryDetailPanel.tsx: 클릭 기억 상세
- MemoryLegend.tsx: layer 색상 범례
- MemoryToolbar.tsx: layer/importance 필터
- MemorySummaryPanel.tsx: AI 핵심 기억 요약
- `/memory-timeline` 페이지
- DashboardNav 링크 추가

## API 연동

- GET /api/memory/{trace_id}
- GET /api/trace/{trace_id}
- latest fallback 유지

## 기술

- Tailwind 다크 테마
- 한국어 친화적 UI (단기/중기/장기 기억, 시장 기억, AI 자기 검토)
- 과도한 animation 금지
- 과도한 abstraction 금지

## 제외

- Cognitive Architecture / Human-like Simulation 금지
- Real-time Streaming 금지
- Autonomous Memory Evolution 금지
