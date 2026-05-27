import { Button } from "@/components/ui/button";
import type { MemoryLayer, MemoryTimelineFilters } from "@/types/memory-timeline";

interface MemoryToolbarProps {
  filters: MemoryTimelineFilters;
  onFilterChange: (f: MemoryTimelineFilters) => void;
  onReset: () => void;
}

const LAYER_LABELS: Record<MemoryLayer, string> = {
  short_term: "단기 기억",
  mid_term: "중기 기억",
  long_term: "장기 기억",
};

const IMPORTANCE_STEPS = [0, 0.3, 0.5, 0.7, 0.9];

export function MemoryToolbar({ filters, onFilterChange, onReset }: MemoryToolbarProps) {
  const toggleLayer = (layer: MemoryLayer) => {
    const next = new Set(filters.layers);
    if (next.has(layer)) {
      if (next.size > 1) next.delete(layer);
    } else {
      next.add(layer);
    }
    onFilterChange({ ...filters, layers: next });
  };

  const setImportance = (v: number) => {
    onFilterChange({ ...filters, minImportance: v });
  };

  return (
    <div className="flex flex-wrap items-center gap-3 rounded-lg border border-border bg-card/60 px-4 py-2 text-xs">
      <span className="font-medium text-muted-foreground">기억 유형</span>
      {(Object.keys(LAYER_LABELS) as MemoryLayer[]).map((layer) => (
        <button
          key={layer}
          onClick={() => toggleLayer(layer)}
          className={`rounded px-2 py-1 transition-colors ${
            filters.layers.has(layer)
              ? layer === "short_term"
                ? "bg-blue-500/30 text-blue-300"
                : layer === "mid_term"
                  ? "bg-yellow-500/30 text-yellow-300"
                  : "bg-purple-500/30 text-purple-300"
              : "bg-card text-muted-foreground opacity-50"
          }`}
        >
          {LAYER_LABELS[layer]}
        </button>
      ))}

      <span className="text-border">|</span>
      <span className="font-medium text-muted-foreground">최소 중요도</span>
      {IMPORTANCE_STEPS.map((v) => (
        <button
          key={v}
          onClick={() => setImportance(v)}
          className={`rounded px-2 py-1 transition-colors ${
            filters.minImportance === v
              ? "bg-primary/30 text-primary"
              : "bg-card text-muted-foreground hover:bg-card/80"
          }`}
        >
          {v === 0 ? "전체" : `≥ ${v}`}
        </button>
      ))}

      <Button variant="ghost" size="sm" onClick={onReset} className="ml-auto text-xs">
        초기화
      </Button>
    </div>
  );
}
