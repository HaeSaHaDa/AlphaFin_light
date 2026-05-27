"use client";

import { ENTITY_COLORS } from "@/lib/event-graph/transform";

const LABELS: Record<string, string> = {
  company: "기업",
  industry: "산업",
  product: "제품",
  market_event: "시장 이벤트",
  price_change: "가격 요소",
  supply_chain: "공급망",
};

export function GraphLegend() {
  return (
    <div className="rounded-lg border border-border bg-card/95 p-3 text-xs">
      <p className="mb-2 font-semibold text-foreground">Legend</p>
      <ul className="space-y-1.5">
        {Object.entries(ENTITY_COLORS).map(([type, color]) => (
          <li key={type} className="flex items-center gap-2">
            <span
              className="h-3 w-3 rounded-full"
              style={{ backgroundColor: color }}
            />
            <span className="text-muted-foreground">{LABELS[type] ?? type}</span>
          </li>
        ))}
      </ul>
      <p className="mt-2 border-t border-border pt-2 text-[10px] text-muted-foreground">
        Edge label = impact score · 굵기 = 영향도
      </p>
    </div>
  );
}
