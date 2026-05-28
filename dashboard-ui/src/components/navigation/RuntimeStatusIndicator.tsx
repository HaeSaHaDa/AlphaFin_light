"use client";

import type { RuntimeStatusPayload } from "@/types/market-graph";

export function RuntimeStatusIndicator({
  status,
}: {
  status: RuntimeStatusPayload | null;
}) {
  const label = status?.label ?? "Runtime Active";
  const tone =
    status?.phase === "analysis_complete"
      ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-400"
      : "border-primary/40 bg-primary/10 text-primary";
  return (
    <span className={`rounded-full border px-2.5 py-0.5 text-xs ${tone}`}>
      {label}
    </span>
  );
}
