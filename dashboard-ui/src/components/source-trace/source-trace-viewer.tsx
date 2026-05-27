"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import type { AnalysisLoadStatus, RetrievalDetailData } from "@/types/analysis";

interface SourceTraceViewerProps {
  data: RetrievalDetailData | null;
  status: AnalysisLoadStatus;
  ticker?: string;
}

export function SourceTraceViewer({
  data,
  status,
  ticker,
}: SourceTraceViewerProps) {
  const chunks = data?.chunks ?? [];

  return (
    <PanelShell
      title="Source Trace"
      subtitle="chunk · path · entity"
      status={status}
      empty={!chunks.length}
      className="max-h-none"
    >
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-border text-muted-foreground">
              <th className="py-2 pr-2">Order</th>
              <th className="py-2 pr-2">Chunk ID</th>
              <th className="py-2 pr-2">Source Path</th>
              <th className="py-2">Entity</th>
            </tr>
          </thead>
          <tbody>
            {chunks.map((c) => (
              <tr
                key={`trace-${c.rank}-${c.chunk_id}`}
                className="border-b border-border/40"
              >
                <td className="py-2 pr-2 font-mono text-primary">#{c.rank}</td>
                <td className="py-2 pr-2 font-mono">{c.chunk_id}</td>
                <td className="max-w-[200px] truncate py-2 pr-2 text-muted-foreground">
                  {c.source_file}
                </td>
                <td className="py-2">{c.related_entity ?? ticker ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </PanelShell>
  );
}
