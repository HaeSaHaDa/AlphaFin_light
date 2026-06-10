"use client";

import type { DisclosureData } from "@/types/dashboard";

export function DisclosureSummaryCard({ data }: { data: DisclosureData | null }) {
  return (
    <div className="rounded-lg border border-border bg-card/50 p-3 text-xs">
      <p className="text-muted-foreground">Disclosure Summary</p>
      <p className="mt-1 text-sm font-semibold">
        문서 {data?.document_count ?? 0}건
      </p>
      <p className="mt-1 text-muted-foreground">
        ticker: {data?.ticker ?? "-"}
      </p>
    </div>
  );
}
