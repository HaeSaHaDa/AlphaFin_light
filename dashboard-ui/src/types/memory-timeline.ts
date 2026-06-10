export type MemoryLayer = "short_term" | "mid_term" | "long_term";
export type MemoryStatus = "active" | "promoted" | "decayed" | "archived";

export interface MemoryEvidence {
  chunk_id?: number;
  document_type?: string;
  title?: string;
  report_name?: string;
  report_date?: string;
  published_at?: string;
  text?: string;
  chunk_text?: string;
  url?: string;
  document_url?: string;
}

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
  evidence?: MemoryEvidence[];
}

export interface MemoryTimelineFilters {
  layers: Set<MemoryLayer>;
  minImportance: number;
}
