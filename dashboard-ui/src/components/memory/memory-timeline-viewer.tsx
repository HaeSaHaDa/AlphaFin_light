"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { Badge } from "@/components/ui/badge";
import type { LoadStatus, MemoryData } from "@/types/dashboard";

interface MemoryTimelineViewerProps {
  data: MemoryData | null;
  status: LoadStatus;
}

const LAYERS = [
  { key: "short_term", label: "Short-term", color: "text-sky-300" },
  { key: "mid_term", label: "Mid-term", color: "text-violet-300" },
  { key: "long_term", label: "Long-term", color: "text-amber-300" },
] as const;

export function MemoryTimelineViewer({
  data,
  status,
}: MemoryTimelineViewerProps) {
  const temporal = data?.temporal_result as {
    evolution?: {
      evolution_chains?: string[];
      evolution_stage?: string;
      current_layer?: string;
    };
    action?: string;
  };
  const evolution = temporal?.evolution;

  return (
    <PanelShell
      title="Memory Timeline"
      subtitle="Layered memory lifecycle"
      status={status}
      empty={!data}
      className="min-h-[280px]"
    >
      {data && (
        <div className="space-y-4 text-sm">
          {evolution && (
            <div className="rounded-md border border-border/60 bg-muted/20 p-2">
              <div className="mb-2 flex flex-wrap gap-2">
                <Badge variant="secondary">
                  layer: {evolution.current_layer}
                </Badge>
                <Badge variant="outline">
                  action: {temporal?.action ?? "—"}
                </Badge>
                <Badge variant="outline">
                  stage: {evolution.evolution_stage}
                </Badge>
              </div>
              {evolution.evolution_chains?.map((chain) => (
                <p key={chain} className="text-xs text-muted-foreground">
                  → {chain}
                </p>
              ))}
            </div>
          )}
          {LAYERS.map(({ key, label, color }) => {
            const items =
              data.layered_memory?.[key as keyof typeof data.layered_memory] ??
              [];
            const count = data.layer_counts?.[key] ?? items.length;
            return (
              <div key={key} className="relative border-l-2 border-border pl-3">
                <h4 className={`text-xs font-semibold ${color}`}>
                  {label} ({count})
                </h4>
                <ul className="mt-1 space-y-1">
                  {items.slice(0, 3).map((m, i) => (
                    <li
                      key={`${key}-${i}`}
                      className="truncate text-xs text-muted-foreground"
                    >
                      {(m as { query?: string }).query ??
                        (m as { summary?: string }).summary?.slice(0, 60) ??
                        "memory"}
                      {(m as { importance_score?: number }).importance_score !=
                        null && (
                        <span className="ml-1 text-foreground/60">
                          · imp{" "}
                          {(
                            (m as { importance_score: number })
                              .importance_score * 100
                          ).toFixed(0)}
                          %
                        </span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>
      )}
    </PanelShell>
  );
}
