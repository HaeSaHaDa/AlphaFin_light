import type { RelationExplanationItem } from "@/types/market-graph";

export function buildSupplyChainRelations(
  relations: RelationExplanationItem[],
): RelationExplanationItem[] {
  return relations.filter(
    (r) => r.relation === "SUPPLIES" || r.relation === "DEPENDS_ON",
  );
}
