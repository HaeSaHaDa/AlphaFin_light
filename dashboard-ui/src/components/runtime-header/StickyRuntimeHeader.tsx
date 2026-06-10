"use client";

import { SelectedTickerInfo } from "./SelectedTickerInfo";
import { RuntimeStatusCard } from "@/components/ui-cleanup/RuntimeStatusCard";
import { DetailLocalNavigation } from "@/components/navigation-cleanup/DetailLocalNavigation";
import type { RuntimeStatusPayload } from "@/types/market-graph";

interface Props {
  companyName: string;
  ticker: string;
  traceId: string | null;
  runtimeStatus: RuntimeStatusPayload | null;
  engineRunning?: boolean;
  phase?: string;
}

export function StickyRuntimeHeader({
  companyName,
  ticker,
  traceId,
  runtimeStatus,
  engineRunning,
  phase,
}: Props) {
  const label =
    runtimeStatus?.label ??
    (engineRunning ? "Runtime Active" : traceId ? "Runtime Active" : "Idle");

  return (
    <header className="runtime-sticky-header">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <SelectedTickerInfo
          companyName={companyName || runtimeStatus?.company_name || ""}
          ticker={ticker || runtimeStatus?.ticker || ""}
          traceId={traceId}
        />
        <RuntimeStatusCard
          label={label}
          phase={runtimeStatus?.phase ?? phase}
          engineRunning={engineRunning}
        />
      </div>
      <div className="mt-3">
        <DetailLocalNavigation />
      </div>
    </header>
  );
}
