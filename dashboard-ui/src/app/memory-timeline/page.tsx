import { Suspense } from "react";
import { MemoryTimelineViewerClient } from "@/components/memory-timeline-viewer-client";

export const metadata = { title: "시장 기억 타임라인 | AlphaFin LTE" };

export default function MemoryTimelinePage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-sm text-muted-foreground">로드 중…</div>}>
      <MemoryTimelineViewerClient />
    </Suspense>
  );
}
