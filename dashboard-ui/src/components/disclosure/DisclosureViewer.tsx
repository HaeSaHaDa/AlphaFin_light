"use client";

import type { DisclosureData } from "@/types/dashboard";

interface Props {
  data: DisclosureData | null;
  filter: string;
}

export function DisclosureViewer({ data, filter }: Props) {
  const f = filter.trim().toLowerCase();
  const docs = (data?.documents ?? []).filter((d) => {
    if (!f) return true;
    return (
      d.report_name.toLowerCase().includes(f) ||
      (d.report_type || "").toLowerCase().includes(f) ||
      (d.source_type || "").toLowerCase().includes(f)
    );
  });
  if (!docs.length) {
    return <p className="text-xs text-muted-foreground">표시할 공시가 없습니다.</p>;
  }
  return (
    <div className="space-y-2">
      {docs.slice(0, 8).map((d) => (
        <article key={d.document_id} className="rounded border border-border/80 p-2 text-xs">
          <p className="font-medium">{d.report_name}</p>
          <p className="mt-0.5 text-muted-foreground">
            {d.report_date || "-"} · {d.report_type}
          </p>
          {d.summary ? <p className="mt-1 line-clamp-2 text-foreground/90">{d.summary}</p> : null}
        </article>
      ))}
    </div>
  );
}
