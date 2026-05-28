import { NODE_CATEGORY_COLORS, NODE_CATEGORY_LABELS } from "./graph-node-types";
import { EDGE_TYPE_LABELS } from "./graph-edge-types";
import type { MarketNodeCategory, MarketEdgeType } from "@/types/market-graph";

export const LEGEND_NODE_CATEGORIES: MarketNodeCategory[] = [
  "company",
  "sector",
  "product",
  "competitor",
  "risk",
  "theme",
];

export const LEGEND_EDGE_TYPES: MarketEdgeType[] = [
  "SUPPLIES",
  "AFFECTED_BY",
  "BENEFITS_FROM",
  "COMPETES_WITH",
  "EXPOSED_TO",
  "DEPENDS_ON",
  "RELATED_TO",
];

export function legendNodeItems() {
  return LEGEND_NODE_CATEGORIES.map((c) => ({
    key: c,
    label: NODE_CATEGORY_LABELS[c],
    color: NODE_CATEGORY_COLORS[c],
  }));
}

export function legendEdgeItems() {
  return LEGEND_EDGE_TYPES.map((t) => ({
    key: t,
    label: EDGE_TYPE_LABELS[t],
  }));
}
