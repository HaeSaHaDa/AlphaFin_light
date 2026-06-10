"use client";

import {
  RUNTIME_STATUS_CLASS,
  RUNTIME_STATUS_LABEL,
  resolveRuntimeStatusKind,
} from "@/ui/runtime-status-theme";

interface Props {
  label?: string;
  phase?: string;
  engineRunning?: boolean;
}

export function RuntimeStatusCard({ label, phase, engineRunning }: Props) {
  const kind = resolveRuntimeStatusKind({ engineRunning, phase, label });
  const text =
    engineRunning
      ? "분석 실행 중…"
      : label || RUNTIME_STATUS_LABEL[kind];

  return (
    <span className={RUNTIME_STATUS_CLASS[kind]} role="status">
      {kind === "running" || kind === "retrieval" ? (
        <span className="mr-1.5 inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-current" />
      ) : null}
      {text}
    </span>
  );
}
