import { DASHBOARD_SECTIONS } from "./action-policy";

/** Visual scan order for presentation. */
export const VISUAL_SCAN_ORDER = [
  "ticker",
  "runtime_status",
  "signal",
  "events",
  "risk",
  "evidence",
  "detail",
] as const;

export function getDashboardSectionNav() {
  return DASHBOARD_SECTIONS.map(({ id, label }) => ({ id, label }));
}
