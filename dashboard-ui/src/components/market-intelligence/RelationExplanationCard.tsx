"use client";

import type { RelationExplanationItem } from "@/types/market-graph";

export function RelationExplanationCard({ item }: { item: RelationExplanationItem }) {
  return (
    <article className="rounded-lg border border-border bg-card/60 p-3 text-xs">
      <p className="font-medium">
        {item.source} → {item.target}
      </p>
      <p className="mt-1 text-muted-foreground">
        {item.relation} · {item.impact} · conf {Math.round(item.confidence * 100)}%
      </p>
      <p className="mt-2 text-foreground/90">{item.explanation}</p>
      {item.evidence?.length ? (
        <p className="mt-2 text-[11px] text-muted-foreground">
          근거: {item.evidence.join(", ")}
        </p>
      ) : null}
    </article>
  );
}
