/** traceId · Dashboard payload 상태 타입 */
import type { DashboardData } from "@/types/dashboard";
import type { SignalEvaluationData } from "@/types/signal-evaluation";
import type { LoadStatus } from "@/types/dashboard";

export type RuntimePhase =
  | "idle"
  | "running_query"
  | "loading_panels"
  | "ready"
  | "error";

export interface RuntimeTraceState {
  traceId: string | null;
  selectedTicker: string | null;
  companyName: string | null;
  runtimeQuery: string | null;
  phase: RuntimePhase;
  panelStatus: LoadStatus;
  loadingMessage: string | null;
  error: string | null;
  warning: string | null;
  data: DashboardData;
  signal: SignalEvaluationData | null;
}

export const EMPTY_DASHBOARD: DashboardData = {
  retrieval: null,
  reflection: null,
  memory: null,
  stockChain: null,
  trace: null,
  evaluation: null,
};

export function createInitialRuntimeState(): RuntimeTraceState {
  return {
    traceId: null,
    selectedTicker: null,
    companyName: null,
    runtimeQuery: null,
    phase: "idle",
    panelStatus: "idle",
    loadingMessage: null,
    error: null,
    warning: null,
    data: EMPTY_DASHBOARD,
    signal: null,
  };
}

export function traceQueryHref(path: string, traceId: string | null): string {
  if (!traceId?.trim()) return path;
  const sep = path.includes("?") ? "&" : "?";
  return `${path}${sep}trace_id=${encodeURIComponent(traceId.trim())}`;
}
