"use client";

import { SignalSummaryCard } from "@/components/report-layout/SignalSummaryCard";
import { RuntimePanelShell } from "./RuntimePanelShell";
import type { LoadStatus } from "@/types/dashboard";
import type { SignalEvaluationData } from "@/types/signal-evaluation";

interface Props {
  traceId: string | null;
  status: LoadStatus;
  signal: SignalEvaluationData | null;
}

export function RuntimeSignalPanel({ traceId, status, signal }: Props) {
  return (
    <RuntimePanelShell traceId={traceId} status={status} title="Signal">
      {!signal?.current_signal ? (
        <div className="rounded-xl border border-border bg-card/60 p-5 text-sm text-muted-foreground">
          Signal 데이터가 없습니다.
        </div>
      ) : (
        <SignalSummaryCard signal={signal} />
      )}
    </RuntimePanelShell>
  );
}
