"use client";

import { memo } from "react";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import { cn } from "@/lib/utils";
import { entityColor } from "@/lib/event-graph/transform";

export type GraphNodeData = {
  label: string;
  entityType?: string;
  ticker?: string | null;
  isCenter?: boolean;
  highlighted?: boolean;
  selected?: boolean;
};

function GraphNodeComponent({ data, selected }: NodeProps) {
  const d = data as GraphNodeData;
  const color = entityColor(d.entityType);

  return (
    <div
      className={cn(
        "min-w-[120px] rounded-lg border-2 bg-card px-3 py-2 shadow-md transition-shadow",
        selected && "ring-2 ring-primary",
        (d.isCenter || d.highlighted) && "border-primary shadow-primary/30",
        d.isCenter && "ring-1 ring-primary/50",
      )}
      style={{ borderColor: d.highlighted || selected ? color : `${color}99` }}
    >
      <Handle type="target" position={Position.Left} className="!bg-muted-foreground" />
      <p className="text-sm font-semibold text-foreground">{d.label}</p>
      <p className="text-[10px] uppercase tracking-wide text-muted-foreground">
        {d.entityType ?? "entity"}
      </p>
      {d.ticker && (
        <p className="mt-0.5 font-mono text-[10px] text-primary">{d.ticker}</p>
      )}
      <Handle type="source" position={Position.Right} className="!bg-muted-foreground" />
    </div>
  );
}

export const GraphNode = memo(GraphNodeComponent);
