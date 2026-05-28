"use client";

import { RetrievalViewer } from "@/components/retrieval/retrieval-viewer";
import { RuntimePanelShell } from "./RuntimePanelShell";
import type { LoadStatus, RetrievalData } from "@/types/dashboard";

interface Props {
  traceId: string | null;
  status: LoadStatus;
  retrieval: RetrievalData | null;
}

export function RuntimeRetrievalPanel({ traceId, status, retrieval }: Props) {
  return (
    <RuntimePanelShell
      traceId={traceId}
      status={status}
      title="Retrieval"
      emptyMessage="retrieval 결과가 없습니다."
    >
      <RetrievalViewer data={retrieval} status={status} />
    </RuntimePanelShell>
  );
}
