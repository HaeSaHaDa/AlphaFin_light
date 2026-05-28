"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import {
  loadRuntimeSession,
  type RuntimeSession,
} from "@/runtime-state/runtime-session";

/** URL ?trace_id= 우선, 없으면 최근 분석 session */
export function useActiveTrace() {
  const params = useSearchParams();
  const urlTrace = params.get("trace_id")?.trim() || null;
  const [session, setSession] = useState<RuntimeSession | null>(null);

  useEffect(() => {
    setSession(loadRuntimeSession());
  }, []);

  const traceId = urlTrace || session?.traceId || null;

  return {
    traceId,
    ticker: session?.ticker ?? null,
    companyName: session?.companyName ?? null,
    runtimeQuery: session?.runtimeQuery ?? null,
    fromUrl: Boolean(urlTrace),
    fromSession: Boolean(!urlTrace && session?.traceId),
  };
}
