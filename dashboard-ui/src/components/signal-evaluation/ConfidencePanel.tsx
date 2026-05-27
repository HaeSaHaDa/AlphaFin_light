import type { SignalEvaluationData } from "@/types/signal-evaluation";

interface ConfidencePanelProps {
  evaluation: SignalEvaluationData["confidence_evaluation"];
  summary: SignalEvaluationData["confidence_summary"];
  currentConfidence: number;
}

export function ConfidencePanel({
  evaluation,
  summary,
  currentConfidence,
}: ConfidencePanelProps) {
  const pct = Math.round(currentConfidence * 100);
  const barWidth = pct;

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card/60 p-4">
      <h3 className="text-sm font-semibold">분석 신뢰도 평가</h3>

      <div className="space-y-1">
        <div className="flex justify-between text-xs">
          <span className="text-muted-foreground">현재 Signal 분석 신뢰도</span>
          <span className="font-bold">{pct}%</span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-muted">
          <div
            className="h-full rounded-full bg-primary transition-all"
            style={{ width: `${barWidth}%` }}
          />
        </div>
      </div>

      {evaluation.label && (
        <p className="rounded-md bg-primary/10 px-3 py-2 text-xs text-primary">
          {evaluation.label}
        </p>
      )}

      {summary.avg_confidence != null && (
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="rounded border border-border p-2">
            <p className="text-muted-foreground">평균 신뢰도</p>
            <p className="font-mono font-medium">
              {(summary.avg_confidence * 100).toFixed(0)}%
            </p>
          </div>
          <div className="rounded border border-border p-2">
            <p className="text-muted-foreground">고신뢰도 적중률</p>
            <p className="font-mono font-medium">
              {summary.high_confidence_hit_rate ?? 0}%
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
