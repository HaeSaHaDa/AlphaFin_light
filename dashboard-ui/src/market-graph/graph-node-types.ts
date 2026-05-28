import type { MarketNodeCategory } from "@/types/market-graph";

export const NODE_CATEGORY_LABELS: Record<MarketNodeCategory, string> = {
  company: "기업",
  sector: "산업",
  product: "제품",
  risk: "리스크",
  theme: "테마",
  macro: "매크로",
  competitor: "경쟁사",
  customer: "고객",
};

export const NODE_CATEGORY_COLORS: Record<MarketNodeCategory, string> = {
  company: "#3b82f6",
  sector: "#a855f7",
  product: "#22c55e",
  risk: "#ef4444",
  theme: "#f59e0b",
  macro: "#64748b",
  competitor: "#f97316",
  customer: "#06b6d4",
};

export function nodeColor(category?: string): string {
  return (
    NODE_CATEGORY_COLORS[category as MarketNodeCategory] ?? "#71717a"
  );
}
