"use client";

interface Props {
  breakdown: Record<string, number>;
}

const LABELS: Record<string, string> = {
  DISCLOSURE: "공시",
  NEWS: "뉴스",
  OTHER: "기타",
};

export function RuntimeSourceBreakdown({ breakdown }: Props) {
  const entries = Object.entries(breakdown).filter(([, n]) => n > 0);
  if (entries.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2">
      {entries.map(([key, count]) => (
        <span
          key={key}
          className="rounded-md border border-border/70 bg-muted/20 px-2 py-1 text-[11px]"
        >
          {LABELS[key] ?? key}: {count}
        </span>
      ))}
    </div>
  );
}
