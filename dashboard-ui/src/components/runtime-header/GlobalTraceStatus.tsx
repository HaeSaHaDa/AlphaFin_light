"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { getRuntimeStatus } from "@/services/api";
import type { RuntimeStatusPayload } from "@/types/market-graph";
import { RuntimeStatusIndicator } from "@/components/navigation/RuntimeStatusIndicator";

export function GlobalTraceStatus() {
  const params = useSearchParams();
  const traceId = params.get("trace_id");
  const [status, setStatus] = useState<RuntimeStatusPayload | null>(null);

  useEffect(() => {
    if (!traceId) {
      setStatus(null);
      return;
    }
    getRuntimeStatus(traceId).then(setStatus).catch(() => setStatus(null));
  }, [traceId]);

  return (
    <div className="flex items-center gap-2">
      <RuntimeStatusIndicator status={status} />
      {traceId ? (
        <span className="font-mono text-[11px] text-muted-foreground">
          trace: {traceId}
        </span>
      ) : null}
    </div>
  );
}
