"use client";

import { legendEdgeItems, legendNodeItems } from "@/market-graph/graph-legend";

export function MarketGraphLegend() {
  const nodes = legendNodeItems();
  const edges = legendEdgeItems();

  return (
    <div className="space-y-3 text-xs">
      <div>
        <p className="mb-1 font-medium text-muted-foreground">Node</p>
        <ul className="space-y-1">
          {nodes.map((n) => (
            <li key={n.key} className="flex items-center gap-2">
              <span
                className="inline-block h-2.5 w-2.5 rounded-full"
                style={{ backgroundColor: n.color }}
              />
              {n.label}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <p className="mb-1 font-medium text-muted-foreground">Edge</p>
        <ul className="space-y-0.5 text-muted-foreground">
          {edges.map((e) => (
            <li key={e.key}>{e.label}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
