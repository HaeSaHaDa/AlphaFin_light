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

const DEMO_PROPAGATION: PropagationStep[] = [
  { source: "NVIDIA", target: "GPU", relation_type: "supply", impact_score: 0.85 },
  { source: "GPU", target: "AI 서버", relation_type: "demand_propagation", impact_score: 0.82 },
  { source: "AI 서버", target: "HBM", relation_type: "demand_propagation", impact_score: 0.88 },
  { source: "HBM", target: "삼성전자", relation_type: "supply", impact_score: 0.8 },
  { source: "HBM", target: "DRAM", relation_type: "product_link", impact_score: 0.75 },
  { source: "DRAM", target: "dram price", relation_type: "price_impact", impact_score: 0.72 },
];

const DEMO_TEMPORAL: TemporalEvent[] = [
  { period: "2024-01", label: "NVIDIA 실적 발표", relation: "earnings_release" },
  { period: "2024-02", label: "HBM 공급 부족 심화", relation: "supply_shortage" },
  { period: "2024-03", label: "DRAM 가격 상승", relation: "price_increase" },
];

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
): EventGraphPayload {
  const chain = data.chain ?? {};
  const entities: GraphEntity[] = (chain.entities ?? []).map((e) => ({
    ...e,
    id: e.name,
  }));
  const links: GraphLink[] = (chain.links ?? []).map((l, i) => ({
    ...l,
    id: `e-${i}-${l.source}-${l.target}`,
  }));

  const propagationPath = extractPropagationPath(links) ?? DEMO_PROPAGATION;
  const temporalEvents = buildTemporalEvents(traceCompletedAt);

  return {
    traceId: data.trace_id,
    query: data.query,
    ticker: data.ticker,
    entities,
    links,
    propagationPath,
    temporalEvents,
  };
}

function extractPropagationPath(links: GraphLink[]): PropagationStep[] | null {
  const preferred = ["NVIDIA", "GPU", "AI 서버", "HBM", "삼성전자", "DRAM"];
  const steps: PropagationStep[] = [];
  for (let i = 0; i < preferred.length - 1; i++) {
    const link = links.find(
      (l) =>
        l.source === preferred[i] &&
        (l.target === preferred[i + 1] ||
          l.target.toLowerCase().includes(preferred[i + 1].toLowerCase())),
    );
    if (link) {
      steps.push({
        source: link.source,
        target: link.target,
        relation_type: link.relation_type ?? "propagation",
        impact_score: link.impact_score ?? 0,
      });
    }
  }
  return steps.length >= 3 ? steps : null;
}

function buildTemporalEvents(completedAt?: string): TemporalEvent[] {
  if (!completedAt) return DEMO_TEMPORAL;
  const base = completedAt.slice(0, 7);
  return [
    { period: base, label: "Engine trace · retrieval", relation: "retrieval" },
    ...DEMO_TEMPORAL,
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
): { nodes: Node[]; edges: Edge[] } {
  const highlight = new Set(
    filters.highlightEntities.map((h) => h.toLowerCase()),
  );
  const positions = layoutNodes(entities, links);

  const nodes: Node[] = entities.map((e) => ({
    id: e.id,
    type: "graphNode",
    position: positions.get(e.id) ?? { x: 0, y: 0 },
    data: {
      label: e.name,
      entityType: e.entity_type,
      ticker: e.ticker,
      highlighted:
        highlight.size > 0 && highlight.has(e.name.toLowerCase()),
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
): Map<string, { x: number; y: number }> {
  const seeds = ["NVIDIA", "삼성전자", "HBM"];
  const root =
    seeds.find((s) => entities.some((e) => e.name === s)) ??
    entities[0]?.name ??
    "";

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
