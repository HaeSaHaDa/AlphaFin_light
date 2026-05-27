"use client";

import { CollapsibleSection } from "@/components/ui/collapsible-section";

interface PromptContextPreviewProps {
  query: string;
  contextLength: number;
  chunkCount: number;
  analysisSummary?: string;
}

export function PromptContextPreview({
  query,
  contextLength,
  chunkCount,
  analysisSummary,
}: PromptContextPreviewProps) {
  const preview = [
    `Query: ${query}`,
    `Retrieved chunks: ${chunkCount}`,
    `Unified context length: ${contextLength} chars`,
    analysisSummary
      ? `Analysis summary: ${analysisSummary.slice(0, 280)}…`
      : "",
  ]
    .filter(Boolean)
    .join("\n\n");

  return (
    <CollapsibleSection title="Prompt / Context Preview" defaultOpen={false}>
      <pre className="max-h-40 overflow-auto whitespace-pre-wrap rounded bg-muted/30 p-2 font-mono text-[11px] text-muted-foreground">
        {preview}
      </pre>
    </CollapsibleSection>
  );
}
