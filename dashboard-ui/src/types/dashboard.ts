export interface RetrievalChunk {
  chunk_id?: number;
  document_type?: string;
  score?: number;
  ticker?: string;
  text?: string;
  source?: string;
}

export interface RetrievalData {
  trace_id: string;
  query: string;
  ticker: string;
  chunk_count: number;
  chunks: RetrievalChunk[];
  retrieval_quality: Record<string, unknown>;
  context_usage: Record<string, unknown>;
  unified_context_length: number;
  retrieval_timestamp?: string;
  analysis?: Record<string, unknown>;
  context_layers?: Record<string, unknown>;
}

export interface ReflectionData {
  trace_id: string;
  query: string;
  persona: string;
  reflection_summary: string;
  missing_risks: string[];
  overconfidence_detected: boolean;
  overconfidence_reasons: string[];
  context_gaps: string[];
  improvement_suggestions: string[];
  timestamp: string;
}

export interface MemoryData {
  trace_id: string;
  query: string;
  memory_updates: Record<string, unknown>;
  temporal_result: Record<string, unknown>;
  layered_memory: {
    short_term?: MemoryItem[];
    mid_term?: MemoryItem[];
    long_term?: MemoryItem[];
  };
  layer_counts: Record<string, number>;
}

export interface MemoryItem {
  memory_type?: string;
  query?: string;
  persona?: string;
  importance_score?: number;
  summary?: string;
  layer?: string;
  retention_action?: string;
  timestamp?: string;
}

export interface StockChainEntity {
  name: string;
  entity_type?: string;
  ticker?: string | null;
  is_center?: boolean;
  event_type?: string | null;
  created_at?: string;
}

export interface StockChainLink {
  source: string;
  target: string;
  relation_type?: string;
  impact_score?: number;
}

export interface StockChainData {
  trace_id: string;
  query: string;
  ticker: string;
  center_name?: string;
  center_ticker?: string;
  summary: Record<string, unknown>;
  chain: {
    entities?: StockChainEntity[];
    links?: StockChainLink[];
    query?: string;
    ticker?: string;
  };
}

export interface TraceStep {
  step?: string;
  name?: string;
  status?: string;
  detail?: string;
  summary?: string;
  timestamp?: string;
}

export interface TraceData {
  trace: {
    trace_id?: string;
    steps?: TraceStep[];
  };
  unified_result_summary: {
    trace_id: string;
    query: string;
    completed_at: string;
  };
  pipeline_flow: string[];
}

export interface EvaluationData {
  trace_id: string;
  query: string;
  retrieval_score: number | null;
  reasoning_score: number | null;
  reflection_score: number | null;
  memory_score: number | null;
  stock_chain_score: number | null;
  overall_score: number | null;
  consistency: Record<string, unknown>;
  hallucination_risk: Record<string, unknown>;
  evaluated_at: string;
}

export interface DashboardData {
  retrieval: RetrievalData | null;
  reflection: ReflectionData | null;
  memory: MemoryData | null;
  stockChain: StockChainData | null;
  trace: TraceData | null;
  evaluation: EvaluationData | null;
}

export type LoadStatus = "idle" | "loading" | "success" | "error";
