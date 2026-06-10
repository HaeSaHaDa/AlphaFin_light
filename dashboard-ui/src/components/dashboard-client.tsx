"use client";

import { useEffect, useState } from "react";
import { Alert } from "@/components/ui/alert";
import { QueryExecutionPanel } from "@/components/company-selector/QueryExecutionPanel";
import { MarketReportHeader } from "@/components/report-layout/MarketReportHeader";
import { BullishFactorsPanel } from "@/components/report-layout/BullishFactorsPanel";
import { RiskFactorsPanel } from "@/components/report-layout/RiskFactorsPanel";
import { RuntimeSignalPanel } from "@/components/runtime-panels/RuntimeSignalPanel";
import { RuntimeNewsPanel } from "@/components/runtime-panels/RuntimeNewsPanel";
import { DisclosurePanel } from "@/components/disclosure/DisclosurePanel";
import { EventSummaryPanel } from "@/components/events/EventSummaryPanel";
import { RuntimeEvidencePanel } from "@/components/runtime/RuntimeEvidencePanel";
import { StickyRuntimeHeader } from "@/components/runtime-header/StickyRuntimeHeader";
import { EmptyStateCard } from "@/components/ui-cleanup/EmptyStateCard";
import { LoadingStateCard } from "@/components/ui-cleanup/LoadingStateCard";
import { SectionDivider } from "@/components/ui-cleanup/SectionDivider";
import { useDashboardRuntime } from "@/runtime-state/runtime-query-context";
import { getRuntimeStatus } from "@/services/api";
import { DASHBOARD_SPACING } from "@/ui/dashboard-spacing";
import type { RuntimeStatusPayload } from "@/types/market-graph";

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
    warning,
    traceId,
    engineRunning,
    companyContext,
    loadByTraceId,
    runQuerySelected,
    selectedTicker,
    companyName,
    loadingMessage,
    signal,
    phase,
  } = useDashboardRuntime();

  const [runtimeStatus, setRuntimeStatus] = useState<RuntimeStatusPayload | null>(
    null,
  );

  useEffect(() => {
    if (!traceId) {
      setRuntimeStatus(null);
      return;
    }
    getRuntimeStatus(traceId)
      .then(setRuntimeStatus)
      .catch(() => setRuntimeStatus(null));
  }, [traceId, engineRunning, phase]);

  const displayQuery =
    data.evaluation?.query ||
    data.retrieval?.query ||
    data.reflection?.query;

  const { bullish, bearish, risks } = getAnalysisFactors(data.retrieval);

  const loading =
    phase === "running_query" ||
    phase === "loading_panels" ||
    status === "loading" ||
    engineRunning;

  const displayCompany =
    companyName ||
    companyContext?.company_name ||
    runtimeStatus?.company_name ||
    "";

  return (
    <div className={`dashboard-shell ${DASHBOARD_SPACING.section}`}>
      <StickyRuntimeHeader
        companyName={displayCompany}
        ticker={selectedTicker ?? runtimeStatus?.ticker ?? ""}
        traceId={traceId}
        runtimeStatus={runtimeStatus}
        engineRunning={engineRunning}
        phase={phase}
      />

      <QueryExecutionPanel
        status={status}
        engineRunning={engineRunning}
        traceId={traceId}
        displayQuery={displayQuery}
        selectedTicker={selectedTicker}
        companyName={displayCompany || companyName}
        companyContext={companyContext}
        onRunQuery={runQuerySelected}
        onLoadByTraceId={loadByTraceId}
      />

      {loading && (
        <LoadingStateCard message={loadingMessage ?? "Runtime 분석 진행 중…"} />
      )}

      {warning && !loading && (
        <Alert className="border-amber-500/50 bg-amber-500/10 text-amber-100">
          <p className="font-medium">분석 데이터 부족</p>
          <p className="mt-1 text-xs opacity-90">{warning}</p>
        </Alert>
      )}

      {error && status === "error" && (
        <Alert variant="destructive">
          <p className="font-medium">Runtime 오류</p>
          <p className="mt-1 text-xs opacity-90">{error}</p>
        </Alert>
      )}

      {!traceId && phase === "idle" && !loading && (
        <EmptyStateCard />
      )}

      <div id="section-summary" className="scroll-mt-24">
        <MarketReportHeader query={displayQuery} traceId={traceId} />
      </div>

      <>
          {traceId && (
            <>
              <div className={DASHBOARD_SPACING.grid3}>
                <RuntimeSignalPanel
                  traceId={traceId}
                  status={status}
                  signal={signal}
                />
                <BullishFactorsPanel factors={bullish} />
                <RiskFactorsPanel risks={risks} bearishFactors={bearish} />
              </div>

              <SectionDivider />
            </>
          )}

          <div id="section-news" className="scroll-mt-24">
            <RuntimeNewsPanel
              traceId={traceId}
              status={status}
              retrieval={data.retrieval}
            />
          </div>

          <EventSummaryPanel
            traceId={traceId}
            ticker={selectedTicker ?? data.retrieval?.ticker ?? null}
          />

          <RuntimeEvidencePanel
            traceId={traceId}
            ticker={selectedTicker ?? data.retrieval?.ticker ?? null}
          />

          <DisclosurePanel
            ticker={selectedTicker ?? data.retrieval?.ticker ?? null}
            traceId={traceId}
          />
      </>
    </div>
  );
}
