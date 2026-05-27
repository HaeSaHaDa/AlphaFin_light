"use client";

import { ScoreBar } from "@/components/ui/score-bar";
import type { EnrichedChunk } from "@/types/analysis";

interface SimilarityScoreViewerProps {
  chunks: EnrichedChunk[];
}

export function SimilarityScoreViewer({ chunks }: SimilarityScoreViewerProps) {
  const maxScore = Math.max(...chunks.map((c) => c.score ?? 0), 0.01);
  return (
    <div className="space-y-2">
      {chunks.map((chunk) => (
        <ScoreBar
          key={`sim-${chunk.rank}-${chunk.chunk_id}`}
          score={(chunk.score ?? 0) / maxScore}
          label={`#${chunk.rank} · ${chunk.document_type ?? "source"}`}
        />
      ))}
    </div>
  );
}
