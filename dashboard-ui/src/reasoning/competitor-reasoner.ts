import type { RelationExplanationItem } from "@/types/market-graph";

export function reasonCompetitors(
  relations: RelationExplanationItem[],
): RelationExplanationItem[] {
  return relations.filter((r) => r.relation === "COMPETES_WITH");
}
