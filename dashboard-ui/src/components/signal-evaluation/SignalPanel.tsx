import type { CurrentSignal } from "@/types/signal-evaluation";

const SIGNAL_STYLE = {
  bullish: "border-green-500/50 bg-green-500/15 text-green-400",
  neutral: "border-yellow-500/50 bg-yellow-500/15 text-yellow-400",
  bearish: "border-red-500/50 bg-red-500/15 text-red-400",
};

interface SignalPanelProps {
  signal: CurrentSignal;
  query: string;
}

export function SignalPanel({ signal, query }: SignalPanelProps) {
  const style = SIGNAL_STYLE[signal.signal] ?? SIGNAL_STYLE.neutral;
  const confPct = Math.round(signal.confidence * 100);

  return (
    <div className={`rounded-lg border p-4 ${style}`}>
      <p className="text-xs text-muted-foreground">현재 관점 (AI 시장 관점)</p>
      <div className="mt-2 flex flex-wrap items-baseline gap-3">
        <span className="text-3xl font-bold">{signal.display_label}</span>
        <span className="rounded-full border border-current/30 px-2 py-0.5 text-xs">
          분석 신뢰도 {confPct}%
        </span>
      </div>
      {query && (
        <p className="mt-2 text-xs opacity-80">분석 대상: {query}</p>
      )}
      {signal.reason.length > 0 && (
        <ul className="mt-3 space-y-1 text-sm">
          {signal.reason.map((r, i) => (
            <li key={i} className="flex gap-2">
              <span>·</span>
              <span>{r}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
