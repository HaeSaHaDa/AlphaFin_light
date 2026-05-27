"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { Badge } from "@/components/ui/badge";
import type { LoadStatus, ReflectionData } from "@/types/dashboard";

interface ReflectionViewerProps {
  data: ReflectionData | null;
  status: LoadStatus;
}

export function ReflectionViewer({ data, status }: ReflectionViewerProps) {
  return (
    <PanelShell
      title="Reflection Viewer"
      subtitle={data?.persona}
      status={status}
      empty={!data}
    >
      {data && (
        <div className="space-y-3 text-sm">
          <p className="leading-relaxed text-foreground/90">
            {data.reflection_summary}
          </p>
          {data.overconfidence_detected && (
            <Badge variant="warning">Overconfidence detected</Badge>
          )}
          <Section title="Missing Risks" items={data.missing_risks} />
          <Section title="Context Gaps" items={data.context_gaps} />
          <Section
            title="Improvements"
            items={data.improvement_suggestions}
          />
        </div>
      )}
    </PanelShell>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  if (!items?.length) return null;
  return (
    <div>
      <h4 className="mb-1 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
        {title}
      </h4>
      <ul className="list-inside list-disc space-y-0.5 text-xs text-foreground/80">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
