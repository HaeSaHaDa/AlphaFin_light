"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { MarketImpactPanel } from "@/components/report-layout/MarketImpactPanel";
import { RuntimePanelShell } from "./RuntimePanelShell";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";
import type { LoadStatus, StockChainData } from "@/types/dashboard";

interface Props {
  traceId: string | null;
  status: LoadStatus;
  stockChain: StockChainData | null;
}

export function RuntimeEventGraphPanel({ traceId, status, stockChain }: Props) {
  return (
    <RuntimePanelShell traceId={traceId} status={status} title="Event Graph">
      <div className="space-y-3">
        <MarketImpactPanel data={stockChain} status={status} traceId={traceId} />
        {traceId && (
          <Button variant="outline" size="sm" asChild>
            <Link href={traceQueryHref("/event-graph", traceId)}>
              시장 연결 구조 상세 보기
            </Link>
          </Button>
        )}
      </div>
    </RuntimePanelShell>
  );
}
