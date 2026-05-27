"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { Badge } from "@/components/ui/badge";
import { CollapsibleSection } from "@/components/ui/collapsible-section";
import type { AnalysisLoadStatus } from "@/types/analysis";
import type { ReflectionData } from "@/types/dashboard";

interface ReflectionDetailViewerProps {
  data: ReflectionData | null;
  status: AnalysisLoadStatus;
}

export function ReflectionDetailViewer({
  data,
  status,
}: ReflectionDetailViewerProps) {
  return (
    <PanelShell
      title="Reflection Detail"
      subtitle={data?.timestamp}
      status={status}
      empty={!data?.reflection_summary}
      className="min-h-[320px]"
    >
      {data && (
        <div className="space-y-3 text-sm">
          {data.overconfidence_detected && (
            <Badge variant="warning">Overconfidence detected</Badge>
          )}
          <p className="text-xs leading-relaxed">{data.reflection_summary}</p>
          <ListSection title="Missing Risks" items={data.missing_risks} />
          <ListSection title="Context Gaps" items={data.context_gaps} />
          <ListSection title="Improvements" items={data.improvement_suggestions} />
          {data.overconfidence_reasons?.length > 0 && (
            <CollapsibleSection title="Overconfidence Reasons" defaultOpen>
              <List items={data.overconfidence_reasons} />
            </CollapsibleSection>
          )}
        </div>
      )}
    </PanelShell>
  );
}

function ListSection({ title, items }: { title: string; items: string[] }) {
  if (!items?.length) return null;
  return (
    <CollapsibleSection title={title} defaultOpen>
      <List items={items} />
    </CollapsibleSection>
  );
}

function List({ items }: { items: string[] }) {
  return (
    <ul className="list-inside list-disc space-y-0.5 text-xs text-muted-foreground">
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}
