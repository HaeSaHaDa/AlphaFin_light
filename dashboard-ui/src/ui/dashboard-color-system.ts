/** Semantic color tokens for dashboard panels. */

export const DASHBOARD_COLORS = {
  primary: "text-primary border-primary/40 bg-primary/10",
  success: "text-emerald-400 border-emerald-500/40 bg-emerald-500/10",
  warning: "text-amber-300 border-amber-500/40 bg-amber-500/10",
  danger: "text-rose-400 border-rose-500/40 bg-rose-500/10",
  neutral: "text-muted-foreground border-border/70 bg-muted/20",
  disclosure: "text-cyan-300 border-cyan-500/40 bg-cyan-500/10",
  memory: "text-violet-300 border-violet-500/40 bg-violet-500/10",
  graph: "text-sky-300 border-sky-500/40 bg-sky-500/10",
  news: "text-blue-300 border-blue-500/40 bg-blue-500/10",
  evidence: "text-teal-300 border-teal-500/40 bg-teal-500/10",
} as const;

export type DashboardColorKey = keyof typeof DASHBOARD_COLORS;

export const PANEL_ACCENT: Record<string, DashboardColorKey> = {
  summary: "primary",
  signal: "primary",
  news: "news",
  events: "warning",
  evidence: "evidence",
  disclosure: "disclosure",
  graph: "graph",
  memory: "memory",
  evaluation: "success",
  risk: "danger",
};
