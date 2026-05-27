"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { PropagationStep, TemporalEvent } from "@/types/event-graph";

interface PropagationPanelProps {
  path: PropagationStep[];
  temporalEvents: TemporalEvent[];
}

export function PropagationPanel({ path, temporalEvents }: PropagationPanelProps) {
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Propagation Flow</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {path.map((step, i) => (
            <div key={`${step.source}-${step.target}-${i}`}>
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <span className="font-medium text-primary">{step.source}</span>
                <span className="text-muted-foreground">↓</span>
                <span className="font-medium">{step.target}</span>
                <Badge variant="success">
                  {(step.impact_score * 100).toFixed(0)}%
                </Badge>
              </div>
              <p className="ml-1 text-[10px] text-muted-foreground">
                {step.relation_type}
              </p>
            </div>
          ))}
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Temporal Relations</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {temporalEvents.map((ev, i) => (
            <div key={`${ev.period}-${i}`} className="flex gap-3 text-xs">
              <span className="shrink-0 font-mono text-muted-foreground">
                {ev.period}
              </span>
              <div>
                <p className="font-medium">{ev.label}</p>
                {ev.relation && (
                  <p className="text-muted-foreground">{ev.relation}</p>
                )}
              </div>
              {i < temporalEvents.length - 1 && (
                <span className="ml-auto text-muted-foreground">↓</span>
              )}
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
