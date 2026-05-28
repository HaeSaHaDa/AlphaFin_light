"use client";

import type { MarketGraphNode } from "@/types/market-graph";
import { NODE_CATEGORY_LABELS } from "@/market-graph/graph-node-types";
import { MarketGraphNodeTooltip } from "./MarketGraphTooltip";

export function GraphNodeDetailPanel({ node }: { node: MarketGraphNode | null }) {
  if (!node) {
    return (
      <p className="text-xs text-muted-foreground">노드를 선택하면 상세가 표시됩니다.</p>
    );
  }
  return (
    <div className="space-y-2 text-sm">
      <p className="font-semibold">{node.label}</p>
      <p className="text-xs text-muted-foreground">
        {NODE_CATEGORY_LABELS[node.category] ?? node.category}
        {node.ticker ? ` · ${node.ticker}` : ""}
        {node.is_center ? " · 중심 종목" : ""}
      </p>
      <MarketGraphNodeTooltip node={node} />
    </div>
  );
}
