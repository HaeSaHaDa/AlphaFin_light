"use client";

import Link from "next/link";
import { useEffect } from "react";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { DashboardNav } from "@/components/layout/dashboard-nav";
import { EventGraph } from "@/components/event-graph/EventGraph";
import { GraphLegend } from "@/components/event-graph/GraphLegend";
import { GraphToolbar } from "@/components/event-graph/GraphToolbar";
import { NodeDetailPanel } from "@/components/event-graph/NodeDetailPanel";
import { PropagationPanel } from "@/components/event-graph/PropagationPanel";
import { useEventGraph } from "@/hooks/use-event-graph";
import { API_BASE } from "@/services/api";

export function EventGraphViewerClient() {
  const {
    payload,
    filters,
    baseFilters,
    updateFilters,
    status,
    error,
    selectedEntity,
    setSelectedEntity,
    setHoveredId,
    connectedCount,
    loadLatest,
  } = useEventGraph();

  useEffect(() => {
    loadLatest();
  }, [loadLatest]);

  return (
    <div className="mx-auto max-w-7xl space-y-4 p-4 md:p-6">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <DashboardNav
          traceId={payload?.traceId ?? null}
          apiBase={API_BASE}
          showAnalysisLink
        />
        <div className="flex gap-2">
          <Button variant="outline" size="sm" asChild>
            <Link href="/">Overview</Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link href="/analysis">Analysis</Link>
          </Button>
        </div>
      </div>

      <div className="rounded-lg border border-border bg-card p-4">
        <h2 className="text-lg font-semibold">Event Graph Visualization</h2>
        <p className="mt-1 text-xs text-muted-foreground">
          Stock Chain · propagation · NVIDIA / HBM / 삼성전자 관계망
        </p>
        {payload?.query && (
          <p className="mt-2 text-sm">
            Query: <span className="text-primary">{payload.query}</span>
          </p>
        )}
      </div>

      {error && (
        <Alert variant="destructive">
          <p className="text-sm">{error}</p>
        </Alert>
      )}

      <GraphToolbar
        filters={baseFilters}
        onChange={updateFilters}
        onRefresh={loadLatest}
        loading={status === "loading"}
      />

      <div className="grid gap-4 lg:grid-cols-[1fr_240px]">
        <EventGraph
          payload={payload}
          filters={filters}
          selectedEntity={selectedEntity}
          onSelectEntity={setSelectedEntity}
          onHoverEntity={setHoveredId}
        />
        <div className="space-y-4">
          <GraphLegend />
          <NodeDetailPanel
            entity={selectedEntity}
            connectedCount={connectedCount}
          />
        </div>
      </div>

      {payload && (
        <PropagationPanel
          path={payload.propagationPath}
          temporalEvents={payload.temporalEvents}
        />
      )}
    </div>
  );
}
