import type { MarketEdgeType } from "@/types/market-graph";

export const EDGE_TYPE_LABELS: Record<MarketEdgeType, string> = {
  SUPPLIES: "공급",
  COMPETES_WITH: "경쟁",
  DEPENDS_ON: "의존",
  AFFECTED_BY: "영향 받음",
  BENEFITS_FROM: "수혜",
  EXPOSED_TO: "리스크 노출",
  RELATED_TO: "연관",
};

export function edgeColor(type?: string): string {
  switch (type) {
    case "SUPPLIES":
      return "#34d399";
    case "COMPETES_WITH":
      return "#f97316";
    case "AFFECTED_BY":
      return "#60a5fa";
    case "BENEFITS_FROM":
      return "#22c55e";
    case "DEPENDS_ON":
      return "#a78bfa";
    case "EXPOSED_TO":
      return "#f87171";
    default:
      return "#52525b";
  }
}
