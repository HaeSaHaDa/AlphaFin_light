import type { RetrievalData } from "@/types/dashboard";
import type { MarketGraphEdge } from "@/types/market-graph";

export function buildRelationEvidence(
  edge: MarketGraphEdge,
  retrieval: RetrievalData | null,
): string[] {
  if (edge.evidence?.length) return edge.evidence;
  const chunks = retrieval?.chunks ?? [];
  const picks = chunks
    .slice(0, 2)
    .map((chunk, index) =>
      chunk.title ||
      chunk.text?.split("\n")[0]?.trim() ||
      `근거 문서 ${index + 1}`,
    );
  if (edge.reason) picks.push(`reason:${edge.reason}`);
  return picks.slice(0, 3);
}
