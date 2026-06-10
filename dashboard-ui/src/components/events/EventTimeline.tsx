"use client";

import type { CanonicalEvent } from "@/types/events";
import { CanonicalEventCard } from "./CanonicalEventCard";

interface Props {
  events: CanonicalEvent[];
}

export function EventTimeline({ events }: Props) {
  if (events.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">
        통합된 시장 이벤트가 없습니다. 분석 실행 후 자동 생성됩니다.
      </p>
    );
  }

  return (
    <div className="relative space-y-3 pl-4 before:absolute before:left-1 before:top-2 before:bottom-2 before:w-px before:bg-border">
      {events.map((ev) => (
        <div key={ev.event_id} className="relative">
          <span className="absolute -left-[13px] top-4 h-2 w-2 rounded-full bg-primary" />
          <CanonicalEventCard event={ev} />
        </div>
      ))}
    </div>
  );
}
