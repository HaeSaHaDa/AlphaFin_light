import type { MarketEdgeType, RelationExplanationItem } from "@/types/market-graph";

export function calculateRelationConfidence(
  relation: MarketEdgeType,
  baseScore: number,
  evidenceCount: number,
): number {
  const relationBias =
    relation === "SUPPLIES" || relation === "EXPOSED_TO" || relation === "BENEFITS_FROM"
      ? 0.06
      : 0;
  const evidenceBonus = Math.min(0.2, evidenceCount * 0.05);
  const score = baseScore + relationBias + evidenceBonus;
  return Math.round(Math.min(0.98, Math.max(0.4, score)) * 1000) / 1000;
}

export function rankByConfidence<T extends RelationExplanationItem>(items: T[]): T[] {
  return [...items].sort((a, b) => b.confidence - a.confidence);
}
