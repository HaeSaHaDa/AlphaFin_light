export type MemoryLayer = "short_term" | "mid_term" | "long_term";
export type MemoryStatus = "active" | "promoted" | "decayed" | "archived";

export interface MemoryNodeData {
  id: string;
  query: string;
  summary?: string;
  layer: MemoryLayer;
  importance_score: number;
  status: MemoryStatus;
  timestamp?: string;
  persona?: string;
  retention_action?: string;
  promoted_from?: MemoryLayer;
}

export interface MemoryTimelineFilters {
  layers: Set<MemoryLayer>;
  minImportance: number;
}
