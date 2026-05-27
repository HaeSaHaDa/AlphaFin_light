import { formatScore } from "@/lib/utils";

interface ScoreBarProps {
  score: number;
  label?: string;
}

export function ScoreBar({ score, label }: ScoreBarProps) {
  const pct = Math.min(100, Math.max(0, score * 100));
  return (
    <div className="space-y-1">
      {label && (
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>{label}</span>
          <span>{formatScore(score)}</span>
        </div>
      )}
      <div className="h-2 overflow-hidden rounded-full bg-muted">
        <div
          className="h-full rounded-full bg-primary transition-[width]"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
