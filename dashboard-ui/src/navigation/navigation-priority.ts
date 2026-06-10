import type { NavigationScope } from "./navigation-policy";

const PRIORITY_MAP: Record<NavigationScope, number> = {
  sidebar: 1,
  header: 2,
  "detail-local": 3,
};

export function resolveNavigationPriority(scope: NavigationScope): number {
  return PRIORITY_MAP[scope];
}
