"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { CollapsibleSection } from "@/components/ui/collapsible-section";
import { ChunkRankingViewer } from "@/components/retrieval-detail/chunk-ranking-viewer";
import { SimilarityScoreViewer } from "@/components/retrieval-detail/similarity-score-viewer";
import type { AnalysisLoadStatus, RetrievalDetailData } from "@/types/analysis";

interface RetrievalDetailViewerProps {
  data: RetrievalDetailData | null;
  status: AnalysisLoadStatus;
}

export function RetrievalDetailViewer({
  data,
  status,
}: RetrievalDetailViewerProps) {
  const chunks = [...(data?.chunks ?? [])].sort(
    (a, b) => (a.rank ?? 99) - (b.rank ?? 99),
  );

  return (
    <PanelShell
      title="Retrieval Detail"
      subtitle={
        data?.retrieval_timestamp
          ? `retrieved ${data.retrieval_timestamp}`
          : undefined
      }
      status={status}
      empty={!data?.chunks?.length}
      className="min-h-[320px]"
    >
      {data && chunks.length > 0 && (
        <div className="space-y-3">
          <CollapsibleSection title="Chunk Ranking" defaultOpen>
            <ChunkRankingViewer chunks={chunks} />
          </CollapsibleSection>
          <CollapsibleSection title="Similarity Scores" defaultOpen>
            <SimilarityScoreViewer chunks={chunks} />
          </CollapsibleSection>
        </div>
      )}
    </PanelShell>
  );
}
