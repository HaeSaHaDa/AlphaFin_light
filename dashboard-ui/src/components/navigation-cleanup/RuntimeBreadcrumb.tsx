"use client";

import { usePathname } from "next/navigation";
import { useRuntimeShell } from "@/layout/runtime-shell/RuntimeShellProvider";
import { normalizeSectionKey } from "@/navigation/section-key";

const LABELS: Record<string, string> = {
  "/": "Overview",
  "/analysis": "Analysis",
  "/event-graph": "Graph",
  "/memory-timeline": "Memory",
  "/signal-evaluation": "Evaluation",
};

const SECTION_LABELS: Record<string, string> = {
  summary: "Summary",
  news: "News",
  events: "Events",
  evidence: "Evidence",
  disclosure: "Disclosure",
  graph: "Graph",
  retrieval: "Retrieval",
  memory: "Memory",
  evaluation: "Evaluation",
};

export function RuntimeBreadcrumb() {
  const pathname = usePathname();
  const { currentSection } = useRuntimeShell();
  const current = LABELS[pathname] ?? "Runtime";
  const section =
    pathname === "/" ? SECTION_LABELS[normalizeSectionKey(currentSection)] : null;
  return (
    <p className="text-xs text-muted-foreground">
      Dashboard
      <span className="px-1 text-muted-foreground/70">{">"}</span>
      <span className="text-foreground">{current}</span>
      {section ? (
        <>
          <span className="px-1 text-muted-foreground/70">{">"}</span>
          <span className="text-foreground">{section}</span>
        </>
      ) : null}
    </p>
  );
}
