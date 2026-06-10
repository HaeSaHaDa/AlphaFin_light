"use client";

import type { DisclosureTimelineData } from "@/types/dashboard";

export function DisclosureTimeline({ data }: { data: DisclosureTimelineData | null }) {
  const items = data?.timeline ?? [];
  if (!items.length) {
    return <p className="text-xs text-muted-foreground">타임라인 데이터가 없습니다.</p>;
  }
  return (
    <ul className="space-y-1.5 text-xs">
      {items.slice(0, 8).map((t, idx) => (
        <li key={`${t.report_date}-${idx}`} className="rounded border border-border/70 p-2">
          <p className="font-medium">{t.title}</p>
          <p className="text-muted-foreground">
            {t.report_date || "-"} · {t.report_type || "UNKNOWN"}
          </p>
        </li>
      ))}
    </ul>
  );
}
