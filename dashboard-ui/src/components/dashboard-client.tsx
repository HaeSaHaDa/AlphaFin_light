"use client";

import Link from "next/link";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Alert } from "@/components/ui/alert";
import { DashboardNav } from "@/components/layout/dashboard-nav";
import { QueryInputPanel } from "@/components/query/query-input-panel";
import { RetrievalViewer } from "@/components/retrieval/retrieval-viewer";
import { ReflectionViewer } from "@/components/reflection/reflection-viewer";
import { MemoryTimelineViewer } from "@/components/memory/memory-timeline-viewer";
import { StockChainViewer } from "@/components/stock-chain/stock-chain-viewer";
import { EngineTraceViewer } from "@/components/trace/engine-trace-viewer";
import { EvaluationScorePanel } from "@/components/evaluation/evaluation-score-panel";
import { useDashboardData } from "@/hooks/use-dashboard-data";
import { API_BASE } from "@/services/api";

export function DashboardClient() {
  const {
    data,
    status,
    error,
    traceId,
    engineRunning,
    loadLatest,
    loadByTraceId,
    runAndLoad,
  } = useDashboardData();

  useEffect(() => {
    loadLatest();
  }, [loadLatest]);

  const displayQuery =
    data.evaluation?.query ||
    data.retrieval?.query ||
    data.reflection?.query;

  return (
    <div className="mx-auto max-w-7xl space-y-4 p-4 md:p-6">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <DashboardNav traceId={traceId} apiBase={API_BASE} />
        <div className="flex gap-2">
          <Button variant="outline" size="sm" asChild>
            <Link href="/analysis">Analysis</Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link href="/event-graph">Event Graph</Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link href="/memory-timeline">시장 기억</Link>
          </Button>
        </div>
      </div>

      <QueryInputPanel
        status={status}
        engineRunning={engineRunning}
        traceId={traceId}
        displayQuery={displayQuery}
        onRunEngine={runAndLoad}
        onLoadLatest={loadLatest}
        onLoadByTraceId={loadByTraceId}
      />

      {error && (
        <Alert variant="destructive">
          <p className="font-medium">API 연동 실패</p>
          <p className="mt-1 text-xs opacity-90">{error}</p>
          <p className="mt-2 text-xs opacity-75">
            Backend 실행: uvicorn src.dashboard_api.app:app --host 0.0.0.0 --port 8000
          </p>
        </Alert>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        <RetrievalViewer data={data.retrieval} status={status} />
        <ReflectionViewer data={data.reflection} status={status} />
        <MemoryTimelineViewer data={data.memory} status={status} />
        <StockChainViewer data={data.stockChain} status={status} />
      </div>

      <EngineTraceViewer data={data.trace} status={status} />
      <EvaluationScorePanel data={data.evaluation} status={status} />
    </div>
  );
}
