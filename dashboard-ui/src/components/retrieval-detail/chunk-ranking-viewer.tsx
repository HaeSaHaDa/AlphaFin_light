"use client";

import { Badge } from "@/components/ui/badge";
import { formatScore } from "@/lib/utils";
import type { EnrichedChunk } from "@/types/analysis";

interface ChunkRankingViewerProps {
  chunks: EnrichedChunk[];
}

export function ChunkRankingViewer({ chunks }: ChunkRankingViewerProps) {
  return (
    <ol className="space-y-2">
      {chunks.map((chunk) => (
        <li
          key={`rank-${chunk.rank}-${chunk.chunk_id}`}
          className="flex items-start gap-2 rounded-md border border-border/50 bg-muted/20 p-2 text-xs"
        >
          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded bg-primary/20 font-bold text-primary">
            {chunk.rank}
          </span>
          <div className="min-w-0 flex-1">
            <p className="font-medium">{chunk.chunk_preview}</p>
            <p className="mt-0.5 truncate text-muted-foreground">
              {chunk.source_file}
            </p>
          </div>
          <Badge variant="success">{formatScore(chunk.score)}</Badge>
        </li>
      ))}
    </ol>
  );
}
