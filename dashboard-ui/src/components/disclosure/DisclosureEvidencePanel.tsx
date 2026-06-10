"use client";

import type { DisclosureEvidenceData } from "@/types/dashboard";

export function DisclosureEvidencePanel({
  data,
}: {
  data: DisclosureEvidenceData | null;
}) {
  const ev = data?.evidence ?? [];
  if (!ev.length) {
    return <p className="text-xs text-muted-foreground">공시 evidence 없음</p>;
  }
  return (
    <div className="space-y-1.5">
      {ev.slice(0, 4).map((e, i) => (
        <article key={`${e.chunk_id}-${i}`} className="rounded border border-border/70 p-2 text-xs">
          <p className="font-medium">{e.report_name}</p>
          <p className="text-muted-foreground">
            {e.report_date || "-"} · {e.report_type || "-"} · score {(e.score ?? 0).toFixed(3)}
          </p>
          <p className="mt-1 line-clamp-3">{e.text}</p>
        </article>
      ))}
    </div>
  );
}
