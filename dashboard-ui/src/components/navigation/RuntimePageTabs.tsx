"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";

const TABS = [
  { href: "/", label: "Summary" },
  { href: "/analysis", label: "News/Retrieval" },
  { href: "/event-graph", label: "Graph" },
  { href: "/memory-timeline", label: "Memory" },
  { href: "/signal-evaluation", label: "Signal" },
];

export function RuntimePageTabs() {
  const pathname = usePathname();
  const params = useSearchParams();
  const traceId = params.get("trace_id");
  return (
    <div className="flex flex-wrap gap-1">
      {TABS.map((tab) => {
        const active = pathname === tab.href;
        return (
          <Link
            key={tab.href}
            href={traceQueryHref(tab.href, traceId)}
            className={
              active
                ? "rounded-md border border-primary/50 bg-primary/10 px-2 py-1 text-xs text-primary"
                : "rounded-md border border-border/70 px-2 py-1 text-xs text-muted-foreground hover:text-foreground"
            }
          >
            {tab.label}
          </Link>
        );
      })}
    </div>
  );
}
