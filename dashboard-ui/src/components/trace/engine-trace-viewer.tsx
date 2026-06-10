"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { Badge } from "@/components/ui/badge";
import { PIPELINE_FALLBACK } from "@/services/api";
import { CheckCircle2, Circle } from "lucide-react";
import type { LoadStatus, TraceData } from "@/types/dashboard";

interface EngineTraceViewerProps {
  data: TraceData | null;
  status: LoadStatus;
}

export function EngineTraceViewer({ data, status }: EngineTraceViewerProps) {
  const pipeline = data?.pipeline_flow ?? PIPELINE_FALLBACK;
  const steps = data?.trace?.steps ?? [];
  const completedAt = data?.unified_result_summary?.completed_at;

  return (
    <PanelShell
      title="Engine Trace"
      subtitle={completedAt ? `완료: ${completedAt}` : "Full reasoning pipeline"}
      status={status}
      empty={!data}
      className="max-h-none"
    >
      {data && (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-1">
            {pipeline.map((step, i) => (
              <div key={step} className="flex items-center text-xs">
                <Badge variant="outline" className="font-mono">
                  {step}
                </Badge>
                {i < pipeline.length - 1 && (
                  <span className="mx-1 text-muted-foreground">→</span>
                )}
              </div>
            ))}
          </div>
          {steps.length > 0 ? (
            <ol className="space-y-2 border-t border-border pt-3">
              {steps.map((step, i) => (
                <li
                  key={`${step.step ?? step.name}-${i}`}
                  className="flex items-start gap-2 text-xs"
                >
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-400" />
                  <div>
                    <span className="font-medium">
                      {step.step ?? step.name ?? `step ${i + 1}`}
                    </span>
                    {step.detail && (
                      <p className="text-muted-foreground">{step.detail}</p>
                    )}
                  </div>
                </li>
              ))}
            </ol>
          ) : (
            <ul className="grid gap-2 sm:grid-cols-2">
              {pipeline.map((step) => (
                <li
                  key={step}
                  className="flex items-center gap-2 rounded border border-border/50 px-2 py-1.5 text-xs"
                >
                  <Circle className="h-3 w-3 text-primary" />
                  {step}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </PanelShell>
  );
}
