export type EventSourceType = "NEWS" | "DISCLOSURE" | "CHUNK" | "MEMORY";

export interface EventEvidence {
  evidence_id?: number;
  event_id?: string;
  source_type: EventSourceType;
  source_id?: string;
  title?: string;
  url?: string;
  published_at?: string;
  relevance_score?: number;
}

export interface CanonicalEvent {
  event_id: string;
  trace_id?: string;
  ticker: string;
  company_name?: string;
  canonical_title: string;
  event_summary?: string;
  event_type?: string;
  event_date?: string;
  confidence_score: number;
  importance_score: number;
  impact_direction?: string;
  evidence_count: number;
  evidence?: EventEvidence[];
}

export interface EventsTracePayload {
  trace_id: string;
  ticker: string;
  query?: string;
  event_count: number;
  events: CanonicalEvent[];
  memory_layers?: EventMemoryLayer[];
  dedup_stats?: Record<string, number>;
}

export interface EventMemoryLayer {
  event_id: string;
  memory_layer: "SHORT" | "MID" | "LONG";
  entered_at?: string;
  promoted_from?: string;
  importance_score?: number;
  is_active?: boolean;
  canonical_title?: string;
}
