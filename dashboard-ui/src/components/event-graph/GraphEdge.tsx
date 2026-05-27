"use client";

import {
  BaseEdge,
  EdgeLabelRenderer,
  getBezierPath,
  type EdgeProps,
} from "@xyflow/react";

export type GraphEdgeData = {
  relationType?: string;
  impactScore?: number;
};

export function GraphEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
  label,
  style,
  markerEnd,
}: EdgeProps) {
  const d = (data ?? {}) as GraphEdgeData;
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
  });

  return (
    <>
      <BaseEdge id={id} path={edgePath} style={style} markerEnd={markerEnd} />
      <EdgeLabelRenderer>
        <div
          className="pointer-events-auto nodrag nopan rounded border border-border bg-background/95 px-1.5 py-0.5 text-[10px] shadow-sm"
          style={{
            position: "absolute",
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
          }}
          title={`${d.relationType ?? "relation"} · impact ${((d.impactScore ?? 0) * 100).toFixed(0)}%`}
        >
          <span className="text-muted-foreground">{d.relationType}</span>
          <span className="ml-1 font-medium text-primary">{label}</span>
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
