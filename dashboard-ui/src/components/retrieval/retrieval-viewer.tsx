"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { Badge } from "@/components/ui/badge";
import { formatScore } from "@/lib/utils";
import type { LoadStatus, RetrievalData } from "@/types/dashboard";

interface RetrievalViewerProps {
  data: RetrievalData | null;
  status: LoadStatus;
}

export function RetrievalViewer({ data, status }: RetrievalViewerProps) {
  const chunks = data?.chunks ?? [];
  const stats = (data?.retrieval_quality as { score_stats?: { avg?: number } })
    ?.score_stats;

  return (
    <PanelShell
      title="Retrieval Viewer"
      subtitle={`${data?.chunk_count ?? 0} chunks · ${data?.ticker ?? ""}`}
      status={status}
      empty={!data}
    >
      {data && (
        <div className="space-y-3">
          <div className="flex flex-wrap gap-2 text-xs">
            <Badge variant="secondary">
              avg score: {formatScore(stats?.avg)}
            </Badge>
            <Badge variant="outline">
              context: {data.unified_context_length} chars
            </Badge>
          </div>
          <ul className="space-y-2">
            {chunks.map((chunk, i) => (
              <li
                key={`${chunk.chunk_id}-${i}`}
                className="rounded-md border border-border/60 bg-muted/30 p-2 text-xs"
              >
                <div className="mb-1 flex items-center justify-between gap-2">
                  <span className="font-medium text-primary">
                    #{i + 1} · chunk {chunk.chunk_id}
                  </span>
                  <Badge variant="success">
                    {formatScore(chunk.score)}
                  </Badge>
                </div>
                <p className="text-muted-foreground">
                  source: {chunk.document_type ?? "unknown"}
                  {chunk.ticker ? ` · ${chunk.ticker}` : ""}
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </PanelShell>
  );
}
