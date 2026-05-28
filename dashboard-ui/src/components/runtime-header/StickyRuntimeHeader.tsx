"use client";

import { SelectedTickerInfo } from "./SelectedTickerInfo";
import { RuntimeStatusBadge } from "./RuntimeStatusBadge";
import { RuntimeSectionNav } from "./RuntimeSectionNav";
import { RuntimeActionBar } from "./RuntimeActionBar";
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
        <RuntimeStatusBadge
          label={label}
          phase={runtimeStatus?.phase ?? phase}
          engineRunning={engineRunning}
        />
      </div>
      <div className="mt-3 flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
        <RuntimeSectionNav />
        <RuntimeActionBar traceId={traceId} />
      </div>
    </header>
  );
}
