import type { MarketGraphPayload, RelationExplanationItem } from "@/types/market-graph";

export function removeNoiseEntities(payload: MarketGraphPayload): MarketGraphPayload {
  const nodes = payload.nodes.filter((n) => {
    if (n.is_center) return true;
    if (n.label.length <= 1) return false;
    if (n.relevance < 0.4) return false;
    return true;
  });
  const ids = new Set(nodes.map((n) => n.id));
  const edges = payload.edges.filter(
    (e) => ids.has(e.source) && ids.has(e.target),
  );
  return { ...payload, nodes, edges };
}

export function filterWeakRelations(
  relations: RelationExplanationItem[],
): RelationExplanationItem[] {
  return relations.filter((r) => {
    if (r.confidence < 0.55 && r.relation === "RELATED_TO") return false;
    if (!r.explanation?.trim()) return false;
    return true;
  });
}
