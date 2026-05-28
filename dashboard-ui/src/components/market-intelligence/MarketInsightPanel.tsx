"use client";

import type {
  MarketInsightPayload,
  RelationExplanationItem,
  RiskExposurePayload,
} from "@/types/market-graph";
import { reasonMarketRelations } from "@/reasoning/market-relation-reasoner";
import { RelationExplanationCard } from "./RelationExplanationCard";
import { SupplyChainPanel } from "./SupplyChainPanel";
import { MacroImpactPanel } from "./MacroImpactPanel";
import { IndustryRelationPanel } from "./IndustryRelationPanel";
import { RiskExposurePanel } from "./RiskExposurePanel";

interface Props {
  insight: MarketInsightPayload | null;
  riskExposure: RiskExposurePayload | null;
}

export function MarketInsightPanel({ insight, riskExposure }: Props) {
  const relations = reasonMarketRelations(insight);
  if (!insight) {
    return <p className="text-xs text-muted-foreground">Market Insight 없음</p>;
  }
  return (
    <section className="space-y-3 rounded-lg border border-border bg-card/50 p-3">
      <div>
        <p className="text-sm font-semibold">Explainable Market Insight</p>
        <p className="mt-1 text-xs text-muted-foreground">{insight.market_story}</p>
      </div>

      <div className="grid gap-3 lg:grid-cols-2">
        <article>
          <p className="mb-1 text-xs font-medium text-muted-foreground">산업 인텔리전스</p>
          <IndustryRelationPanel relations={relations} />
        </article>
        <article>
          <p className="mb-1 text-xs font-medium text-muted-foreground">공급망 관계</p>
          <SupplyChainPanel relations={relations} />
        </article>
        <article>
          <p className="mb-1 text-xs font-medium text-muted-foreground">매크로 영향</p>
          <MacroImpactPanel relations={relations} />
        </article>
        <article>
          <p className="mb-1 text-xs font-medium text-muted-foreground">리스크 노출</p>
          <RiskExposurePanel data={riskExposure} />
        </article>
      </div>

      <div className="space-y-2">
        {relations.slice(0, 3).map((item: RelationExplanationItem) => (
          <RelationExplanationCard key={`${item.source}-${item.target}-${item.relation}`} item={item} />
        ))}
      </div>
    </section>
  );
}
