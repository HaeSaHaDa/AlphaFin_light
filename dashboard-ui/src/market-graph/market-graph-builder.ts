import type { Node, Edge } from "@xyflow/react";
import type {
  MarketGraphFilters,
  MarketGraphNode,
  MarketGraphEdge,
  MarketGraphPayload,
} from "@/types/market-graph";
import { filterGraphByTicker } from "./graph-filter";
import { nodeColor } from "./graph-node-types";
import { edgeColor } from "./graph-edge-types";

export function buildMarketGraph(payload: MarketGraphPayload): MarketGraphPayload {
  return payload;
}

export function buildTickerCenteredGraph(
  payload: MarketGraphPayload,
  filters: MarketGraphFilters,
): { nodes: MarketGraphNode[]; edges: MarketGraphEdge[] } {
  return filterGraphByTicker(payload, filters);
}

function layoutFromCenter(
  centerId: string,
  nodes: MarketGraphNode[],
  edges: MarketGraphEdge[],
): Map<string, { x: number; y: number }> {
  const adj = new Map<string, string[]>();
  edges.forEach((e) => {
    if (!adj.has(e.source)) adj.set(e.source, []);
    adj.get(e.source)!.push(e.target);
    if (!adj.has(e.target)) adj.set(e.target, []);
    adj.get(e.target)!.push(e.source);
  });

  const level = new Map<string, number>();
  const queue = [centerId];
  level.set(centerId, 0);
  while (queue.length) {
    const cur = queue.shift()!;
    for (const nb of adj.get(cur) ?? []) {
      if (!level.has(nb)) {
        level.set(nb, (level.get(cur) ?? 0) + 1);
        queue.push(nb);
      }
    }
  }
  nodes.forEach((n) => {
    if (!level.has(n.id)) level.set(n.id, 1);
  });

  const byLevel = new Map<number, string[]>();
  nodes.forEach((n) => {
    const lv = level.get(n.id) ?? 0;
    if (!byLevel.has(lv)) byLevel.set(lv, []);
    byLevel.get(lv)!.push(n.id);
  });

  const positions = new Map<string, { x: number; y: number }>();
  const xGap = 240;
  const yGap = 88;
  byLevel.forEach((ids, lv) => {
    ids.forEach((id, i) => {
      positions.set(id, {
        x: lv * xGap,
        y: i * yGap - ((ids.length - 1) * yGap) / 2,
      });
    });
  });
  return positions;
}

export function toMarketFlowElements(
  nodes: MarketGraphNode[],
  edges: MarketGraphEdge[],
  centerId: string,
): { nodes: Node[]; edges: Edge[] } {
  const positions = layoutFromCenter(centerId, nodes, edges);

  const flowNodes: Node[] = nodes.map((n) => ({
    id: n.id,
    type: "graphNode",
    position: positions.get(n.id) ?? { x: 0, y: 0 },
    data: {
      label: n.label,
      entityType: n.category,
      ticker: n.ticker,
      isCenter: n.is_center,
      highlighted: n.is_center,
      description: n.description,
    },
  }));

  const flowEdges: Edge[] = edges.map((e) => ({
    id: e.id,
    source: e.source,
    target: e.target,
    type: "graphEdge",
    animated: e.relevance >= 0.8,
    data: {
      relationType: e.edge_type,
      impactScore: e.relevance,
      reason: e.reason,
    },
    label: e.edge_type,
    style: {
      stroke: edgeColor(e.edge_type),
      strokeWidth: 1 + e.relevance * 2,
    },
    markerEnd: {
      type: "arrowclosed" as const,
      color: edgeColor(e.edge_type),
    },
  }));

  return { nodes: flowNodes, edges: flowEdges };
}

export { nodeColor };
