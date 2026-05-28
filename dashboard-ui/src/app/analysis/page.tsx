import { Suspense } from "react";
import { AnalysisViewerClient } from "@/components/analysis-viewer-client";

export default function AnalysisPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-sm text-muted-foreground">로드 중…</div>}>
      <AnalysisViewerClient />
    </Suspense>
  );
}
