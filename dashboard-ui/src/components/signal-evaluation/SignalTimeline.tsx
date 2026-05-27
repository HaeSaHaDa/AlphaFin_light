"use client";

import { useState } from "react";
import type { TimelineEntry } from "@/types/signal-evaluation";

const DOT = {
  bullish: "bg-green-500 border-green-400",
  neutral: "bg-yellow-500 border-yellow-400",
  bearish: "bg-red-500 border-red-400",
};

interface SignalTimelineProps {
  timeline: TimelineEntry[];
}

export function SignalTimeline({ timeline }: SignalTimelineProps) {
  const [hovered, setHovered] = useState<TimelineEntry | null>(null);

  if (!timeline.length) return null;

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold">Signal 타임라인</h3>
      <div className="flex flex-col gap-0 sm:flex-row sm:items-center sm:gap-2">
        {timeline.map((entry, idx) => (
          <div key={entry.period} className="flex items-center gap-2">
            <button
              type="button"
              className="group flex flex-col items-center gap-1 rounded-lg px-3 py-2 transition-colors hover:bg-card/80"
              onMouseEnter={() => setHovered(entry)}
              onMouseLeave={() => setHovered(null)}
            >
              <span
                className={`h-4 w-4 rounded-full border-2 ${DOT[entry.signal]}`}
              />
              <span className="text-xs font-mono text-muted-foreground">
                {entry.period}
              </span>
              <span className="text-xs font-medium">{entry.display_label}</span>
            </button>
            {idx < timeline.length - 1 && (
              <span className="hidden text-muted-foreground sm:inline">↓</span>
            )}
          </div>
        ))}
      </div>
      {hovered && (
        <div className="rounded-md border border-border bg-card/80 px-3 py-2 text-xs">
          <span className="font-medium">{hovered.period}</span>
          {" · "}
          {hovered.display_label}
          {hovered.price_change_pct != null && (
            <span
              className={
                hovered.price_change_pct >= 0
                  ? " text-green-400"
                  : " text-red-400"
              }
            >
              {" "}
              · 실제 {hovered.price_change_pct >= 0 ? "+" : ""}
              {hovered.price_change_pct}%
            </span>
          )}
        </div>
      )}
    </div>
  );
}
