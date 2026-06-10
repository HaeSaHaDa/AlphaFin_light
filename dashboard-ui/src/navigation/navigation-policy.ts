export type NavigationScope = "header" | "sidebar" | "detail-local";

export interface NavigationPolicy {
  scope: NavigationScope;
  allowGlobalRoute: boolean;
  allowSectionScroll: boolean;
}

export function resolveNavigationPolicy(
  scope: NavigationScope,
): NavigationPolicy {
  if (scope === "header") {
    return {
      scope,
      allowGlobalRoute: false,
      allowSectionScroll: false,
    };
  }
  if (scope === "sidebar") {
    return {
      scope,
      allowGlobalRoute: true,
      allowSectionScroll: false,
    };
  }
  return {
    scope,
    allowGlobalRoute: false,
    allowSectionScroll: true,
  };
}
