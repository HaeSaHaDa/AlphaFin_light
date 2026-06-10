"use client";

import type { EventEvidence } from "@/types/events";

interface Props {
  evidence: EventEvidence[];
  maxItems?: number;
}

const SOURCE_LABEL: Record<string, string> = {
  NEWS: "뉴스",
  DISCLOSURE: "공시",
  CHUNK: "문서",
  MEMORY: "메모리",
};

export function EventEvidenceList({ evidence, maxItems = 6 }: Props) {
  const items = evidence.slice(0, maxItems);
  if (items.length === 0) {
    return (
      <p className="text-xs text-muted-foreground">연결된 근거가 없습니다.</p>
    );
  }

  return (
    <ul className="mt-2 space-y-2">
      {items.map((ev, i) => (
        <li
          key={`${ev.source_id ?? i}-${ev.source_type}`}
          className="rounded-lg border border-border/60 bg-muted/15 px-3 py-2 text-xs"
        >
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded bg-primary/10 px-1.5 py-0.5 text-[10px] text-primary">
              {SOURCE_LABEL[ev.source_type] ?? ev.source_type}
            </span>
            {ev.relevance_score != null && (
              <span className="text-muted-foreground">
                {(ev.relevance_score * 100).toFixed(0)}%
              </span>
            )}
          </div>
          <p className="mt-1 leading-snug text-foreground/90">
            {ev.title ?? ev.source_id ?? "근거"}
          </p>
        </li>
      ))}
    </ul>
  );
}
