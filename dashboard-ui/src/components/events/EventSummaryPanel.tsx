"use client";

import { useEffect, useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { DashboardSectionCard } from "@/components/ui-cleanup/DashboardSectionCard";
import { InformationPriorityBadge } from "@/components/ui-cleanup/InformationPriorityBadge";
import { getEventsByTrace } from "@/services/api";
import type { EventsTracePayload } from "@/types/events";
import { EventTimeline } from "./EventTimeline";

interface Props {
  traceId: string | null;
  ticker?: string | null;
}

export function EventSummaryPanel({ traceId, ticker }: Props) {
  const [data, setData] = useState<EventsTracePayload | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "error" | "ok">("idle");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const id = traceId?.trim();
    if (!id) {
      setData(null);
      setStatus("idle");
      return;
    }
    setStatus("loading");
    setError(null);
    getEventsByTrace(id, ticker ?? undefined)
      .then((payload) => {
        setData(payload);
        setStatus("ok");
      })
      .catch((e) => {
        setError(e instanceof Error ? e.message : "이벤트 로드 실패");
        setStatus("error");
      });
  }, [traceId, ticker]);

  return (
    <DashboardSectionCard
      id="section-events"
      title="핵심 시장 이벤트"
      subtitle="중복 뉴스·공시를 canonical event로 통합"
      accent="warning"
      badge={
        data ? (
          <InformationPriorityBadge
            label={`${data.event_count}개 이벤트`}
            accent="warning"
          />
        ) : undefined
      }
    >
      {status === "loading" && <Skeleton className="h-32 w-full rounded-xl" />}
      {status === "error" && (
        <p className="text-sm text-destructive">{error}</p>
      )}
      {status === "idle" && (
        <p className="text-sm text-muted-foreground">
          분석 실행 후 이벤트 타임라인이 표시됩니다.
        </p>
      )}
      {status === "ok" && data && <EventTimeline events={data.events} />}
    </DashboardSectionCard>
  );
}
