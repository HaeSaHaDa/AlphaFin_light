"use client";

import { usePathname } from "next/navigation";

const LABELS: Record<string, string> = {
  "/": "Dashboard",
  "/analysis": "Analysis",
  "/event-graph": "Graph",
  "/memory-timeline": "Memory",
  "/signal-evaluation": "Evaluation",
};

export function RuntimeBreadcrumb() {
  const pathname = usePathname();
  const current = LABELS[pathname] ?? "Runtime";
  return (
    <p className="text-xs text-muted-foreground">
      Runtime / <span className="text-foreground">{current}</span>
    </p>
  );
}
