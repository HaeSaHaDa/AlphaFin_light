import type { RelationExplanationItem } from "@/types/market-graph";

export function relationDirection(
  source: string,
  target: string,
  centerCompany: string,
  relation: string,
): RelationExplanationItem["direction"] {
  if (relation === "AFFECTED_BY" || relation === "BENEFITS_FROM") {
    if (target === centerCompany) return "inbound";
  }
  if (source === centerCompany) return "outbound";
  if (target === centerCompany) return "inbound";
  return "lateral";
}
