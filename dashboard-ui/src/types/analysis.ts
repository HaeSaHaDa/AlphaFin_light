import type {
  EvaluationData,
  ReflectionData,
  RetrievalData,
  TraceData,
} from "@/types/dashboard";

export interface EnrichedChunk {
  chunk_id?: number;
  document_type?: string;
  score?: number;
  ticker?: string;
  rank?: number;
  source_file?: string;
  chunk_preview?: string;
  related_entity?: string;
}

export interface RetrievalDetailData extends RetrievalData {
  retrieval_timestamp?: string;
  analysis?: {
    summary?: string;
    bullish_factors?: string[];
    bearish_factors?: string[];
    risks?: string[];
    model?: string;
  };
  context_layers?: {
    retrieval?: Record<string, unknown>;
    memory?: Record<string, unknown>;
    reflection?: Record<string, unknown>;
    stock_chain?: Record<string, unknown>;
    temporal?: Record<string, unknown>;
  };
  chunks: EnrichedChunk[];
}

export interface AnalysisViewerData {
  retrieval: RetrievalDetailData | null;
  reflection: ReflectionData | null;
  trace: TraceData | null;
  evaluation: EvaluationData | null;
}

export type AnalysisLoadStatus = "idle" | "loading" | "success" | "error";
