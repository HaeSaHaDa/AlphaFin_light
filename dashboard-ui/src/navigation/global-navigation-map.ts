export interface GlobalNavigationItem {
  key: string;
  label: string;
  shortLabel: string;
  href: string;
}

export const GLOBAL_NAVIGATION_MAP: GlobalNavigationItem[] = [
  {
    key: "dashboard",
    label: "Dashboard",
    shortLabel: "Home",
    href: "/",
  },
  {
    key: "retrieval",
    label: "Retrieval",
    shortLabel: "Rtrv",
    href: "/analysis",
  },
  {
    key: "graph",
    label: "Graph",
    shortLabel: "Graph",
    href: "/event-graph",
  },
  {
    key: "memory",
    label: "Memory",
    shortLabel: "Memo",
    href: "/memory-timeline",
  },
  {
    key: "evaluation",
    label: "Evaluation",
    shortLabel: "Eval",
    href: "/signal-evaluation",
  },
];
