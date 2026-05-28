"use client";

import type { RelationExplanationItem } from "@/types/market-graph";
import { reasonMacroImpact } from "@/reasoning/macro-relation-reasoner";

export function MacroImpactPanel({ relations }: { relations: RelationExplanationItem[] }) {
  const items = reasonMacroImpact(relations).slice(0, 4);
  if (!items.length) {
    return <p className="text-xs text-muted-foreground">매크로 영향 정보 없음</p>;
  }
  return (
    <ul className="space-y-1 text-xs">
      {items.map((r) => (
        <li key={`${r.source}-${r.target}-${r.relation}`}>
          {r.source} → {r.target} ({r.impact})
        </li>
      ))}
    </ul>
  );
}
