"use client";

import type { CanonicalEvent } from "@/types/events";
import { EventConfidenceBadge } from "./EventConfidenceBadge";
import { EventEvidenceList } from "./EventEvidenceList";

interface Props {
  event: CanonicalEvent;
  defaultOpen?: boolean;
}

export function CanonicalEventCard({ event, defaultOpen = false }: Props) {
  const impact =
    event.impact_direction === "positive"
      ? "text-emerald-400"
      : event.impact_direction === "negative"
        ? "text-rose-400"
        : "text-muted-foreground";

  return (
    <article className="rounded-xl border border-border bg-card/60 p-4">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div>
          <h4 className="text-sm font-semibold leading-snug">
            {event.canonical_title}
          </h4>
          {event.event_summary && (
            <p className="mt-1 whitespace-pre-line text-xs leading-relaxed text-muted-foreground">
              {event.event_summary}
            </p>
          )}
        </div>
        <EventConfidenceBadge score={event.confidence_score} />
      </div>
      <div className="mt-2 flex flex-wrap gap-2 text-[10px] text-muted-foreground">
        <span className={impact}>{event.impact_direction ?? "neutral"}</span>
        <span>·</span>
        <span>근거 {event.evidence_count}건</span>
        {event.event_type && (
          <>
            <span>·</span>
            <span>{event.event_type}</span>
          </>
        )}
      </div>
      {(defaultOpen || (event.evidence?.length ?? 0) <= 4) && (
        <EventEvidenceList evidence={event.evidence ?? []} />
      )}
    </article>
  );
}
