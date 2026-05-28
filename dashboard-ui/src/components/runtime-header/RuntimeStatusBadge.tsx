"use client";

interface Props {
  label: string;
  phase?: string;
  engineRunning?: boolean;
}

export function RuntimeStatusBadge({
  label,
  phase,
  engineRunning,
}: Props) {
  const active =
    engineRunning ||
    phase === "retrieval_running" ||
    phase === "runtime_active";
  const done = phase === "analysis_complete";

  return (
    <span
      className={
        done
          ? "inline-flex items-center rounded-full border border-emerald-500/40 bg-emerald-500/10 px-2.5 py-0.5 text-xs font-medium text-emerald-400"
          : active
            ? "inline-flex items-center rounded-full border border-primary/40 bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary"
            : "inline-flex items-center rounded-full border border-border bg-muted/40 px-2.5 py-0.5 text-xs text-muted-foreground"
      }
    >
      {engineRunning ? "분석 실행 중…" : label}
    </span>
  );
}
