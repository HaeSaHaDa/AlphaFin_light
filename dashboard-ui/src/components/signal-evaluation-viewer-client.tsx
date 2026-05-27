"use client";

import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { Loader2, AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { SignalPanel } from "@/components/signal-evaluation/SignalPanel";
import { SignalHistory } from "@/components/signal-evaluation/SignalHistory";
import { SignalTimeline } from "@/components/signal-evaluation/SignalTimeline";
import { AccuracyPanel } from "@/components/signal-evaluation/AccuracyPanel";
import { ConfidencePanel } from "@/components/signal-evaluation/ConfidencePanel";
import { EvaluationSummary } from "@/components/signal-evaluation/EvaluationSummary";
import { useSignalEvaluation } from "@/hooks/use-signal-evaluation";

export function SignalEvaluationViewerClient() {
  const params = useSearchParams();
  const traceId = params.get("trace_id") || null;
  const { data, status, error, reload } = useSignalEvaluation(traceId);

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-6">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border pb-4">
        <div>
          <h1 className="text-xl font-bold">AI Signal 평가</h1>
          <p className="text-xs text-muted-foreground">
            AI 시장 관점 · 방향 예측 정확도 · 예측 적중률
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm" asChild>
            <Link href="/">Dashboard</Link>
          </Button>
          <Button variant="outline" size="sm" onClick={reload} disabled={status === "loading"}>
            <RefreshCw className="h-3 w-3" />
            새로고침
          </Button>
        </div>
      </div>

      {status === "loading" && (
        <div className="flex justify-center py-20">
          <Loader2 className="h-6 w-6 animate-spin text-primary" />
          <span className="ml-2 text-sm text-muted-foreground">Signal 로드 중…</span>
        </div>
      )}

      {status === "error" && (
        <div className="flex items-center gap-2 rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-sm">
          <AlertTriangle className="h-4 w-4" />
          {error}
        </div>
      )}

      {status === "success" && data && (
        <div className="space-y-6">
          <EvaluationSummary data={data} />
          <SignalPanel signal={data.current_signal} query={data.query} />
          <div className="grid gap-4 lg:grid-cols-2">
            <AccuracyPanel metrics={data.metrics} market={data.market_comparison} />
            <ConfidencePanel
              evaluation={data.confidence_evaluation}
              summary={data.confidence_summary}
              currentConfidence={data.current_signal.confidence}
            />
          </div>
          <SignalTimeline timeline={data.timeline} />
          <SignalHistory history={data.history} />
        </div>
      )}
    </div>
  );
}
