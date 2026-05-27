import type { SignalEvaluationData } from "@/types/signal-evaluation";

interface EvaluationSummaryProps {
  data: SignalEvaluationData;
}

export function EvaluationSummary({ data }: EvaluationSummaryProps) {
  return (
    <div className="rounded-lg border border-primary/30 bg-primary/5 p-4 text-sm">
      <h3 className="font-semibold text-primary">Signal 평가 요약</h3>
      <p className="mt-2 leading-relaxed text-muted-foreground">
        {data.summary_text}
      </p>
      <div className="mt-3 flex flex-wrap gap-2 text-xs">
        <span className="rounded border border-border px-2 py-1">
          trace: {data.trace_id}
        </span>
        {data.ticker && (
          <span className="rounded border border-border px-2 py-1">
            ticker: {data.ticker}
          </span>
        )}
        <span className="rounded border border-border px-2 py-1">
          적중률 {data.metrics.hit_ratio_pct}%
        </span>
      </div>
    </div>
  );
}
