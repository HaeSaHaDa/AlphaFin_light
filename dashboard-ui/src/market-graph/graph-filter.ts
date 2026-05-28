import type {
  MarketGraphFilters,
  MarketGraphNode,
  MarketGraphEdge,
  MarketGraphPayload,
} from "@/types/market-graph";

export function filterGraphByTicker(
  payload: MarketGraphPayload,
  filters: MarketGraphFilters,
): { nodes: MarketGraphNode[]; edges: MarketGraphEdge[] } {
  const centerId =
    payload.nodes.find((n) => n.is_center)?.id ?? payload.center_company;

  let nodes = payload.nodes.filter((n) => n.relevance >= filters.minRelevance);
  if (filters.category !== "all") {
    nodes = nodes.filter(
      (n) => n.is_center || n.category === filters.category,
    );
  }

  const nodeIds = new Set(nodes.map((n) => n.id));
  nodeIds.add(centerId);

  let edges = payload.edges.filter((e) => e.relevance >= filters.minRelevance);
  if (filters.edgeType !== "all") {
    edges = edges.filter((e) => e.edge_type === filters.edgeType);
  }

  edges = edges.filter(
    (e) => nodeIds.has(e.source) && nodeIds.has(e.target),
  );

  edges.forEach((e) => {
    nodeIds.add(e.source);
    nodeIds.add(e.target);
  });

  nodes = payload.nodes.filter((n) => nodeIds.has(n.id));
  if (!nodes.some((n) => n.is_center)) {
    const center = payload.nodes.find((n) => n.is_center);
    if (center) nodes = [center, ...nodes];
  }

  return { nodes, edges };
}
