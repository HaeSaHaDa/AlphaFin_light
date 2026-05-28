"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";

export function RuntimeQuickActions() {
  const params = useSearchParams();
  const traceId = params.get("trace_id");
  return (
    <div className="flex flex-wrap gap-1">
      <Link
        href={traceQueryHref("/event-graph", traceId)}
        className="rounded border border-border px-2 py-1 text-[11px] text-muted-foreground hover:text-foreground"
      >
        Graph
      </Link>
      <Link
        href={traceQueryHref("/memory-timeline", traceId)}
        className="rounded border border-border px-2 py-1 text-[11px] text-muted-foreground hover:text-foreground"
      >
        Memory
      </Link>
    </div>
  );
}
