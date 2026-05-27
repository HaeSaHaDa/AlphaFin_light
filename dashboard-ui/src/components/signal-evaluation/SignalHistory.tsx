import type { SignalEvaluationData } from "@/types/signal-evaluation";

const BADGE = {
  bullish: "bg-green-500/20 text-green-400",
  neutral: "bg-yellow-500/20 text-yellow-400",
  bearish: "bg-red-500/20 text-red-400",
};

interface SignalHistoryProps {
  history: SignalEvaluationData["history"];
}

export function SignalHistory({ history }: SignalHistoryProps) {
  if (!history.length) {
    return <p className="text-xs text-muted-foreground">기록 없음</p>;
  }

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold">Signal 기록</h3>
      <ul className="space-y-2">
        {history.map((h, i) => (
          <li
            key={`${h.period}-${i}`}
            className="flex flex-wrap items-center justify-between gap-2 rounded border border-border bg-card/50 px-3 py-2 text-xs"
          >
            <span className="font-mono text-muted-foreground">{h.period}</span>
            <span className={`rounded px-2 py-0.5 ${BADGE[h.signal]}`}>
              {h.display_label}
            </span>
            {h.price_change_pct != null && (
              <span
                className={
                  h.price_change_pct >= 0 ? "text-green-400" : "text-red-400"
                }
              >
                {h.price_change_pct >= 0 ? "+" : ""}
                {h.price_change_pct}%
              </span>
            )}
            <span
              className={
                h.direction_correct ? "text-green-400" : "text-red-400"
              }
            >
              {h.direction_correct ? "방향 일치" : "방향 불일치"}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
