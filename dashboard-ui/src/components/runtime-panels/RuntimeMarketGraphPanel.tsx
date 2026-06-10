"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { SecondaryActionButton } from "@/components/ui-cleanup/SecondaryActionButton";
import { MarketRelationshipGraph } from "@/components/market-graph/MarketRelationshipGraph";
import { MarketGraphLegend } from "@/components/market-graph/MarketGraphLegend";
import { MarketGraphToolbar } from "@/components/market-graph/MarketGraphToolbar";
import { GraphNodeDetailPanel } from "@/components/market-graph/GraphNodeDetailPanel";
import { MarketInsightPanel } from "@/components/market-intelligence/MarketInsightPanel";
import { useMarketGraph } from "@/hooks/use-market-graph";
import { RuntimePanelShell } from "./RuntimePanelShell";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";
import type { LoadStatus } from "@/types/dashboard";
import type { MarketGraphNode } from "@/types/market-graph";

interface Props {
  traceId: string | null;
  status: LoadStatus;
}

export function RuntimeMarketGraphPanel({ traceId, status }: Props) {
  const {
    payload,
    filters,
    updateFilters,
    load,
    status: graphStatus,
    marketInsight,
    riskExposure,
  } = useMarketGraph();
  const [selected, setSelected] = useState<MarketGraphNode | null>(null);

  useEffect(() => {
    if (traceId) load(traceId);
  }, [traceId, load]);

  const panelStatus =
    graphStatus === "loading" ? "loading" : status;

  return (
    <RuntimePanelShell
      traceId={traceId}
      status={panelStatus}
      title="시장 관계 그래프"
    >
      <div className="dash-panel dash-panel-graph space-y-3 p-4 md:p-5">
        {payload?.center_company && (
          <p className="text-xs text-muted-foreground">
            중심:{" "}
            <span className="font-medium text-foreground">
              {payload.center_company} / {payload.center_ticker}
            </span>
          </p>
        )}
        <MarketGraphToolbar
          filters={filters}
          onChange={updateFilters}
          onRefresh={() => traceId && load(traceId)}
          loading={graphStatus === "loading"}
        />
        <div className="grid gap-4 lg:grid-cols-[1fr_200px]">
          <MarketRelationshipGraph
            payload={payload}
            filters={filters}
            height={380}
            onSelectNode={setSelected}
          />
          <div className="space-y-3">
            <MarketGraphLegend />
            <GraphNodeDetailPanel node={selected} />
          </div>
        </div>
        <MarketInsightPanel insight={marketInsight} riskExposure={riskExposure} />
        {traceId && (
          <SecondaryActionButton asChild>
            <Link href={traceQueryHref("/event-graph", traceId)}>
              그래프 전체 화면
            </Link>
          </SecondaryActionButton>
        )}
      </div>
    </RuntimePanelShell>
  );
}
