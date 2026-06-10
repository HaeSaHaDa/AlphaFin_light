"use client";

import { useRuntimeTicker } from "@/hooks/use-runtime-ticker";

/** URL ?trace_id= 우선, 없으면 최근 분석 session · 컨텍스트 */
export function useActiveTrace() {
  return useRuntimeTicker();
}
