"use client";

import { Button } from "@/components/ui/button";
import type { MarketGraphFilters } from "@/types/market-graph";
import { NODE_CATEGORY_LABELS } from "@/market-graph/graph-node-types";
import { EDGE_TYPE_LABELS } from "@/market-graph/graph-edge-types";

interface Props {
  filters: MarketGraphFilters;
  onChange: (partial: Partial<MarketGraphFilters>) => void;
  onRefresh?: () => void;
  loading?: boolean;
}

export function MarketGraphToolbar({
  filters,
  onChange,
  onRefresh,
  loading,
}: Props) {
  return (
    <div className="flex flex-wrap items-end gap-3 text-xs">
      <label className="flex flex-col gap-1">
        <span className="text-muted-foreground">최소 관련도</span>
        <input
          type="range"
          min={0.3}
          max={0.9}
          step={0.05}
          value={filters.minRelevance}
          onChange={(e) =>
            onChange({ minRelevance: Number(e.target.value) })
          }
          className="w-32"
        />
      </label>
      <label className="flex flex-col gap-1">
        <span className="text-muted-foreground">Node</span>
        <select
          className="rounded border border-border bg-card px-2 py-1"
          value={filters.category}
          onChange={(e) =>
            onChange({
              category: e.target.value as MarketGraphFilters["category"],
            })
          }
        >
          <option value="all">전체</option>
          {Object.entries(NODE_CATEGORY_LABELS).map(([k, v]) => (
            <option key={k} value={k}>
              {v}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1">
        <span className="text-muted-foreground">Edge</span>
        <select
          className="rounded border border-border bg-card px-2 py-1"
          value={filters.edgeType}
          onChange={(e) =>
            onChange({
              edgeType: e.target.value as MarketGraphFilters["edgeType"],
            })
          }
        >
          <option value="all">전체</option>
          {Object.entries(EDGE_TYPE_LABELS).map(([k, v]) => (
            <option key={k} value={k}>
              {v}
            </option>
          ))}
        </select>
      </label>
      {onRefresh && (
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={onRefresh}
          disabled={loading}
        >
          새로고침
        </Button>
      )}
    </div>
  );
}
