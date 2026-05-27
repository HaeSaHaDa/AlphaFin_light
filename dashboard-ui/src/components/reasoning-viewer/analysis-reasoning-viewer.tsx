"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { CollapsibleSection } from "@/components/ui/collapsible-section";
import type { AnalysisLoadStatus, RetrievalDetailData } from "@/types/analysis";

interface AnalysisReasoningViewerProps {
  data: RetrievalDetailData | null;
  status: AnalysisLoadStatus;
}

export function AnalysisReasoningViewer({
  data,
  status,
}: AnalysisReasoningViewerProps) {
  const analysis = data?.analysis;

  return (
    <PanelShell
      title="Analysis Reasoning"
      subtitle="bullish · bearish · risks"
      status={status}
      empty={!analysis?.summary}
      className="min-h-[320px]"
    >
      {analysis && (
        <div className="space-y-3 text-sm">
          <CollapsibleSection title="Evidence Summary" defaultOpen>
            <p className="text-xs leading-relaxed text-foreground/90">
              {analysis.summary}
            </p>
          </CollapsibleSection>
          <FactorList title="Bullish Factors" items={analysis.bullish_factors ?? []} tone="positive" />
          <FactorList title="Bearish Factors" items={analysis.bearish_factors ?? []} tone="negative" />
          <FactorList title="Risks" items={analysis.risks ?? []} tone="warning" />
        </div>
      )}
    </PanelShell>
  );
}

function FactorList({
  title,
  items,
  tone,
}: {
  title: string;
  items: string[];
  tone: "positive" | "negative" | "warning";
}) {
  const color =
    tone === "positive"
      ? "text-emerald-400"
      : tone === "negative"
        ? "text-rose-400"
        : "text-amber-400";
  return (
    <CollapsibleSection title={title} defaultOpen={tone !== "warning"}>
      <ul className={`list-inside list-disc space-y-1 text-xs ${color}`}>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </CollapsibleSection>
  );
}
