"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { Badge } from "@/components/ui/badge";
import { PromptContextPreview } from "@/components/context-viewer/prompt-context-preview";
import type { AnalysisLoadStatus, RetrievalDetailData } from "@/types/analysis";

interface ContextAssemblyViewerProps {
  data: RetrievalDetailData | null;
  status: AnalysisLoadStatus;
}

export function ContextAssemblyViewer({
  data,
  status,
}: ContextAssemblyViewerProps) {
  const layers = data?.context_layers;

  return (
    <PanelShell
      title="Context Assembly"
      subtitle={`${data?.unified_context_length ?? 0} chars unified`}
      status={status}
      empty={!data}
      className="min-h-[320px]"
    >
      {data && (
        <div className="space-y-3 text-sm">
          <LayerBlock
            title="Retrieval Context"
            items={[
              `chunks: ${layers?.retrieval?.chunk_count ?? data.chunk_count}`,
              `length: ${layers?.retrieval?.context_length ?? data.unified_context_length}`,
            ]}
          />
          <LayerBlock
            title="Memory Context"
            items={memoryItems(layers?.memory as Record<string, unknown>)}
          />
          <LayerBlock
            title="Reflection Context"
            items={[reflectionPreview(layers?.reflection)]}
          />
          <LayerBlock
            title="Stock Chain Context"
            items={stockChainItems(layers?.stock_chain as Record<string, unknown>)}
          />
          <PromptContextPreview
            query={data.query}
            contextLength={data.unified_context_length}
            chunkCount={data.chunk_count}
            analysisSummary={data.analysis?.summary}
          />
        </div>
      )}
    </PanelShell>
  );
}

function LayerBlock({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-md border border-border/50 p-2">
      <div className="mb-1 flex items-center gap-2">
        <Badge variant="outline">{title}</Badge>
      </div>
      <ul className="list-inside list-disc text-xs text-muted-foreground">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function reflectionPreview(reflection: unknown): string {
  const summary = (reflection as { reflection_summary?: string })
    ?.reflection_summary;
  if (!summary) return "—";
  return summary.length > 120 ? `${summary.slice(0, 120)}…` : summary;
}

function memoryItems(memory: Record<string, unknown> | undefined): string[] {
  if (!memory) return ["—"];
  const imp = memory.importance as { importance_score?: number } | undefined;
  const layered = memory.layered_memory as { layer?: string; memory_count?: number } | undefined;
  return [
    layered?.layer ? `layer: ${layered.layer}` : "",
    layered?.memory_count != null ? `memories: ${layered.memory_count}` : "",
    imp?.importance_score != null
      ? `importance: ${(imp.importance_score * 100).toFixed(0)}%`
      : "",
  ].filter(Boolean);
}

function stockChainItems(sc: Record<string, unknown> | undefined): string[] {
  if (!sc) return ["—"];
  return [
    sc.entity_count != null ? `entities: ${sc.entity_count}` : "",
    sc.link_count != null ? `links: ${sc.link_count}` : "",
    sc.propagation_paths != null ? `paths: ${sc.propagation_paths}` : "",
  ].filter(Boolean);
}
