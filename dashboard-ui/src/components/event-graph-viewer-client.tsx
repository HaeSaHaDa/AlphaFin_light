"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useActiveTrace } from "@/hooks/use-active-trace";
import { RuntimeTraceBanner } from "@/components/runtime-panels/RuntimeTraceBanner";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { DashboardNav } from "@/components/layout/dashboard-nav";
import { MarketRelationshipGraph } from "@/components/market-graph/MarketRelationshipGraph";
import { MarketGraphLegend } from "@/components/market-graph/MarketGraphLegend";
import { MarketGraphToolbar } from "@/components/market-graph/MarketGraphToolbar";
import { GraphNodeDetailPanel } from "@/components/market-graph/GraphNodeDetailPanel";
import { StickyRuntimeHeader } from "@/components/runtime-header/StickyRuntimeHeader";
import { useMarketGraph } from "@/hooks/use-market-graph";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";
import { API_BASE } from "@/services/api";
import type { MarketGraphNode } from "@/types/market-graph";

export function EventGraphViewerClient() {
  const { traceId } = useActiveTrace();
  const {
    payload,
    runtimeStatus,
    filters,
    updateFilters,
    status,
    error,
    load,
  } = useMarketGraph();
  const [selected, setSelected] = useState<MarketGraphNode | null>(null);

  useEffect(() => {
    if (traceId) load(traceId);
  }, [traceId, load]);

  return (
    <div className="mx-auto max-w-7xl space-y-4 p-4 md:p-6">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <DashboardNav traceId={traceId} apiBase={API_BASE} />
        <Button variant="outline" size="sm" asChild>
          <Link href={traceQueryHref("/", traceId)}>Overview</Link>
        </Button>
      </div>

      <StickyRuntimeHeader
        companyName={payload?.center_company ?? runtimeStatus?.company_name ?? ""}
        ticker={payload?.center_ticker ?? runtimeStatus?.ticker ?? ""}
        traceId={traceId}
        runtimeStatus={runtimeStatus}
      />

      <RuntimeTraceBanner />

      <div className="rounded-lg border border-border bg-card p-4">
        <h2 className="text-lg font-semibold">시장 관계 그래프</h2>
        <p className="mt-1 text-xs text-muted-foreground">
          selectedTicker 중심 · 산업·리스크·경쟁 관계 (traceId 기준)
        </p>
        {payload?.query && (
          <p className="mt-2 text-sm">
            Query: <span className="text-primary">{payload.query}</span>
          </p>
        )}
      </div>

      {!traceId && (
        <Alert className="border-border bg-muted/30">
          <p className="text-sm">
            trace_id가 없습니다. Dashboard에서 분석 실행 후 이동하거나{" "}
            <code className="text-xs">?trace_id=...</code> 를 지정하세요.
          </p>
        </Alert>
      )}

      {error && (
        <Alert variant="destructive">
          <p className="text-sm">{error}</p>
        </Alert>
      )}

      <MarketGraphToolbar
        filters={filters}
        onChange={updateFilters}
        onRefresh={() => traceId && load(traceId)}
        loading={status === "loading"}
      />

      <div className="grid gap-4 lg:grid-cols-[1fr_240px]">
        <MarketRelationshipGraph
          payload={payload}
          filters={filters}
          height={520}
          onSelectNode={setSelected}
        />
        <div className="space-y-4">
          <MarketGraphLegend />
          <GraphNodeDetailPanel node={selected} />
          {payload && payload.risks.length > 0 && (
            <div className="text-xs">
              <p className="font-medium text-muted-foreground">리스크</p>
              <ul className="mt-1 list-inside list-disc text-foreground/90">
                {payload.risks.slice(0, 4).map((r) => (
                  <li key={r}>{r}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
