"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";

interface Props {
  traceId: string | null;
}

export function RuntimeActionBar({ traceId }: Props) {
  if (!traceId) return null;
  return (
    <div className="flex flex-wrap gap-1">
      <Button variant="ghost" size="sm" asChild className="h-7 text-xs">
        <Link href={traceQueryHref("/event-graph", traceId)}>그래프 전체</Link>
      </Button>
      <Button variant="ghost" size="sm" asChild className="h-7 text-xs">
        <Link href={traceQueryHref("/analysis", traceId)}>상세 분석</Link>
      </Button>
    </div>
  );
}
