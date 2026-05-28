"use client";

import type { RelationExplanationItem } from "@/types/market-graph";
import { buildSupplyChainRelations } from "@/reasoning/supply-chain-reasoner";

export function SupplyChainPanel({ relations }: { relations: RelationExplanationItem[] }) {
  const items = buildSupplyChainRelations(relations).slice(0, 4);
  if (!items.length) {
    return <p className="text-xs text-muted-foreground">공급망 관계 없음</p>;
  }
  return (
    <ul className="space-y-1 text-xs">
      {items.map((r) => (
        <li key={`${r.source}-${r.target}-${r.relation}`}>
          {r.source} → {r.target} ({r.relation})
        </li>
      ))}
    </ul>
  );
}
