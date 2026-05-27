"use client";

import { useCallback, useEffect, useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
  type NodeMouseHandler,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { GraphNode } from "@/components/event-graph/GraphNode";
import { GraphEdge } from "@/components/event-graph/GraphEdge";
import { applyFilters, toFlowElements } from "@/lib/event-graph/transform";
import type { EventGraphFilters, EventGraphPayload } from "@/types/event-graph";
import type { GraphEntity } from "@/types/event-graph";

const nodeTypes = { graphNode: GraphNode };
const edgeTypes = { graphEdge: GraphEdge };

interface EventGraphProps {
  payload: EventGraphPayload | null;
  filters: EventGraphFilters;
  selectedEntity: GraphEntity | null;
  onSelectEntity: (entity: GraphEntity | null) => void;
  onHoverEntity: (name: string | null) => void;
}

export function EventGraph({
  payload,
  filters,
  selectedEntity,
  onSelectEntity,
  onHoverEntity,
}: EventGraphProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  const graphData = useMemo(() => {
    if (!payload) return { nodes: [], edges: [] };
    const { entities, links } = applyFilters(payload, filters);
    return toFlowElements(entities, links, filters);
  }, [payload, filters]);

  useEffect(() => {
    const withSelection = graphData.nodes.map((n) => ({
      ...n,
      data: {
        ...n.data,
        selected: selectedEntity?.id === n.id,
      },
    }));
    setNodes(withSelection);
    setEdges(graphData.edges);
  }, [graphData, selectedEntity, setNodes, setEdges]);

  const onNodeClick: NodeMouseHandler = useCallback(
    (_, node) => {
      const entity = payload?.entities.find((e) => e.id === node.id) ?? null;
      onSelectEntity(entity);
    },
    [payload, onSelectEntity],
  );

  if (!payload) {
    return (
      <div className="flex h-[480px] items-center justify-center rounded-lg border border-dashed border-border text-sm text-muted-foreground">
        Stock Chain 데이터를 불러오세요
      </div>
    );
  }

  return (
    <div className="h-[520px] w-full rounded-lg border border-border bg-zinc-950/50">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        onNodeMouseEnter={(_, n) => onHoverEntity(n.id)}
        onNodeMouseLeave={() => onHoverEntity(null)}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        minZoom={0.2}
        maxZoom={1.5}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#3f3f46" gap={16} />
        <Controls className="!bg-card !border-border" />
        <MiniMap
          className="!bg-card !border-border"
          nodeColor={(n) => {
            const t = (n.data as { entityType?: string }).entityType;
            if (t === "company") return "#3b82f6";
            if (t === "product") return "#22c55e";
            return "#71717a";
          }}
        />
      </ReactFlow>
    </div>
  );
}
