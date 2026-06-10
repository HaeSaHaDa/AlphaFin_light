/** Runtime status badge themes. */

export type RuntimeStatusKind =
  | "idle"
  | "running"
  | "retrieval"
  | "complete"
  | "error";

export function resolveRuntimeStatusKind(opts: {
  engineRunning?: boolean;
  phase?: string;
  label?: string;
}): RuntimeStatusKind {
  if (opts.engineRunning) return "running";
  const p = (opts.phase || "").toLowerCase();
  if (p.includes("retrieval") || p.includes("running")) return "retrieval";
  if (p.includes("complete") || (opts.label || "").includes("Complete")) {
    return "complete";
  }
  if (p === "error") return "error";
  if (opts.label?.includes("Active")) return "complete";
  return "idle";
}

export const RUNTIME_STATUS_CLASS: Record<RuntimeStatusKind, string> = {
  idle: "dash-status dash-status-idle",
  running: "dash-status dash-status-running",
  retrieval: "dash-status dash-status-retrieval",
  complete: "dash-status dash-status-complete",
  error: "dash-status dash-status-error",
};

export const RUNTIME_STATUS_LABEL: Record<RuntimeStatusKind, string> = {
  idle: "대기",
  running: "Runtime Active",
  retrieval: "Retrieval Running",
  complete: "Analysis Complete",
  error: "오류",
};
