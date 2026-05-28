import type { RelationExplanationItem } from "@/types/market-graph";

const MACRO_KEYWORDS = ["금리", "환율", "유가", "IRA", "중국"];

export function reasonMacroImpact(
  relations: RelationExplanationItem[],
): RelationExplanationItem[] {
  return relations.filter((r) =>
    MACRO_KEYWORDS.some((k) => r.source.includes(k) || r.target.includes(k)),
  );
}
