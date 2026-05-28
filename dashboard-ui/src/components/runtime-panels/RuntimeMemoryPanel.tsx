"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { MemoryTimelineViewer } from "@/components/memory/memory-timeline-viewer";
import { RuntimePanelShell } from "./RuntimePanelShell";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";
import type { LoadStatus, MemoryData } from "@/types/dashboard";

interface Props {
  traceId: string | null;
  status: LoadStatus;
  memory: MemoryData | null;
}

export function RuntimeMemoryPanel({ traceId, status, memory }: Props) {
  return (
    <RuntimePanelShell traceId={traceId} status={status} title="Memory">
      <MemoryTimelineViewer data={memory} status={status} />
      {traceId && (
        <Button variant="outline" size="sm" className="mt-3" asChild>
          <Link href={traceQueryHref("/memory-timeline", traceId)}>
            시장 기억 타임라인
          </Link>
        </Button>
      )}
    </RuntimePanelShell>
  );
}
