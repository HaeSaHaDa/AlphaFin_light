import { cn } from "@/lib/utils";
import { DASHBOARD_COLORS, type DashboardColorKey } from "./dashboard-color-system";

export function panelAccentClass(accent?: DashboardColorKey): string {
  if (!accent) return "dash-panel";
  return cn("dash-panel", `dash-panel-${accent}`);
}

export function sectionTitleClass(): string {
  return "dash-section-title";
}

export function metricValueClass(): string {
  return "dash-metric-value";
}

export function badgeForAccent(accent: DashboardColorKey): string {
  return cn(
    "inline-flex rounded-md border px-2 py-0.5 text-[11px] font-medium",
    DASHBOARD_COLORS[accent],
  );
}
