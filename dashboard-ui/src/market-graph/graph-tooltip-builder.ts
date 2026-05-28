import type { MarketGraphEdge, MarketGraphNode } from "@/types/market-graph";
import { EDGE_TYPE_LABELS } from "./graph-edge-types";
import { NODE_CATEGORY_LABELS } from "./graph-node-types";

export function buildNodeTooltip(node: MarketGraphNode): string {
  const cat = NODE_CATEGORY_LABELS[node.category] ?? node.category;
  const lines = [node.label, cat];
  if (node.description) lines.push(node.description);
  if (node.ticker) lines.push(`티커: ${node.ticker}`);
  if (node.is_center) lines.push("선택 종목 (중심)");
  return lines.join("\n");
}

export function buildEdgeTooltip(edge: MarketGraphEdge): string {
  const type = EDGE_TYPE_LABELS[edge.edge_type] ?? edge.edge_type;
  const lines = [
    `${edge.source} → ${edge.target}`,
    `관계: ${type}`,
    `관련도: ${Math.round(edge.relevance * 100)}%`,
  ];
  if (edge.reason) lines.push(`근거: ${edge.reason}`);
  return lines.join("\n");
}
