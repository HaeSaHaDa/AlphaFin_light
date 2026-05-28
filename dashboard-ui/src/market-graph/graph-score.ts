import type { MarketGraphEdge, MarketGraphNode } from "@/types/market-graph";

export function scoreNode(node: MarketGraphNode): number {
  if (node.is_center) return 1;
  return node.relevance ?? 0.5;
}

export function scoreEdge(edge: MarketGraphEdge): number {
  return edge.relevance ?? 0.5;
}

export function sortNodesByRelevance(nodes: MarketGraphNode[]): MarketGraphNode[] {
  return [...nodes].sort((a, b) => scoreNode(b) - scoreNode(a));
}
