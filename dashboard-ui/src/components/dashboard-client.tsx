"use client";

import Link from "next/link";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Alert } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { DashboardNav } from "@/components/layout/dashboard-nav";
import { QueryInputPanel } from "@/components/query/query-input-panel";
import { MarketReportHeader } from "@/components/report-layout/MarketReportHeader";
import { SignalSummaryCard } from "@/components/report-layout/SignalSummaryCard";
import { BullishFactorsPanel } from "@/components/report-layout/BullishFactorsPanel";
import { RiskFactorsPanel } from "@/components/report-layout/RiskFactorsPanel";
import { RelatedNewsPanel } from "@/components/report-layout/RelatedNewsPanel";
import { MarketImpactPanel } from "@/components/report-layout/MarketImpactPanel";
import { ExplainabilityAccordion } from "@/components/report-layout/ExplainabilityAccordion";
import { useDashboardData } from "@/hooks/use-dashboard-data";
import { useSignalEvaluation } from "@/hooks/use-signal-evaluation";
import { API_BASE } from "@/services/api";

function getAnalysisFactors(retrieval: { analysis?: Record<string, unknown> } | null) {
  const a = retrieval?.analysis ?? {};
  return {
    bullish: (a.bullish_factors as string[]) ?? [],
    bearish: (a.bearish_factors as string[]) ?? [],
    risks: (a.risks as string[]) ?? [],
  };
}

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

  const { data: signalData } = useSignalEvaluation(traceId);

  useEffect(() => {
    loadLatest();
  }, [loadLatest]);

  const displayQuery =
    data.evaluation?.query ||
    data.retrieval?.query ||
    data.reflection?.query;

  const { bullish, bearish, risks } = getAnalysisFactors(data.retrieval);
  const loading = status === "loading" || engineRunning;

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-6">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <DashboardNav traceId={traceId} apiBase={API_BASE} showAnalysisLink={false} />
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm" asChild>
            <Link href="/analysis">상세 분석</Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link href="/event-graph">시장 연결 구조</Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link href="/memory-timeline">시장 기억</Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link href="/signal-evaluation">Signal 평가</Link>
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
            Backend: uvicorn src.dashboard_api.app:app --host 0.0.0.0 --port 8000
          </p>
        </Alert>
      )}

      <MarketReportHeader query={displayQuery} traceId={traceId} />

      {loading ? (
        <div className="grid gap-4 md:grid-cols-3">
          <Skeleton className="h-40 rounded-xl" />
          <Skeleton className="h-40 rounded-xl" />
          <Skeleton className="h-40 rounded-xl" />
        </div>
      ) : (
        <>
          <div className="grid gap-4 md:grid-cols-3">
            <SignalSummaryCard signal={signalData} />
            <BullishFactorsPanel factors={bullish} />
            <RiskFactorsPanel risks={risks} bearishFactors={bearish} />
          </div>

          <RelatedNewsPanel chunks={data.retrieval?.chunks ?? []} />

          <MarketImpactPanel
            data={data.stockChain}
            status={status}
            traceId={traceId}
          />

          <ExplainabilityAccordion
            data={data}
            signal={signalData}
            status={status}
            traceId={traceId}
          />
        </>
      )}
    </div>
  );
}
