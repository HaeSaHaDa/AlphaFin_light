"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import type { EntityTypeFilter, EventGraphFilters } from "@/types/event-graph";

const ENTITY_TYPES: { value: EntityTypeFilter; label: string }[] = [
  { value: "all", label: "전체" },
  { value: "company", label: "기업" },
  { value: "industry", label: "산업" },
  { value: "product", label: "제품" },
  { value: "market_event", label: "이벤트" },
  { value: "price_change", label: "가격" },
];

interface GraphToolbarProps {
  filters: EventGraphFilters;
  onChange: (next: Partial<EventGraphFilters>) => void;
  onRefresh: () => void;
  loading?: boolean;
  /** runtime stock-chain entities — 하드코드 프리셋 대신 사용 */
  highlightOptions?: string[];
}

export function GraphToolbar({
  filters,
  onChange,
  onRefresh,
  loading,
  highlightOptions = [],
}: GraphToolbarProps) {
  return (
    <div className="flex flex-col gap-3 rounded-lg border border-border bg-card/80 p-3">
      <div className="flex flex-wrap items-center gap-2">
        <Input
          className="max-w-[200px]"
          placeholder="엔티티 검색…"
          value={filters.search}
          onChange={(e) => onChange({ search: e.target.value })}
        />
        <label className="flex items-center gap-2 text-xs text-muted-foreground">
          Min impact
          <input
            type="range"
            min={0.5}
            max={0.9}
            step={0.05}
            value={filters.minImpact}
            onChange={(e) =>
              onChange({ minImpact: parseFloat(e.target.value) })
            }
            className="w-24"
          />
          <span className="font-mono text-foreground">
            {(filters.minImpact * 100).toFixed(0)}%
          </span>
        </label>
        <Button type="button" size="sm" variant="secondary" onClick={onRefresh} disabled={loading}>
          Refresh Graph
        </Button>
      </div>
      <div className="flex flex-wrap gap-1">
        {ENTITY_TYPES.map(({ value, label }) => (
          <Button
            key={value}
            type="button"
            size="sm"
            variant={filters.entityType === value ? "default" : "outline"}
            onClick={() => onChange({ entityType: value })}
          >
            {label}
          </Button>
        ))}
      </div>
      {highlightOptions.length > 0 && (
      <div className="flex flex-wrap gap-1">
        <span className="self-center text-[10px] text-muted-foreground">Highlight:</span>
        {highlightOptions.map((name) => (
          <Button
            key={name}
            type="button"
            size="sm"
            variant={
              filters.highlightEntities.includes(name) ? "default" : "ghost"
            }
            className="h-7 text-xs"
            onClick={() => {
              const has = filters.highlightEntities.includes(name);
              onChange({
                highlightEntities: has
                  ? filters.highlightEntities.filter((h) => h !== name)
                  : [...filters.highlightEntities, name],
              });
            }}
          >
            {name}
          </Button>
        ))}
      </div>
      )}
    </div>
  );
}
