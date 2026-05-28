"use client";

import type { RelationExplanationItem } from "@/types/market-graph";
import { reasonIndustryRelations } from "@/reasoning/industry-intelligence";

export function IndustryRelationPanel({ relations }: { relations: RelationExplanationItem[] }) {
  const items = reasonIndustryRelations(relations).slice(0, 4);
  if (!items.length) {
    return <p className="text-xs text-muted-foreground">산업 관계 정보 없음</p>;
  }
  return (
    <ul className="space-y-1 text-xs">
      {items.map((r) => (
        <li key={`${r.source}-${r.target}-${r.relation}`}>
          {r.source} → {r.target}
        </li>
      ))}
    </ul>
  );
}
