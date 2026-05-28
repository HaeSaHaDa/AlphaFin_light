import { Suspense } from "react";
import { EventGraphViewerClient } from "@/components/event-graph-viewer-client";

export default function EventGraphPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-sm text-muted-foreground">로드 중…</div>}>
      <EventGraphViewerClient />
    </Suspense>
  );
}
