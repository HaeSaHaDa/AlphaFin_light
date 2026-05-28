import type {
  MarketInsightPayload,
  RelationExplanationItem,
} from "@/types/market-graph";
import { calculateRelationConfidence, rankByConfidence } from "./relation-confidence";
import { filterWeakRelations } from "./graph-semantic-filter";

export function reasonMarketRelations(
  insight: MarketInsightPayload | null,
): RelationExplanationItem[] {
  const base = insight?.key_relations ?? [];
  const scored = base.map((r) => ({
    ...r,
    confidence: calculateRelationConfidence(
      r.relation,
      r.confidence ?? 0.55,
      r.evidence?.length ?? 0,
    ),
  }));
  return rankByConfidence(filterWeakRelations(scored));
}
