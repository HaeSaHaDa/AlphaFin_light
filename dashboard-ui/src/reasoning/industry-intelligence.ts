import type { RelationExplanationItem } from "@/types/market-graph";

const INDUSTRY_HINTS = ["산업", "업종", "반도체", "자동차", "배터리", "전기차"];

export function reasonIndustryRelations(
  relations: RelationExplanationItem[],
): RelationExplanationItem[] {
  return relations.filter((r) =>
    INDUSTRY_HINTS.some((k) => r.source.includes(k) || r.target.includes(k)),
  );
}
