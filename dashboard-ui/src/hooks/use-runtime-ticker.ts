"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useRuntimeQuery } from "@/runtime-state/runtime-query-context";
import {
  loadRuntimeSession,
  RUNTIME_SESSION_EVENT,
  type RuntimeSession,
} from "@/runtime-state/runtime-session";

/** URL trace_id · React 컨텍스트 · sessionStorage 종목 메타 통합 */
export function useRuntimeTicker() {
  const params = useSearchParams();
  const urlTrace = params.get("trace_id")?.trim() || null;
  const ctx = useRuntimeQuery();
  const [session, setSession] = useState<RuntimeSession | null>(null);

  useEffect(() => {
    const refresh = () => setSession(loadRuntimeSession());
    refresh();
    window.addEventListener(RUNTIME_SESSION_EVENT, refresh);
    return () => window.removeEventListener(RUNTIME_SESSION_EVENT, refresh);
  }, [urlTrace]);

  const traceId = urlTrace || ctx.traceId || session?.traceId || null;
  const ctxAligned = Boolean(ctx.traceId && traceId && ctx.traceId === traceId);

  const ticker =
    (ctxAligned && ctx.selectedTicker) || session?.ticker || null;
  const companyName =
    (ctxAligned && ctx.companyName) || session?.companyName || null;
  const runtimeQuery =
    (ctxAligned && ctx.runtimeQuery) || session?.runtimeQuery || null;

  return {
    traceId,
    ticker,
    companyName,
    runtimeQuery,
    fromUrl: Boolean(urlTrace),
    fromSession: Boolean(session?.traceId && !ctxAligned),
  };
}
