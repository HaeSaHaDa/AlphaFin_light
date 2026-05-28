"use client";

import type { MarketGraphEdge } from "@/types/market-graph";
import { EDGE_TYPE_LABELS } from "@/market-graph/graph-edge-types";
import { MarketGraphEdgeTooltip } from "./MarketGraphTooltip";

export function GraphEdgeInfoPanel({ edge }: { edge: MarketGraphEdge | null }) {
  if (!edge) {
    return null;
  }
  return (
    <div className="rounded border border-border bg-muted/20 p-2 text-xs">
      <p className="font-medium">
        {EDGE_TYPE_LABELS[edge.edge_type] ?? edge.edge_type}
      </p>
      <MarketGraphEdgeTooltip edge={edge} />
    </div>
  );
}
