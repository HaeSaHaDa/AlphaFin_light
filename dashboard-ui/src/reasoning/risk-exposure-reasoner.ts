import type { RelationExplanationItem } from "@/types/market-graph";

export function reasonRiskExposure(
  relations: RelationExplanationItem[],
): RelationExplanationItem[] {
  return relations.filter((r) => r.relation === "EXPOSED_TO");
}
