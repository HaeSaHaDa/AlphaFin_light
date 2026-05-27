"use client";

import { useState } from "react";
import { MemoryTrack } from "./MemoryTrack";
import { MemoryDetailPanel } from "./MemoryDetailPanel";
import { MemoryLegend } from "./MemoryLegend";
import { MemoryToolbar } from "./MemoryToolbar";
import { MemorySummaryPanel } from "./MemorySummaryPanel";
import type { MemoryLayer, MemoryNodeData, MemoryTimelineFilters } from "@/types/memory-timeline";

interface MemoryTimelineProps {
  nodes: MemoryNodeData[];
  query: string;
}

const ALL_LAYERS: MemoryLayer[] = ["short_term", "mid_term", "long_term"];

const DEFAULT_FILTERS: MemoryTimelineFilters = {
  layers: new Set<MemoryLayer>(["short_term", "mid_term", "long_term"]),
  minImportance: 0,
};

export function MemoryTimeline({ nodes, query }: MemoryTimelineProps) {
  const [selectedNode, setSelectedNode] = useState<MemoryNodeData | null>(null);
  const [filters, setFilters] = useState<MemoryTimelineFilters>(DEFAULT_FILTERS);

  const filteredNodes = nodes.filter(
    (n) => filters.layers.has(n.layer) && n.importance_score >= filters.minImportance,
  );

  const resetFilters = () => {
    setFilters({
      layers: new Set<MemoryLayer>(["short_term", "mid_term", "long_term"]),
      minImportance: 0,
    });
    setSelectedNode(null);
  };

  return (
    <div className="space-y-4">
      {/* 범례 */}
      <MemoryLegend />

      {/* 툴바 */}
      <MemoryToolbar
        filters={filters}
        onFilterChange={setFilters}
        onReset={resetFilters}
      />

      {/* 타임라인 + 사이드패널 */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        {/* 타임라인 본체: 3개 트랙 */}
        <div className="space-y-6 lg:col-span-2">
          {ALL_LAYERS.filter((l) => filters.layers.has(l)).map((layer) => (
            <MemoryTrack
              key={layer}
              layer={layer}
              nodes={filteredNodes.filter((n) => n.layer === layer)}
              selectedId={selectedNode?.id ?? null}
              onSelect={setSelectedNode}
            />
          ))}
          {filteredNodes.length === 0 && (
            <p className="py-10 text-center text-sm text-muted-foreground">
              조건에 맞는 기억 데이터가 없습니다.
            </p>
          )}
        </div>

        {/* 우측 사이드패널 */}
        <div className="space-y-4">
          <MemoryDetailPanel node={selectedNode} />
          <MemorySummaryPanel nodes={nodes} query={query} />
        </div>
      </div>
    </div>
  );
}
