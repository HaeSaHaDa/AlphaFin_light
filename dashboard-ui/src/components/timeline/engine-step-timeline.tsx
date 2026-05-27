"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { CheckCircle2, Circle } from "lucide-react";
import type { AnalysisLoadStatus } from "@/types/analysis";
import type { TraceData } from "@/types/dashboard";

const DEMO_FLOW = [
  "retrieval",
  "context assembly",
  "reasoning",
  "reflection",
  "memory update",
  "stock chain",
  "evaluation",
];

interface EngineStepTimelineProps {
  trace: TraceData | null;
  status: AnalysisLoadStatus;
}

export function EngineStepTimeline({ trace, status }: EngineStepTimelineProps) {
  const steps = trace?.trace?.steps ?? [];
  const flow = trace?.pipeline_flow?.length
    ? mapPipelineLabels(trace.pipeline_flow)
    : DEMO_FLOW;

  return (
    <PanelShell
      title="Engine Step Timeline"
      subtitle={trace?.unified_result_summary?.completed_at}
      status={status}
      empty={!trace}
      className="max-h-none"
    >
      <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
        {flow.map((step, i) => (
          <span key={step} className="flex items-center gap-1">
            <span className="rounded border border-border px-2 py-0.5 font-mono text-foreground">
              {step}
            </span>
            {i < flow.length - 1 && <span>→</span>}
          </span>
        ))}
      </div>
      {steps.length > 0 && (
        <ol className="mt-4 space-y-2 border-t border-border pt-3">
          {steps.map((step, i) => (
            <li key={`${step.step}-${i}`} className="flex gap-2 text-xs">
              {step.status === "ok" ? (
                <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
              ) : (
                <Circle className="h-4 w-4 shrink-0 text-muted-foreground" />
              )}
              <div>
                <span className="font-medium">{step.step ?? step.name}</span>
                {step.summary && (
                  <p className="text-muted-foreground">{step.summary}</p>
                )}
                {step.timestamp && (
                  <p className="text-[10px] text-muted-foreground/70">
                    {step.timestamp}
                  </p>
                )}
              </div>
            </li>
          ))}
        </ol>
      )}
    </PanelShell>
  );
}

function mapPipelineLabels(steps: string[]): string[] {
  const labels: Record<string, string> = {
    retrieval: "retrieval",
    context_assembly: "context assembly",
    character_analysis: "reasoning",
    evaluation: "evaluation",
    reflection: "reflection",
    memory_save: "memory update",
    importance_update: "memory update",
    temporal_tracking: "temporal",
    event_graph: "event graph",
    stock_chain: "stock chain",
    result_save: "final result",
  };
  const seen = new Set<string>();
  const out: string[] = [];
  for (const s of steps) {
    const label = labels[s] ?? s;
    if (!seen.has(label)) {
      seen.add(label);
      out.push(label);
    }
  }
  return out;
}
