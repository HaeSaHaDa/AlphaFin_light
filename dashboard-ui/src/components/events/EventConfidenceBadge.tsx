"use client";

interface Props {
  score: number;
  className?: string;
}

export function EventConfidenceBadge({ score, className = "" }: Props) {
  const pct = Math.round(score * 100);
  const tone =
    score >= 0.75
      ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-400"
      : score >= 0.5
        ? "border-amber-500/40 bg-amber-500/10 text-amber-300"
        : "border-border bg-muted/30 text-muted-foreground";

  return (
    <span
      className={`inline-flex items-center rounded-md border px-2 py-0.5 text-[11px] font-medium ${tone} ${className}`}
      title="Event-level confidence"
    >
      신뢰도 {pct}%
    </span>
  );
}
