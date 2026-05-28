"use client";

import { RelatedNewsPanel } from "@/components/report-layout/RelatedNewsPanel";
import { RuntimePanelShell } from "./RuntimePanelShell";
import type { LoadStatus, RetrievalData } from "@/types/dashboard";

interface Props {
  traceId: string | null;
  status: LoadStatus;
  retrieval: RetrievalData | null;
}

export function RuntimeNewsPanel({ traceId, status, retrieval }: Props) {
  const chunks = retrieval?.chunks ?? [];
  return (
    <RuntimePanelShell
      traceId={traceId}
      status={status}
      title="News"
      emptyMessage="retrieval 결과가 없습니다."
    >
      {chunks.length === 0 ? (
        <div className="rounded-xl border border-border bg-card/60 p-5 text-sm text-muted-foreground">
          관련 뉴스·공시 chunk가 없습니다.
        </div>
      ) : (
        <RelatedNewsPanel chunks={chunks} />
      )}
    </RuntimePanelShell>
  );
}
