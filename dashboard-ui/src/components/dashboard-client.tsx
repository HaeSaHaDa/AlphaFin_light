"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Alert } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { DashboardNav } from "@/components/layout/dashboard-nav";
import { QueryExecutionPanel } from "@/components/company-selector/QueryExecutionPanel";
import { MarketReportHeader } from "@/components/report-layout/MarketReportHeader";
import { BullishFactorsPanel } from "@/components/report-layout/BullishFactorsPanel";
import { RiskFactorsPanel } from "@/components/report-layout/RiskFactorsPanel";
import { ExplainabilityAccordion } from "@/components/report-layout/ExplainabilityAccordion";
import { RuntimeSignalPanel } from "@/components/runtime-panels/RuntimeSignalPanel";
import { RuntimeNewsPanel } from "@/components/runtime-panels/RuntimeNewsPanel";
import { RuntimeMarketGraphPanel } from "@/components/runtime-panels/RuntimeMarketGraphPanel";
import { StickyRuntimeHeader } from "@/components/runtime-header/StickyRuntimeHeader";
import { useDashboardRuntime } from "@/runtime-state/runtime-query-context";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";
import { API_BASE, getRuntimeStatus } from "@/services/api";
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
    <div className="dashboard-shell">
      <div className="dashboard-nav-row">
        <DashboardNav traceId={traceId} apiBase={API_BASE} showAnalysisLink={false} />
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm" asChild>
            <Link href={traceQueryHref("/analysis", traceId)}>상세 분석</Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link href={traceQueryHref("/event-graph", traceId)}>시장 연결 구조</Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link href={traceQueryHref("/memory-timeline", traceId)}>시장 기억</Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link href={traceQueryHref("/signal-evaluation", traceId)}>Signal 평가</Link>
          </Button>
        </div>
      </div>

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
        companyContext={companyContext}
        onRunQuery={runQuerySelected}
        onLoadByTraceId={loadByTraceId}
      />

      {loading && loadingMessage && (
        <Alert className="border-primary/40 bg-primary/10">
          <p className="text-sm font-medium">{loadingMessage}</p>
          <p className="mt-1 text-xs text-muted-foreground">
            모든 패널이 동일 traceId 기준으로 동기화됩니다.
            {traceId && (
              <span className="ml-2 font-mono">trace: {traceId}</span>
            )}
          </p>
        </Alert>
      )}

      {warning && (
        <Alert className="border-amber-500/50 bg-amber-500/10 text-amber-100">
          <p className="font-medium">분석 데이터 부족</p>
          <p className="mt-1 text-xs opacity-90">{warning}</p>
        </Alert>
      )}

      {error && status === "error" && (
        <Alert variant="destructive">
          <p className="font-medium">Runtime 오류</p>
          <p className="mt-1 text-xs opacity-90">{error}</p>
          <p className="mt-1 text-xs opacity-75">
            sample/latest fallback 없음 — trace_id 기준 payload만 표시합니다.
          </p>
        </Alert>
      )}

      {!traceId && phase === "idle" && (
        <Alert className="border-border bg-muted/30">
          <p className="text-sm">
            자동완성에서 종목을 선택하고 키워드를 입력한 뒤{" "}
            <strong>분석 실행</strong>을 누르세요.
            실행 후 모든 패널이 동일 <strong>traceId</strong>로 갱신됩니다.
          </p>
        </Alert>
      )}

      <div id="section-summary" className="scroll-mt-24">
        <MarketReportHeader query={displayQuery} traceId={traceId} />
      </div>

      {loading ? (
        <div className="dashboard-grid-3">
          <Skeleton className="h-40 rounded-xl" />
          <Skeleton className="h-40 rounded-xl" />
          <Skeleton className="h-40 rounded-xl" />
        </div>
      ) : (
        <>
          <div className="dashboard-grid-3">
            <RuntimeSignalPanel
              traceId={traceId}
              status={status}
              signal={signal}
            />
            <BullishFactorsPanel factors={bullish} />
            <RiskFactorsPanel risks={risks} bearishFactors={bearish} />
          </div>

          <div id="section-news" className="scroll-mt-24">
            <RuntimeNewsPanel
              traceId={traceId}
              status={status}
              retrieval={data.retrieval}
            />
          </div>

          <RuntimeMarketGraphPanel traceId={traceId} status={status} />

          <ExplainabilityAccordion
            data={data}
            signal={signal}
            status={status}
            traceId={traceId}
          />
        </>
      )}
    </div>
  );
}
