import type { SignalEvaluationData } from "@/types/signal-evaluation";

interface SignalSummaryCardProps {
  signal: SignalEvaluationData | null;
  fallbackLabel?: string;
  fallbackConfidence?: number;
}

const STYLE = {
  bullish: "border-green-500/40 bg-green-500/10 text-green-400",
  neutral: "border-yellow-500/40 bg-yellow-500/10 text-yellow-400",
  bearish: "border-red-500/40 bg-red-500/10 text-red-400",
};

export function SignalSummaryCard({
  signal,
  fallbackLabel = "중립",
  fallbackConfidence = 0.5,
}: SignalSummaryCardProps) {
  const current = signal?.current_signal;
  const label = current?.display_label ?? fallbackLabel;
  const conf = current?.confidence ?? fallbackConfidence;
  const key = current?.signal ?? "neutral";
  const style = STYLE[key] ?? STYLE.neutral;

  return (
    <div className={`rounded-xl border p-5 ${style}`}>
      <p className="text-xs text-muted-foreground">현재 관점</p>
      <p className="mt-1 text-3xl font-bold">{label}</p>
      <div className="mt-4">
        <p className="text-xs text-muted-foreground">분석 신뢰도</p>
        <p className="text-2xl font-semibold">{Math.round(conf * 100)}%</p>
        <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-background/50">
          <div
            className="h-full rounded-full bg-current opacity-80"
            style={{ width: `${Math.round(conf * 100)}%` }}
          />
        </div>
      </div>
      {signal?.summary_text && (
        <p className="mt-3 text-xs leading-relaxed opacity-90">
          {signal.summary_text}
        </p>
      )}
    </div>
  );
}
