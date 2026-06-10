/** Dashboard action roles — primary vs secondary vs removed. */

export type ActionRole = "primary" | "secondary";

export const PRIMARY_ACTION_LABELS = [
  "분석 실행",
  "종목 선택",
  "Load trace",
] as const;

export const SECONDARY_ACTION_LABELS = [
  "상세 분석",
  "시장 연결 구조",
  "시장 기억",
  "Signal 평가",
  "그래프 전체",
  "근거",
] as const;

/** Main dashboard scroll sections (must match DOM id). */
export const DASHBOARD_SECTIONS = [
  { id: "section-summary", label: "요약", priority: 1 },
  { id: "section-news", label: "뉴스", priority: 2 },
  { id: "section-events", label: "이벤트", priority: 3 },
  { id: "section-runtime-evidence", label: "근거", priority: 4 },
  { id: "section-disclosure", label: "공시", priority: 5 },
  { id: "section-graph", label: "그래프", priority: 6 },
  { id: "section-memory", label: "메모리", priority: 7 },
  { id: "section-evaluation", label: "평가", priority: 8 },
] as const;

export const SIDEBAR_ROUTES = [
  { key: "dashboard", label: "Dashboard", href: "/" },
  { key: "analysis", label: "상세 분석", href: "/analysis" },
  { key: "graph", label: "시장 그래프", href: "/event-graph" },
  { key: "memory", label: "시장 기억", href: "/memory-timeline" },
  { key: "signal", label: "Signal 평가", href: "/signal-evaluation" },
] as const;

export const RUNTIME_PAGE_TABS = SIDEBAR_ROUTES;
