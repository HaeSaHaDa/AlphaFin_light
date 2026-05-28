"use client";

import { useEffect, useMemo, useState } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { GraphNode } from "@/components/event-graph/GraphNode";
import { GraphEdge } from "@/components/event-graph/GraphEdge";
import {
  buildTickerCenteredGraph,
  toMarketFlowElements,
} from "@/market-graph/market-graph-builder";
import type {
  MarketGraphFilters,
  MarketGraphNode,
  MarketGraphEdge,
  MarketGraphPayload,
} from "@/types/market-graph";
import { nodeColor } from "@/market-graph/graph-node-types";

const nodeTypes = { graphNode: GraphNode };
const edgeTypes = { graphEdge: GraphEdge };

interface Props {
  payload: MarketGraphPayload | null;
  filters: MarketGraphFilters;
  height?: number;
  onSelectNode?: (node: MarketGraphNode | null) => void;
}

export function MarketRelationshipGraph({
  payload,
  filters,
  height = 420,
  onSelectNode,
}: Props) {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  const [selected, setSelected] = useState<MarketGraphNode | null>(null);

  const centerId = useMemo(
    () =>
      payload?.nodes.find((n) => n.is_center)?.id ??
      payload?.center_company ??
      "",
    [payload],
  );

  const graphData = useMemo(() => {
    if (!payload) return { nodes: [], edges: [] };
    const { nodes: n, edges: e } = buildTickerCenteredGraph(payload, filters);
    return toMarketFlowElements(n, e, centerId);
  }, [payload, filters, centerId]);

  useEffect(() => {
    setNodes(graphData.nodes);
    setEdges(graphData.edges);
  }, [graphData, setNodes, setEdges]);

  if (!payload) {
    return (
      <div
        className="flex items-center justify-center rounded-lg border border-dashed border-border text-sm text-muted-foreground"
        style={{ height }}
      >
        trace 실행 후 시장 관계 그래프가 표시됩니다
      </div>
    );
  }

  return (
    <div
      className="w-full rounded-lg border border-border bg-zinc-950/50"
      style={{ height }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={(_, node) => {
          const ent =
            payload.nodes.find((n) => n.id === node.id) ?? null;
          setSelected(ent);
          onSelectNode?.(ent);
        }}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        minZoom={0.15}
        maxZoom={1.4}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#3f3f46" gap={16} />
        <Controls className="!bg-card !border-border" />
        <MiniMap
          className="!bg-card !border-border"
          nodeColor={(n) =>
            nodeColor((n.data as { entityType?: string }).entityType)
          }
        />
      </ReactFlow>
    </div>
  );
}
