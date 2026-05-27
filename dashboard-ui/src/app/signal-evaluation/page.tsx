import { Suspense } from "react";
import { SignalEvaluationViewerClient } from "@/components/signal-evaluation-viewer-client";

export const metadata = { title: "AI Signal 평가 | AlphaFin LTE" };

export default function SignalEvaluationPage() {
  return (
    <Suspense
      fallback={
        <div className="p-8 text-center text-sm text-muted-foreground">로드 중…</div>
      }
    >
      <SignalEvaluationViewerClient />
    </Suspense>
  );
}
