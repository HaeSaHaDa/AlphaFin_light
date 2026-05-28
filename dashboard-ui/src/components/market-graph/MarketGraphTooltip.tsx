"use client";

import {
  buildEdgeTooltip,
  buildNodeTooltip,
} from "@/market-graph/graph-tooltip-builder";
import type { MarketGraphEdge, MarketGraphNode } from "@/types/market-graph";

export function MarketGraphNodeTooltip({ node }: { node: MarketGraphNode }) {
  return (
    <pre className="whitespace-pre-wrap text-xs leading-relaxed">
      {buildNodeTooltip(node)}
    </pre>
  );
}

export function MarketGraphEdgeTooltip({ edge }: { edge: MarketGraphEdge }) {
  return (
    <pre className="whitespace-pre-wrap text-xs leading-relaxed">
      {buildEdgeTooltip(edge)}
    </pre>
  );
}
