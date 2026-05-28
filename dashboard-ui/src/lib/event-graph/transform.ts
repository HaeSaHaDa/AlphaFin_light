import type { Node, Edge } from "@xyflow/react";
import type {
  EventGraphFilters,
  EventGraphPayload,
  GraphEntity,
  GraphLink,
  PropagationStep,
  TemporalEvent,
} from "@/types/event-graph";
import type { StockChainData } from "@/types/dashboard";
import { buildTickerCentricChain } from "@/lib/ticker-centric-chain";

const ENTITY_COLORS: Record<string, string> = {
  company: "#3b82f6",
  industry: "#a855f7",
  product: "#22c55e",
  market_event: "#f59e0b",
  price_change: "#ef4444",
  supply_chain: "#64748b",
};

export function entityColor(type?: string): string {
  return ENTITY_COLORS[type ?? ""] ?? "#71717a";
}

export function buildPayloadFromStockChain(
  data: StockChainData,
  traceCompletedAt?: string,
  retrievalChunks?: Array<{
    document_type?: string;
    chunk_id?: number;
    score?: number;
    ticker?: string;
  }>,
): EventGraphPayload {
  const centered = buildTickerCentricChain(data, retrievalChunks);
  const propagationPath =
    extractPropagationPath(centered.links, centered.centerName) ?? [];
  const temporalEvents = buildTemporalEvents(traceCompletedAt);

  return {
    traceId: data.trace_id,
    query: data.query,
    ticker: data.ticker,
    centerName: data.center_name || centered.centerName,
    centerTicker: data.center_ticker || centered.centerTicker,
    entities: centered.entities,
    links: centered.links,
    propagationPath,
    temporalEvents,
  };
}

function extractPropagationPath(
  links: GraphLink[],
  centerName: string,
): PropagationStep[] | null {
  if (!links.length || !centerName) return null;
  const fromCenter = links.filter(
    (l) => l.source === centerName || l.target === centerName,
  );
  const pool = fromCenter.length ? fromCenter : links;
  const sorted = [...pool].sort(
    (a, b) => (b.impact_score ?? 0) - (a.impact_score ?? 0),
  );
  return sorted.slice(0, 8).map((l) => ({
    source: l.source,
    target: l.target,
    relation_type: l.relation_type ?? "propagation",
    impact_score: l.impact_score ?? 0,
  }));
}

function buildTemporalEvents(completedAt?: string): TemporalEvent[] {
  if (!completedAt) return [];
  const base = completedAt.slice(0, 7);
  return [
    { period: base, label: "Engine trace · retrieval", relation: "retrieval" },
  ];
}

export function applyFilters(
  payload: EventGraphPayload,
  filters: EventGraphFilters,
): { entities: GraphEntity[]; links: GraphLink[] } {
  let links = payload.links.filter(
    (l) => (l.impact_score ?? 0) >= filters.minImpact,
  );

  if (filters.entityType !== "all") {
    const names = new Set(
      payload.entities
        .filter((e) => e.entity_type === filters.entityType)
        .map((e) => e.name),
    );
    links = links.filter((l) => names.has(l.source) || names.has(l.target));
  }

  const nodeNames = new Set<string>();
  links.forEach((l) => {
    nodeNames.add(l.source);
    nodeNames.add(l.target);
  });

  if (filters.search.trim()) {
    const q = filters.search.trim().toLowerCase();
    const matched = new Set(
      [...nodeNames].filter((n) => n.toLowerCase().includes(q)),
    );
    links = links.filter(
      (l) => matched.has(l.source) || matched.has(l.target),
    );
    matched.forEach((n) => nodeNames.add(n));
    payload.entities
      .filter((e) => e.name.toLowerCase().includes(q))
      .forEach((e) => nodeNames.add(e.name));
  }

  const entities = payload.entities.filter((e) => nodeNames.has(e.name));
  return { entities, links };
}

export function toFlowElements(
  entities: GraphEntity[],
  links: GraphLink[],
  filters: EventGraphFilters,
  centerName: string,
): { nodes: Node[]; edges: Edge[] } {
  const highlight = new Set(
    filters.highlightEntities.map((h) => h.toLowerCase()),
  );
  const rootName =
    centerName ||
    entities.find((e) => e.is_center)?.name ||
    "";
  const positions = layoutNodes(entities, links, rootName);

  const nodes: Node[] = entities.map((e) => ({
    id: e.id,
    type: "graphNode",
    position: positions.get(e.id) ?? { x: 0, y: 0 },
    data: {
      label: e.name,
      entityType: e.entity_type,
      ticker: e.ticker,
      isCenter: Boolean(e.is_center),
      highlighted:
        e.is_center ||
        (highlight.size > 0 && highlight.has(e.name.toLowerCase())),
    },
  }));

  const edges: Edge[] = links.map((l) => ({
    id: l.id,
    source: l.source,
    target: l.target,
    type: "graphEdge",
    animated: (l.impact_score ?? 0) >= 0.85,
    data: {
      relationType: l.relation_type,
      impactScore: l.impact_score,
    },
    label: `${((l.impact_score ?? 0) * 100).toFixed(0)}%`,
    style: {
      stroke: edgeStroke(l.impact_score),
      strokeWidth: 1 + (l.impact_score ?? 0.5) * 2,
    },
    markerEnd: { type: "arrowclosed" as const, color: edgeStroke(l.impact_score) },
  }));

  return { nodes, edges };
}

function edgeStroke(score?: number): string {
  const s = score ?? 0.5;
  if (s >= 0.85) return "#60a5fa";
  if (s >= 0.75) return "#34d399";
  return "#52525b";
}

function layoutNodes(
  entities: GraphEntity[],
  links: GraphLink[],
  centerName: string,
): Map<string, { x: number; y: number }> {
  const root =
    centerName ||
    entities.find((e) => e.is_center)?.name ||
    entities.find((e) => e.ticker)?.name ||
    "";
  if (!root) {
    return new Map();
  }

  const adj = new Map<string, string[]>();
  links.forEach((l) => {
    if (!adj.has(l.source)) adj.set(l.source, []);
    adj.get(l.source)!.push(l.target);
  });

  const level = new Map<string, number>();
  const queue = [root];
  level.set(root, 0);
  while (queue.length) {
    const cur = queue.shift()!;
    for (const next of adj.get(cur) ?? []) {
      if (!level.has(next)) {
        level.set(next, (level.get(cur) ?? 0) + 1);
        queue.push(next);
      }
    }
  }

  entities.forEach((e) => {
    if (!level.has(e.name)) level.set(e.name, 0);
  });

  const byLevel = new Map<number, string[]>();
  entities.forEach((e) => {
    const lv = level.get(e.name) ?? 0;
    if (!byLevel.has(lv)) byLevel.set(lv, []);
    byLevel.get(lv)!.push(e.name);
  });

  const positions = new Map<string, { x: number; y: number }>();
  const xGap = 220;
  const yGap = 90;

  byLevel.forEach((names, lv) => {
    names.forEach((name, i) => {
      positions.set(name, {
        x: lv * xGap,
        y: i * yGap - ((names.length - 1) * yGap) / 2,
      });
    });
  });

  return positions;
}

export { ENTITY_COLORS };
